from __future__ import annotations

import json
import sqlite3
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

from app.ops_api import normalized_title
from app.semantic.candidates import assess_candidate
from app.semantic.signatures import extract_event_signature, signature_match
from app.utils import utc_now
from scripts.evaluate_ops_quality import QualityItem, build_quality_items


REPO_CONTENT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB = REPO_CONTENT_DIR / "data" / "content_inbox.sqlite3"
REPORT_PATH = REPO_CONTENT_DIR / "docs" / "event_aggregation_deep_diagnostic_20260531.md"


@dataclass
class PairDecision:
    case_a: str
    case_b: str
    gold_same_event: bool
    gold_non_event: bool
    lightweight_same_title: bool
    signature_same_event: bool
    candidate_priority: str
    candidate_lane: str
    candidate_score: float
    candidate_predict_high: bool
    candidate_predict_medium: bool
    same_actor: bool
    same_product: bool
    same_action: bool
    signature_a: dict[str, Any]
    signature_b: dict[str, Any]
    disqualifiers: list[str]
    evidence: list[str]
    score_components: dict[str, float]


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def pair_metrics(gold: set[tuple[str, str]], predicted: set[tuple[str, str]]) -> dict[str, Any]:
    tp = len(gold & predicted)
    fp = len(predicted - gold)
    fn = len(gold - predicted)
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}


def item_dict(item: QualityItem) -> dict[str, Any]:
    return {
        "item_id": item.case_id,
        "url": item.url,
        "guid": item.gold_dedupe_group if item.case_id.startswith("guid_") else None,
        "title": item.title,
        "summary": item.summary,
        "content_text": item.content_text,
        "source_id": item.source_id,
        "source_name": item.source_name,
        "source_category": item.source_category,
        "published_at": item.published_at,
        "created_at": item.published_at,
    }


def card_dict(item: QualityItem) -> dict[str, Any]:
    text = f"{item.title}\n{item.summary}\n{item.content_text}"
    entities = []
    for token in item.expected_entities:
        if token not in entities:
            entities.append(token)
    return {
        "item_id": item.case_id,
        "canonical_title": item.title,
        "short_summary": item.summary,
        "event_hint": item.summary,
        "content_role": "source_material",
        "confidence": 0.8,
        "entities_json": json.dumps(entities, ensure_ascii=False),
        "text": text,
    }


def gold_same_event_pairs(items: list[QualityItem]) -> set[tuple[str, str]]:
    labels = {
        item.case_id: item.gold_event
        for item in items
        if item.should_form_event
    }
    groups: dict[str, list[str]] = defaultdict(list)
    for case_id, event_id in labels.items():
        groups[event_id].append(case_id)
    pairs: set[tuple[str, str]] = set()
    for members in groups.values():
        for a, b in combinations(sorted(members), 2):
            pairs.add((a, b))
    return pairs


def gold_non_event_pairs(items: list[QualityItem]) -> set[tuple[str, str]]:
    non_event_ids = sorted(item.case_id for item in items if not item.should_form_event)
    pairs: set[tuple[str, str]] = set()
    for a, b in combinations(non_event_ids, 2):
        pairs.add((a, b))
    return pairs


def diagnose_pairs(items: list[QualityItem]) -> tuple[list[PairDecision], dict[str, Any]]:
    by_id = {item.case_id: item for item in items}
    same_event = gold_same_event_pairs(items)
    non_event = gold_non_event_pairs(items)
    decisions: list[PairDecision] = []
    lightweight_pred: set[tuple[str, str]] = set()
    signature_pred: set[tuple[str, str]] = set()
    candidate_high_pred: set[tuple[str, str]] = set()
    candidate_medium_pred: set[tuple[str, str]] = set()

    for left, right in combinations(sorted(by_id), 2):
        a = by_id[left]
        b = by_id[right]
        left_item = item_dict(a)
        right_item = item_dict(b)
        left_card = card_dict(a)
        right_card = card_dict(b)
        pair = (left, right)
        lightweight = normalized_title(a.title) == normalized_title(b.title)
        left_sig = extract_event_signature(left_item, left_card)
        right_sig = extract_event_signature(right_item, right_card)
        sig_match = signature_match(left_sig, right_sig)
        assessment = assess_candidate(left_item, right_item, left_card, right_card)
        predict_high = (
            assessment.candidate_priority in {"must_run", "high"}
            and not assessment.suppressed
            and (
                assessment.event_signature_match
                or assessment.same_actor and assessment.same_product and assessment.same_action
                or any("same_actor_product_action_72h" in ev for ev in assessment.same_event_evidence)
                or any(ev == "high_title_similarity" for ev in assessment.same_event_evidence)
            )
            and not any(d in assessment.disqualifiers for d in {"generic_entity_overlap", "generic_only_overlap", "wide_time_window", "semantic_level_reject"})
        )
        predict_medium = predict_high or (
            assessment.candidate_priority == "medium"
            and assessment.same_actor
            and (assessment.same_product or assessment.same_action)
            and not assessment.suppressed
            and not any(d in assessment.disqualifiers for d in {"generic_entity_overlap", "generic_only_overlap", "wide_time_window", "semantic_level_reject"})
        )
        if lightweight:
            lightweight_pred.add(pair)
        if sig_match:
            signature_pred.add(pair)
        if predict_high:
            candidate_high_pred.add(pair)
        if predict_medium:
            candidate_medium_pred.add(pair)
        decisions.append(
            PairDecision(
                case_a=left,
                case_b=right,
                gold_same_event=pair in same_event,
                gold_non_event=pair in non_event,
                lightweight_same_title=lightweight,
                signature_same_event=sig_match,
                candidate_priority=assessment.candidate_priority,
                candidate_lane=assessment.lane,
                candidate_score=assessment.candidate_score,
                candidate_predict_high=predict_high,
                candidate_predict_medium=predict_medium,
                same_actor=assessment.same_actor,
                same_product=assessment.same_product,
                same_action=assessment.same_action,
                signature_a=left_sig.model_dump(),
                signature_b=right_sig.model_dump(),
                disqualifiers=assessment.disqualifiers,
                evidence=assessment.same_event_evidence,
                score_components=assessment.candidate_score_components,
            )
        )

    metrics = {
        "gold_same_event_pairs": len(same_event),
        "gold_non_event_pairs": len(non_event),
        "lightweight": pair_metrics(same_event, lightweight_pred),
        "signature_exact": pair_metrics(same_event, signature_pred),
        "candidate_high": pair_metrics(same_event, candidate_high_pred),
        "candidate_medium": pair_metrics(same_event, candidate_medium_pred),
        "lightweight_false_positive_pairs": sorted(lightweight_pred - same_event),
        "lightweight_false_negative_pairs": sorted(same_event - lightweight_pred),
        "candidate_high_false_positive_pairs": sorted(candidate_high_pred - same_event),
        "candidate_high_false_negative_pairs": sorted(same_event - candidate_high_pred),
        "candidate_medium_false_positive_pairs": sorted(candidate_medium_pred - same_event),
        "candidate_medium_false_negative_pairs": sorted(same_event - candidate_medium_pred),
    }
    return decisions, metrics


def signature_failure_summary(decisions: list[PairDecision]) -> dict[str, Any]:
    gold_failures = [d for d in decisions if d.gold_same_event and not d.candidate_predict_high]
    reasons = Counter()
    examples: list[dict[str, Any]] = []
    for decision in gold_failures:
        if decision.disqualifiers:
            for reason in decision.disqualifiers:
                reasons[reason] += 1
        if decision.signature_a.get("semantic_level") != "event_signature":
            reasons[f"a_{decision.signature_a.get('semantic_level')}"] += 1
        if decision.signature_b.get("semantic_level") != "event_signature":
            reasons[f"b_{decision.signature_b.get('semantic_level')}"] += 1
        if not decision.same_actor:
            reasons["actor_mismatch_or_missing"] += 1
        if not decision.same_product:
            reasons["product_mismatch_or_missing"] += 1
        if not decision.same_action:
            reasons["action_mismatch_or_missing"] += 1
        if len(examples) < 12:
            examples.append(
                {
                    "pair": [decision.case_a, decision.case_b],
                    "priority": decision.candidate_priority,
                    "lane": decision.candidate_lane,
                    "score": decision.candidate_score,
                    "signature_a": {
                        "level": decision.signature_a.get("semantic_level"),
                        "actor": decision.signature_a.get("actor"),
                        "product": decision.signature_a.get("product_or_model"),
                        "action": decision.signature_a.get("action"),
                        "key": decision.signature_a.get("signature_key"),
                        "invalid": decision.signature_a.get("invalid_reasons"),
                    },
                    "signature_b": {
                        "level": decision.signature_b.get("semantic_level"),
                        "actor": decision.signature_b.get("actor"),
                        "product": decision.signature_b.get("product_or_model"),
                        "action": decision.signature_b.get("action"),
                        "key": decision.signature_b.get("signature_key"),
                        "invalid": decision.signature_b.get("invalid_reasons"),
                    },
                    "disqualifiers": decision.disqualifiers,
                    "evidence": decision.evidence,
                    "score_components": decision.score_components,
                }
            )
    return {"reason_counts": dict(reasons.most_common()), "examples": examples}


def current_db_signature_scan(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT item_id, title, summary, content_text, url, guid, source_id, source_name,
                   source_category, published_at, created_at
            FROM inbox_items
            WHERE deleted_at IS NULL
            """
        ).fetchall()
    ]
    levels: Counter[str] = Counter()
    actions: Counter[str] = Counter()
    actors: Counter[str] = Counter()
    products: Counter[str] = Counter()
    invalid: Counter[str] = Counter()
    signature_groups: dict[str, list[str]] = defaultdict(list)
    title_groups: dict[str, list[str]] = defaultdict(list)
    for item in rows:
        signature = extract_event_signature(item, None)
        levels[signature.semantic_level] += 1
        actions[signature.action] += 1
        if signature.actor:
            actors[signature.actor] += 1
        if signature.product_or_model:
            products[signature.product_or_model] += 1
        for reason in signature.invalid_reasons:
            invalid[reason] += 1
        if signature.signature_key:
            signature_groups[signature.signature_key].append(item["item_id"])
        title_groups[normalized_title(item.get("title") or "")].append(item["item_id"])
    multi_signature = {key: ids for key, ids in signature_groups.items() if len(ids) > 1}
    multi_title = {key: ids for key, ids in title_groups.items() if len(ids) > 1}
    return {
        "items_scanned": len(rows),
        "semantic_levels": levels.most_common(),
        "top_actions": actions.most_common(15),
        "top_actors": actors.most_common(15),
        "top_products": products.most_common(15),
        "top_invalid_reasons": invalid.most_common(15),
        "signature_groups": len(signature_groups),
        "multi_signature_groups": len(multi_signature),
        "items_in_multi_signature_groups": sum(len(ids) for ids in multi_signature.values()),
        "exact_title_groups": len(title_groups),
        "multi_exact_title_groups": len(multi_title),
        "items_in_multi_exact_title_groups": sum(len(ids) for ids in multi_title.values()),
    }


def current_db_stats(db_path: Path = DEFAULT_DB) -> dict[str, Any]:
    if not db_path.exists():
        return {"exists": False, "path": str(db_path)}
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        tables = {}
        for table in [
            "rss_sources",
            "rss_ingest_runs",
            "item_run_links",
            "inbox_items",
            "event_clusters",
            "cluster_items",
            "events",
            "review_queue",
            "dedupe_groups",
            "dedupe_group_items",
            "item_cards",
            "item_relations",
            "cluster_cards",
            "llm_call_logs",
        ]:
            row = conn.execute("SELECT COUNT(*) AS n FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
            if row["n"]:
                tables[table] = conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]
        clusters_by_creator = [
            dict(row)
            for row in conn.execute(
                """
                SELECT created_by, COUNT(*) AS clusters,
                       SUM(CASE WHEN item_count > 1 THEN 1 ELSE 0 END) AS multi_clusters,
                       ROUND(AVG(item_count), 2) AS avg_items,
                       MAX(item_count) AS max_items
                FROM event_clusters
                GROUP BY created_by
                ORDER BY clusters DESC
                """
            ).fetchall()
        ] if tables.get("event_clusters") else []
        cluster_relation_stats = [
            dict(row)
            for row in conn.execute(
                """
                SELECT primary_relation, same_event, decision_source, COUNT(*) AS n
                FROM cluster_items
                GROUP BY primary_relation, same_event, decision_source
                ORDER BY n DESC
                """
            ).fetchall()
        ] if tables.get("cluster_items") else []
        event_type_stats = [
            dict(row)
            for row in conn.execute(
                """
                SELECT event_type, status, COUNT(*) AS n
                FROM events
                GROUP BY event_type, status
                ORDER BY n DESC
                """
            ).fetchall()
        ] if tables.get("events") else []
        source_status_stats = [
            dict(row)
            for row in conn.execute(
                """
                SELECT status, COUNT(*) AS n
                FROM rss_sources
                GROUP BY status
                ORDER BY n DESC
                """
            ).fetchall()
        ] if tables.get("rss_sources") else []
        item_seen_stats = dict(conn.execute(
            """
            SELECT COUNT(*) AS items,
                   SUM(CASE WHEN seen_count > 1 THEN 1 ELSE 0 END) AS items_seen_multiple,
                   MAX(seen_count) AS max_seen,
                   ROUND(AVG(seen_count), 2) AS avg_seen,
                   SUM(seen_count) AS total_seen
            FROM inbox_items
            """
        ).fetchone()) if tables.get("inbox_items") else {}
        clustering_json_stats = [
            dict(row)
            for row in conn.execute(
                """
                SELECT json_extract(clustering_json, '$.cluster_relation') AS relation, COUNT(*) AS n
                FROM inbox_items
                WHERE clustering_json IS NOT NULL
                GROUP BY relation
                ORDER BY n DESC
                """
            ).fetchall()
        ] if tables.get("inbox_items") else []
        cluster_integrity = dict(conn.execute(
            """
            SELECT COUNT(*) AS clusters,
                   SUM(CASE WHEN ci.n IS NULL THEN 1 ELSE 0 END) AS clusters_without_cluster_items,
                   SUM(CASE WHEN ci.n IS NOT NULL AND ci.n != ec.item_count THEN 1 ELSE 0 END) AS item_count_mismatch
            FROM event_clusters ec
            LEFT JOIN (
                SELECT cluster_id, COUNT(*) AS n
                FROM cluster_items
                GROUP BY cluster_id
            ) ci ON ci.cluster_id = ec.cluster_id
            """
        ).fetchone()) if tables.get("event_clusters") else {}
        return {
            "exists": True,
            "path": str(db_path),
            "table_counts": tables,
            "source_status_stats": source_status_stats,
            "item_seen_stats": item_seen_stats,
            "cluster_integrity": cluster_integrity,
            "clusters_by_creator": clusters_by_creator,
            "cluster_relation_stats": cluster_relation_stats,
            "event_type_stats": event_type_stats,
            "clustering_json_stats": clustering_json_stats,
            "signature_scan": current_db_signature_scan(conn) if tables.get("inbox_items") else {},
        }
    finally:
        conn.close()


def render_report(decisions: list[PairDecision], metrics: dict[str, Any], db_stats: dict[str, Any]) -> str:
    signature_summary = signature_failure_summary(decisions)
    status = "不通过"
    lines = [
        "# 事件去重与聚合深度诊断",
        "",
        f"生成时间: {utc_now()}",
        "",
        "## 第一性原理定义",
        "",
        "你的目标不是把“相似标题”放在一起，而是把多条信息映射到同一个现实世界事件，并保留它们之间的信息增量。一个合格事件聚合系统至少要回答四个问题：",
        "",
        "1. 这是不是事件，还是日报、综述、教程、观点、主题线索？",
        "2. 如果是事件，它的主体、对象、动作、时间窗口是什么？",
        "3. 两条内容是同一事件、同一主题不同事件、同一产品不同进展，还是纯重复？",
        "4. 合并后是否新增事实、角度或证据，是否值得进入简报？",
        "",
        f"本轮状态: **{status}**。当前作战台接入的是 lightweight 标题规则，语义聚合模块存在但没有进入这条 console pipeline。",
        "",
        "## 对照实验",
        "",
        "| 方法 | Precision | Recall | F1 | TP | FP | FN |",
        "|---|---:|---:|---:|---:|---:|---:|",
        f"| 当前 lightweight 完全标题 | {pct(metrics['lightweight']['precision'])} | {pct(metrics['lightweight']['recall'])} | {pct(metrics['lightweight']['f1'])} | {metrics['lightweight']['tp']} | {metrics['lightweight']['fp']} | {metrics['lightweight']['fn']} |",
        f"| semantic signature 精确匹配 | {pct(metrics['signature_exact']['precision'])} | {pct(metrics['signature_exact']['recall'])} | {pct(metrics['signature_exact']['f1'])} | {metrics['signature_exact']['tp']} | {metrics['signature_exact']['fp']} | {metrics['signature_exact']['fn']} |",
        f"| semantic candidate high | {pct(metrics['candidate_high']['precision'])} | {pct(metrics['candidate_high']['recall'])} | {pct(metrics['candidate_high']['f1'])} | {metrics['candidate_high']['tp']} | {metrics['candidate_high']['fp']} | {metrics['candidate_high']['fn']} |",
        f"| semantic candidate medium+ | {pct(metrics['candidate_medium']['precision'])} | {pct(metrics['candidate_medium']['recall'])} | {pct(metrics['candidate_medium']['f1'])} | {metrics['candidate_medium']['tp']} | {metrics['candidate_medium']['fp']} | {metrics['candidate_medium']['fn']} |",
        "",
        f"Gold same-event pair 数: {metrics['gold_same_event_pairs']}；Gold 非事件 pair 数: {metrics['gold_non_event_pairs']}。",
        "",
        "### 当前 lightweight 失败样例",
        "",
        f"- 误合并: `{metrics['lightweight_false_positive_pairs'][:12]}`",
        f"- 漏合并: `{metrics['lightweight_false_negative_pairs'][:12]}`",
        "",
        "### semantic candidate 失败样例",
        "",
        f"- high 阈值误合并: `{metrics['candidate_high_false_positive_pairs'][:12]}`",
        f"- high 阈值漏合并: `{metrics['candidate_high_false_negative_pairs'][:12]}`",
        f"- medium+ 阈值误合并: `{metrics['candidate_medium_false_positive_pairs'][:12]}`",
        f"- medium+ 阈值漏合并: `{metrics['candidate_medium_false_negative_pairs'][:12]}`",
        "",
        "## 根因拆解",
        "",
        "### 1. 接入根因",
        "",
        "console pipeline 调用的是 `generate_information_objects()`，其聚合键是 `normalized_title(title)`。这意味着：",
        "",
        "- 同一事件只要标题改写，就会漏合并。",
        "- 不同事件只要标题模板相同，就会误合并。",
        "- digest / roundup / market wrap 这类非事件也会被创建为事件。",
        "- 事件类型、摘要、增量价值没有真实推断，只是占位字段。",
        "",
        "### 2. 当前 DB 信号",
        "",
        "```json",
        json.dumps(db_stats, ensure_ascii=False, indent=2),
        "```",
        "",
        "默认大库提供了更接近真实使用的信号：source/item 数量足够，但历史 legacy cluster、embedding cluster、当前 operational cluster 三套形态混在一起，且大量 cluster 缺少可解释的 `cluster_items` 链接。因此它能说明当前路径和数据债务，但不能直接作为人工标注准确率。",
        "",
        "大库额外观察:",
        "",
        "- item 去重已经在写入阶段折叠重复：`seen_count > 1` 的 item 很多，但 `dedupe_groups` 为空，后置去重阶段没有解释重复来源。",
        "- legacy cluster 数量多，但多数没有 `cluster_items`，只能看摘要，不能追溯每条证据。",
        "- operational lightweight cluster 几乎都是单成员；多成员样例主要来自完全标题一致，容易被低质泛标题污染。",
        "- signature scan 显示只有一部分 item 能形成可用事件签名，说明事件聚合前必须先做 eventness 和 alias/normalization。",
        "",
        "### 3. semantic 模块自身的能力与不足",
        "",
        "semantic candidate scorer 明显比完全标题更接近真实需求：它考虑 actor/product/action/time/source diversity/generic overlap。但本轮合成测试显示它还不能直接作为最终答案：",
        "",
        f"- 根因计数: `{signature_summary['reason_counts']}`",
        "- 对 OpenAI GPT-5.5 这类标题，产品抽取常把 `OpenAI launches GPT`、`OpenAI GPT 5.5`、`GPT-5.5` 视作不同产品，导致同事件漏合。",
        "- 对 DeepSeek V4.1 这类中英文混写，中文别名和产品版本标准化不足。",
        "- 对政策类事件，`EU` / `European Commission` 与 `AI Act` 的 actor/product/action 表达不稳定。",
        "- signature 精确匹配偏保守，适合作为高精度 seed，不适合作为唯一聚合依据。",
        "",
        "signature/candidate 失败样例:",
        "",
        "```json",
        json.dumps(signature_summary["examples"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## 当前不足",
        "",
        "1. 事件定义层缺失：没有先判断 item 是否是事件。",
        "2. 事件身份层过弱：lightweight 只有标题；semantic 有 signature，但没有接入 console。",
        "3. 同事件关系层缺少分级：duplicate、near_duplicate、same_event_new_info、same_topic_different_event 应分开。",
        "4. 聚合决策缺少负特征：generic title、digest、wide time window、same source boilerplate 应强力降权。",
        "5. 事件对象质量不足：event_type、summary、importance、confidence、evidence 目前无法承载简报。",
        "6. 去重和聚合边界不清：URL/GUID/title-date 是 item 去重；same-event 是事件聚合；现在报告层没有解释这两者的关系。",
        "",
        "## 深入改进方向",
        "",
        "### Phase 1: 先修 console 接入和规则基线",
        "",
        "- 把 `generate_information_objects()` 拆成 `classify_item_eventness -> build_event_signature -> candidate_pairs -> decide_relation -> materialize_event_cluster`。",
        "- digest/newsletter/roundup/market wrap/tutorial/opinion 默认不建 event，进入 topic 或 review。",
        "- item 去重补 `http/https` 可配置 canonicalization，并在 dedupe stage 展示 `seen_count` 与重复来源。",
        "- lightweight cluster 不再用完全标题，至少使用 actor/product/action/date bucket + title token overlap。",
        "",
        "### Phase 2: 使用 semantic 模块做候选召回",
        "",
        "- 接入 `extract_event_signature()` 和 `assess_candidate()` 作为候选生成器。",
        "- signature exact 作为高精度 seed；candidate medium 进入 review；candidate high 自动合并。",
        "- 建立 alias map：OpenAI GPT-5.5/GPT 5.5/GPT-5.5、DeepSeek/深度求索、EU/European Commission 等。",
        "- 对 generic title 和 digest title 加 hard negative 规则。",
        "",
        "### Phase 3: 引入 LLM 或真实 API 做困难 pair 裁决",
        "",
        "- 只对 high-uncertain/medium pair 调 LLM，输入是结构化 signature、证据、负特征，而不是全文乱扔。",
        "- LLM 输出必须包含 relation_type、same_event、new_facts、disqualifiers、confidence。",
        "- 低风险策略：自动合并只允许 high confidence same_event；其余进 review_queue。",
        "",
        "### Phase 4: 事件对象和简报质量",
        "",
        "- event_type 最小集合：release、funding、policy、partnership、earnings、security、benchmark、market、digest_non_event。",
        "- event_summary 必须包含主体、动作、对象、时间、来源数量、增量事实。",
        "- briefing/report 从 event cluster card 生成，而不是直接列 event title 和 opaque review id。",
        "",
        "## 建议质量门",
        "",
        "- same-event pair F1 >= 0.80，recall >= 0.75。",
        "- generic/digest false positive rate <= 2%。",
        "- eventness precision >= 0.90。",
        "- event_type known rate >= 0.80。",
        "- auto-merge precision >= 0.95；auto-merge recall 可以先低，召回交给 review。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    items = build_quality_items()
    decisions, metrics = diagnose_pairs(items)
    db_stats = current_db_stats()
    report = render_report(decisions, metrics, db_stats)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(json.dumps({"report_path": str(REPORT_PATH), "metrics": metrics}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
