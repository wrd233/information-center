from __future__ import annotations

import math

from app.config import settings
from app.embedding import embed_text
from app.models import ClusteringResult, NormalizedContent, ScreeningResult
from app.screener import summarize_increment
from app.storage import InboxStore
from app.utils import truncate


def cluster_content(
    store: InboxStore,
    item_id: str,
    normalized: NormalizedContent,
    screening: ScreeningResult,
) -> ClusteringResult:
    if not settings.clustering.get("enabled", True):
        return ClusteringResult(
            cluster_relation="disabled",
            notification_decision="manual_review",
            clustering_status="disabled",
        )
    if not should_cluster(screening):
        return ClusteringResult(
            cluster_relation="skipped_low_value",
            notification_decision="silent",
            clustering_status="skipped",
        )

    embedding_text = build_embedding_text(normalized, screening)
    try:
        vector = embed_text(embedding_text)
        store.archive_stale_clusters()
        matches = store.search_active_clusters(vector, int(settings.clustering.get("top_k", 5)))
    except Exception as exc:
        return ClusteringResult(
            cluster_relation="embedding_failed",
            notification_decision="manual_review",
            embedding_text=embedding_text,
            embedding_model=settings.embedding.get("model"),
            clustering_status="failed",
            error=str(exc),
        )

    best = matches[0] if matches else None
    if not best or best["similarity"] < float(settings.clustering.get("new_event_threshold", 0.85)):
        cluster = store.create_cluster(
            title=cluster_title(normalized, screening),
            summary=screening.summary,
            entities=screening.entities,
            representative_item_id=item_id,
            vector=vector,
            embedding_model=settings.embedding.get("model"),
        )
        return ClusteringResult(
            cluster_id=cluster["cluster_id"],
            cluster_title=cluster["cluster_title"],
            cluster_relation="new_event",
            max_similarity=best["similarity"] if best else None,
            entity_overlap_ratio=0.0,
            notification_decision="full_push",
            incremental_summary="",
            embedding_text=embedding_text,
            embedding_model=settings.embedding.get("model"),
            clustering_status="ok",
        )

    overlap = entity_overlap_ratio(screening.entities, best["entities"])
    duplicate_threshold = float(settings.clustering.get("duplicate_threshold", 0.97))
    high_overlap = float(settings.clustering.get("high_overlap_entity_ratio", 0.6))

    if best["similarity"] >= duplicate_threshold and overlap >= high_overlap:
        store.update_cluster(best["cluster_id"], screening.entities)
        return ClusteringResult(
            cluster_id=best["cluster_id"],
            cluster_title=best["cluster_title"],
            cluster_relation="duplicate",
            max_similarity=best["similarity"],
            entity_overlap_ratio=overlap,
            notification_decision="silent",
            incremental_summary="",
            embedding_text=embedding_text,
            embedding_model=settings.embedding.get("model"),
            clustering_status="ok",
        )

    if best["similarity"] >= duplicate_threshold and overlap < high_overlap:
        relation = "uncertain" if settings.notification.get("manual_review_when_uncertain", True) else "incremental_update"
        decision = "manual_review" if relation == "uncertain" else "incremental_push"
        store.update_cluster(best["cluster_id"], screening.entities)
        return ClusteringResult(
            cluster_id=best["cluster_id"],
            cluster_title=best["cluster_title"],
            cluster_relation=relation,
            max_similarity=best["similarity"],
            entity_overlap_ratio=overlap,
            notification_decision=decision,
            incremental_summary="高相似但实体重合度不足，避免静默误判。",
            embedding_text=embedding_text,
            embedding_model=settings.embedding.get("model"),
            clustering_status="ok",
        )

    return handle_incremental(store, item_id, normalized, screening, best, vector, embedding_text, overlap)


def should_cluster(screening: ScreeningResult) -> bool:
    return (
        screening.screening_status == "ok"
        and screening.value_score >= int(settings.clustering.get("cluster_min_value_score", 3))
        and screening.personal_relevance
        >= int(settings.clustering.get("cluster_min_personal_relevance", 3))
    )


def build_embedding_text(normalized: NormalizedContent, screening: ScreeningResult) -> str:
    return "\n".join(
        [
            f"标题：{normalized.title}",
            f"摘要：{screening.summary}",
            f"核心实体：{', '.join(screening.entities)}",
            f"事件描述：{screening.event_hint}",
            f"来源分类：{normalized.source_category or ''}",
            f"内容类型：{normalized.content_type}",
        ]
    )


def cluster_title(normalized: NormalizedContent, screening: ScreeningResult) -> str:
    return truncate(screening.event_hint or screening.summary or normalized.title, 120) or normalized.title


def handle_incremental(
    store: InboxStore,
    item_id: str,
    normalized: NormalizedContent,
    screening: ScreeningResult,
    best: dict,
    vector: list[float],
    embedding_text: str,
    overlap: float,
) -> ClusteringResult:
    notification = "incremental_push"
    incremental_summary = ""
    updated_summary = None
    update_vector = vector_for_cluster_update(best, vector)

    try:
        increment = summarize_increment(
            cluster_title=best["cluster_title"],
            cluster_summary=best["cluster_summary"],
            new_item_title=normalized.title,
            new_item_summary=screening.summary,
            hidden_signals=screening.hidden_signals,
            entities=screening.entities,
        )
        has_value = bool(increment.get("has_incremental_value"))
        incremental_summary = increment.get("incremental_summary") or ""
        if not has_value:
            notification = "silent"
        if increment.get("should_update_cluster_summary") and increment.get("updated_cluster_summary"):
            updated_summary = increment["updated_cluster_summary"]
    except Exception:
        notification = "manual_review"

    updated = store.update_cluster(
        best["cluster_id"],
        screening.entities,
        cluster_summary=updated_summary,
        vector=update_vector,
        embedding_model=settings.embedding.get("model") if update_vector else None,
    )
    return ClusteringResult(
        cluster_id=updated["cluster_id"],
        cluster_title=updated["cluster_title"],
        cluster_relation="incremental_update",
        max_similarity=best["similarity"],
        entity_overlap_ratio=overlap,
        notification_decision=notification,
        incremental_summary=incremental_summary,
        embedding_text=embedding_text,
        embedding_model=settings.embedding.get("model"),
        clustering_status="ok",
    )


def vector_for_cluster_update(best: dict, new_vector: list[float]) -> list[float] | None:
    strategy = settings.clustering.get("cluster_vector_strategy", "summary_embedding")
    if strategy == "representative_item":
        return None
    if strategy == "average_items" and best.get("cluster_vector"):
        count = max(1, int(best.get("item_count", 1)))
        return [
            (old * count + new) / (count + 1)
            for old, new in zip(best["cluster_vector"], new_vector)
        ]
    return new_vector


def entity_overlap_ratio(new_entities: list[str], cluster_entities: list[str]) -> float:
    left = {normalize_entity(entity) for entity in new_entities if normalize_entity(entity)}
    right = {normalize_entity(entity) for entity in cluster_entities if normalize_entity(entity)}
    if not left or not right:
        return 0.0
    return len(left & right) / max(1, min(len(left), len(right)))


def normalize_entity(entity: str) -> str:
    return entity.strip().lower()


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)

