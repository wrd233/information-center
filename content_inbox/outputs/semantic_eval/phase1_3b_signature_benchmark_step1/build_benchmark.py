#!/usr/bin/env python3
"""Build the 50-row Event Signature Benchmark from Phase 1.3 evidence."""
import json, csv, os
from pathlib import Path
from datetime import datetime

ROUND_C = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_3_round_c_80_live_tuned")
OUTPUT = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/phase1_3b_signature_benchmark_step1")

# ── Load evidence ──────────────────────────────────────────────
def load_jsonl(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

items = {r["dry_run_item_id"]: r for r in load_jsonl(ROUND_C / "semantic_items.jsonl")}
sigs = {r["item_id"]: r for r in load_jsonl(ROUND_C / "event_signatures.jsonl")}
cards = {r["item_id"]: r for r in load_jsonl(ROUND_C / "item_cards.jsonl")}

rels_by_pair = {}
for r in load_jsonl(ROUND_C / "relations_interesting.jsonl"):
    key = (r.get("item_a_id"), r.get("item_b_id"))
    rels_by_pair[key] = r

# ── Helpers ─────────────────────────────────────────────────────
def sig_summary(item_id):
    s = sigs.get(item_id, {})
    reasons = s.get("invalid_reasons", [])
    return {
        "action": s.get("action", ""),
        "actor": s.get("actor", ""),
        "product": s.get("product_or_model", ""),
        "object": s.get("object", ""),
        "concreteness": s.get("concreteness_score", 0),
        "is_concrete": s.get("is_concrete", False),
        "signature_key": s.get("signature_key"),
        "invalid_reasons": reasons,
    }

def item_meta(item_id):
    it = items.get(item_id, {})
    return {
        "source_name": it.get("source_name", ""),
        "published_at": it.get("published_at", ""),
        "title": it.get("title", ""),
        "url": it.get("url", ""),
    }

def card_meta(item_id):
    c = cards.get(item_id, {})
    return {
        "short_summary": c.get("short_summary") or "",
        "content_role": c.get("content_role") or "",
        "entities": c.get("entities") or [],
        "event_hint": c.get("event_hint") or "",
    }

def rel_for(a, b):
    return rels_by_pair.get((a, b)) or rels_by_pair.get((b, a))

# ── Build benchmark rows ────────────────────────────────────────
benchmark_rows = []
seq = [0]

def bid(kind):
    seq[0] += 1
    return f"BENCH_1_3b_{kind}_{seq[0]:03d}"

def make_row(kind, item_id, candidate_item_id=None, cluster_id=None, **overrides):
    """Assemble a benchmark row with defaults from evidence + overrides."""
    si = sig_summary(item_id)
    im = item_meta(item_id)
    cm = card_meta(item_id)
    rel = rel_for(item_id, candidate_item_id) if candidate_item_id else None

    current_sig = si["signature_key"] if si["is_concrete"] and si["signature_key"] else f"REJECTED: {'; '.join(si['invalid_reasons'])}" if si["invalid_reasons"] else "NONE"

    row = {
        "benchmark_id": bid(kind),
        "kind": kind,
        "source_file_refs": ["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl"],
        "item_id": item_id,
        "candidate_item_id": candidate_item_id,
        "cluster_id": cluster_id,
        "source_name": im["source_name"],
        "candidate_source_name": item_meta(candidate_item_id)["source_name"] if candidate_item_id else None,
        "published_at": im["published_at"],
        "candidate_published_at": item_meta(candidate_item_id)["published_at"] if candidate_item_id else None,
        "title": im["title"],
        "candidate_title": item_meta(candidate_item_id)["title"] if candidate_item_id else None,
        "short_summary": cm["short_summary"],
        "candidate_short_summary": card_meta(candidate_item_id)["short_summary"] if candidate_item_id else None,
        "current_signature": current_sig,
        "current_invalid_reasons": si["invalid_reasons"],
        "current_relation": rel.get("relation_label") if rel else None,
        "current_candidate_lane": rel.get("lane") if rel else None,
        "current_candidate_priority": rel.get("candidate_priority") if rel else None,
        "recommended_label": "",
        "recommended_event_signature": None,
        "recommended_relation": None,
        "should_form_event_cluster": False,
        "should_form_thread_relation": False,
        "should_fold": False,
        "confidence": 0.0,
        "reason": "",
        "risk_notes": [],
        "human_label": "",
        "human_notes": "",
    }
    row.update(overrides)
    return row

def esig(actor, product, action, obj="", date_bucket="", confidence=0.8, is_event=True, is_thread=False):
    """Shorthand for recommended_event_signature."""
    return {
        "actor": actor,
        "product_or_model": product,
        "action": action,
        "object": obj,
        "date_bucket": date_bucket,
        "confidence": confidence,
        "is_event_like": is_event,
        "is_thread_like": is_thread,
    }

# ═══════════════════════════════════════════════════════════════════
# SECTION A: VALID EVENT SIGNATURES (6 rows — accepted but flawed)
# ═══════════════════════════════════════════════════════════════════

benchmark_rows.append(make_row("single", "item_3067df504cf4433888188c024bac275c",
    recommended_label="event_announcement",
    recommended_event_signature=esig("Snyk", "AI Security Summit", "event", "London", "2026-05-14", 0.85),
    confidence=0.85,
    reason="Current extractor got action=security (reasonable) but used 'May 14' as product instead of 'AI Security Summit'. Actor missing (should be Snyk/AI Engineer). Clear event promotion for a conference.",
    risk_notes=["Product fragment 'May 14' is a date, not a product name", "Actor should be Snyk (organizer), not AI Engineer (promoter)"],
))

benchmark_rows.append(make_row("single", "item_9353d0480b5d4303bb2e9d8bb3983f5a",
    recommended_label="integration_or_tooling",
    recommended_event_signature=esig("NVIDIA", "OpenShell v0.0.40", "release", "k8s scheduling + TLS security fixes", "2026-05-13", 0.9),
    confidence=0.9,
    reason="Current extractor correctly identified actor=NVIDIA but classified as action=security with product=k8s. Actual event is a versioned software release (OpenShell v0.0.40) with multiple features.",
    risk_notes=["'k8s' is a feature domain, not the product", "Action should be 'release', not 'security'"],
))

benchmark_rows.append(make_row("single", "item_336cf2f457b647ff8a59fdd5d590c528",
    recommended_label="company_or_funding",
    recommended_event_signature=esig("Recursive", "Recursive Superintelligence", "company_launch", "", "2026-05-14", 0.9),
    confidence=0.9,
    reason="Current extractor got action=launch (correct category) but actor=Meta (wrong — Tian Yuandong left Meta to found Recursive) and product='Our 25' (gibberish from tokenization).",
    risk_notes=["Actor 'Meta' is the former employer, not the company being launched", "'Our 25' is a random token fragment"],
))

benchmark_rows.append(make_row("single", "item_6ec5265251ab401284ced9735bc9d28d",
    recommended_label="technical_blog",
    recommended_event_signature=esig("NVIDIA", "DGX Spark + Hermes Agent", "case_study", "121B model local testing", "2026-05-13", 0.65),
    confidence=0.6,
    reason="Accepted by current extractor as feature_update but product='for updates from my phone. hermes agent' is a garbled phrase fragment. This is a firsthand account of local model testing — more anecdote than event.",
    risk_notes=["Borderline event-like; this is a social anecdote, not a product announcement", "Product tokenization is catastrophically wrong"],
))

benchmark_rows.append(make_row("single", "item_ce3cfb151a984123a49a53b5d7a4db4b",
    recommended_label="company_or_funding",
    recommended_event_signature=esig("PLAN0", "PLAN0", "company_launch", "construction cost estimation", "2026-05-14", 0.85),
    confidence=0.85,
    reason="Current extractor got action=launch and product=PLAN0 mostly correct, but actor is empty. This is a Y Combinator launch announcement — the actor should be PLAN0.",
    risk_notes=["Actor missing despite being obvious from product name"],
))

benchmark_rows.append(make_row("single", "item_1e1fb9374a9e4d4a88e2e09a9516f736",
    recommended_label="low_signal_social",
    recommended_event_signature=None,
    confidence=0.9,
    reason="Accepted as action=funding but product is a 69-character phrase 'coordinated opposition campaigns around our Utah projects'. Title is just 'Concerning.' This is a low-context social media reaction, not a fundable event signature. Should be REJECTED.",
    risk_notes=["Product phrase is absurdly long — should be rejected", "Title 'Concerning.' provides zero semantic signal", "This is a false positive acceptance — extractor should have rejected"],
))

# ═══════════════════════════════════════════════════════════════════
# SECTION B: SINGLE FAILURE — missing_concrete_event_action (10 rows)
# ═══════════════════════════════════════════════════════════════════

benchmark_rows.append(make_row("single", "item_a5427d9ae1a34bbebcce09738422f478",
    recommended_label="event_announcement",
    recommended_event_signature=esig("Google", "Googlebook", "release", "Gemini-powered AI Laptop platform", "2026-05-12", 0.9),
    confidence=0.9,
    reason="Clear product launch (Googlebook AI laptop platform). Actor=Google identified correctly. Action=other despite explicit launch language ('Google 刚刚发布了一个新东西'). Action regex failed on Chinese text.",
    risk_notes=["Chinese-language content — action detection likely English-only"],
))

benchmark_rows.append(make_row("single", "item_4e57b89e89224128951f7fd22403b804",
    recommended_label="adoption_metric",
    recommended_event_signature=esig("NVIDIA", "NVDA", "adoption_metric", "$5.5T market cap milestone", "2026-05-13", 0.85),
    confidence=0.85,
    reason="Clear milestone event: NVIDIA hits $5.5T market cap. Actor=Nvidia identified correctly. Concreteness 0.48. Action=other despite explicit 'became the first company to hit' language.",
    risk_notes=["Market cap milestone is a valid event type not in action taxonomy"],
))

benchmark_rows.append(make_row("single", "item_f14c5d1af066457dbc050b797452ddcb",
    recommended_label="adoption_metric",
    recommended_event_signature=esig("Anthropic", "Claude", "adoption_metric", "34.4% enterprise share surpasses OpenAI", "2026-05-13", 0.85),
    confidence=0.85,
    reason="Clear adoption data: Anthropic surpassed OpenAI in enterprise subscriptions. Concreteness 0.8. Actor=Anthropic identified. Action=other despite clear 'surpassed' language. Ramp AI Index data.",
    risk_notes=["Product='just 0.3' is a number fragment from tokenization"],
))

benchmark_rows.append(make_row("single", "item_eaf6591ef88f4dc58f0b86678ab3d50d",
    recommended_label="integration_or_tooling",
    recommended_event_signature=esig("Notion", "Notion CLI", "release", "command-line interface for developers", "2026-05-13", 0.9),
    confidence=0.9,
    reason="Clear product launch: Notion CLI. Actor=Notion correctly identified. Concreteness 0.8. Product='made just for developers and coding agents' is a phrase fragment — should be 'Notion CLI'.",
    risk_notes=["Product is a descriptive phrase, not the product name"],
))

benchmark_rows.append(make_row("single", "item_882a0697c88d44f99a3e9cb0f21d2e7a",
    recommended_label="feature_update",
    recommended_event_signature=esig("Notion", "Notion Custom Agents", "feature_update", "agent tools via Workers", "2026-05-13", 0.85),
    confidence=0.85,
    reason="Feature update: Notion Custom Agents now support arbitrary tools via Workers. Actor missing. Product='Give your Custom Agents' is a verb phrase fragment.",
    risk_notes=["Related to Notion CLI launch (item_17) — same product ecosystem, different feature"],
))

benchmark_rows.append(make_row("single", "item_4d5823911a8c47cb86a7c722e3b8d5ec",
    recommended_label="technical_blog",
    recommended_event_signature=esig("OpenAI", "Codex for Windows", "technical_blog", "sandbox implementation deep-dive", "2026-05-14", 0.85),
    confidence=0.85,
    reason="Technical blog about Codex Windows sandbox by David Wiesen. Actor=OpenAI correctly identified. Concreteness 0.8. Action=other despite being an engineering deep-dive.",
    risk_notes=["Product='exit 1' and object='Part 1' are tokenization artifacts"],
))

benchmark_rows.append(make_row("single", "item_be5611f94b884954915804fa926518db",
    recommended_label="feature_update",
    recommended_event_signature=esig("OpenAI/Codex", "Codex Remote Control", "feature_update", "ChatGPT mobile remote control", "2026-05-15", 0.8),
    confidence=0.8,
    reason="Feature update: Codex now supports remote control via ChatGPT on mobile. Actor=Codex (identified as organization — debatable). Concreteness 0.48.",
    risk_notes=["Codex is a product, not an organization — actor classification issue"],
))

benchmark_rows.append(make_row("single", "item_5c8c1a4e54154b6288894a68bd3cfce7",
    recommended_label="integration_or_tooling",
    recommended_event_signature=esig("QVeris", "QVeris CLI", "integration", "Claude Code financial analysis integration", "2026-05-15", 0.8),
    confidence=0.8,
    reason="Integration announcement: QVeris CLI connects financial data to Claude Code. Actor='Claude' (wrong — should be QVeris). Product='Claude Code' is the integration target, not the product.",
    risk_notes=["Actor/product confusion: Claude Code is the platform being integrated with, not the actor"],
))

benchmark_rows.append(make_row("single", "item_d28c9c5b374a46f3a9a81902384e1ec3",
    recommended_label="integration_or_tooling",
    recommended_event_signature=esig("NVIDIA", "OpenShell v0.0.41", "release", "agent-driven policy + sandbox flags", "2026-05-14", 0.9),
    confidence=0.9,
    reason="Versioned release: OpenShell v0.0.41. Actor=NVIDIA identified. Rejected despite clear product+version in title. Same pattern as v0.0.40 which was accepted as security — inconsistency.",
    risk_notes=["Inconsistent with v0.0.40 which was accepted", "Product='U4n62' is a URL fragment"],
))

# 10th single-failure item: LangChain Interrupt event announcement
benchmark_rows.append(make_row("single", "item_b51cf0ea11be433e86cc0ba1302676f7",
    recommended_label="event_announcement",
    recommended_event_signature=esig("LangChain", "LangChain Interrupt", "event", "agent conference with Andrew Ng", "2026-05-14", 0.8),
    confidence=0.8,
    reason="Conference/event announcement: LangChain Interrupt featuring Andrew Ng and Harrison Chase. Concreteness 0.5. Single-failure (missing_concrete_event_action). Product='conversation on the future of agents' is a descriptive phrase, not event name.",
    risk_notes=["Event name 'Interrupt' was not extracted — product is a descriptive phrase"],
))

# Section B has exactly 10 items above. Moving to section C.

# ═══════════════════════════════════════════════════════════════════
# SECTION C: TRIPLE-FAILURE LOW-SIGNAL (9 rows)
# ═══════════════════════════════════════════════════════════════════

benchmark_rows.append(make_row("single", "item_2e8748de572e4ee38e1aa1186dad65fe",
    recommended_label="generic_opinion",
    recommended_event_signature=None,
    confidence=0.95,
    reason="Title is just 'Great advice'. Pure social engagement bait with no concrete product, actor, or event. Triple-failure is correct — this should not produce an event signature.",
    risk_notes=["Classic example of low-signal social media content that should be filtered"],
))

benchmark_rows.append(make_row("single", "item_0be43f87ff76474aadee26a8741e9e31",
    recommended_label="generic_opinion",
    recommended_event_signature=None,
    confidence=0.95,
    reason="Title is 'Banger'. One-word social engagement post with zero event content. Triple-failure correctly rejects this.",
    risk_notes=["Shows that very short social posts are fundamentally un-extractable"],
))

benchmark_rows.append(make_row("single", "item_063c93ebca06426ea4816cba64452dcc",
    recommended_label="generic_opinion",
    recommended_event_signature=None,
    confidence=0.9,
    reason="Chinese podcast commentary about LLMs — philosophical opinion with no concrete event. 'LLM development is too simple now, no individual heroism'. Triple-failure is correct.",
    risk_notes=["Chinese-language content amplifies extraction difficulty", "Opinion content is inherently non-event-like"],
))

benchmark_rows.append(make_row("single", "item_911c3b9116e04d97b5a35e54fefad8f4",
    recommended_label="generic_opinion",
    recommended_event_signature=None,
    confidence=0.9,
    reason="Chinese startup advice: 'follow your heart, follow your money'. Purely opinion/advice with no concrete product or event. Triple-failure correct.",
    risk_notes=[],
))

benchmark_rows.append(make_row("single", "item_3445b70e409c4853a19117c27dfacd13",
    recommended_label="generic_opinion",
    recommended_event_signature=None,
    confidence=0.9,
    reason="Philosophical commentary on human decision-making and 'skin in the game'. No concrete event. Triple-failure correct.",
    risk_notes=["'skin in the game' is a book/concept reference, not an event"],
))

benchmark_rows.append(make_row("single", "item_53862d15553c47ee9f4cb443e1c3596a",
    recommended_label="low_signal_social",
    recommended_event_signature=None,
    confidence=0.95,
    reason="Three-word social reply: '@xeophon @arcee_ai Open > closed'. Zero event content. Triple-failure correct. This is a social media reply, not content.",
    risk_notes=["Extremely short content — should be filtered at ingest, not extraction"],
))

benchmark_rows.append(make_row("single", "item_ab429ffdddcd425ca8285f4af013053c",
    recommended_label="generic_opinion",
    recommended_event_signature=None,
    confidence=0.9,
    reason="Taleb book quotes shared as social content. Literary excerpt with no event. Triple-failure correct.",
    risk_notes=["Book quotes are content but not events", "Author name 'Taleb' is detected but not as an event actor"],
))

benchmark_rows.append(make_row("single", "item_42a84c1583c343c3a04d68b0ee94df93",
    recommended_label="pricing_or_availability",
    recommended_event_signature=esig("China Telecom Shanghai", "Token calling plan", "pricing", "1 RMB per 250K tokens", "2026-05-16", 0.7),
    confidence=0.7,
    reason="MISCLASSIFIED AS TRIPLE-FAILURE. This is a real pricing event: China Telecom Shanghai launched token bundles as phone plan add-ons (1 RMB = 250K tokens). The Chinese text obscured the concrete event from the extractor.",
    risk_notes=["False negative — this IS an event", "Chinese-language pricing announcement completely missed by extractor"],
))

benchmark_rows.append(make_row("single", "item_51c09adf4af64e48b4e1a03e8b6dcc54",
    recommended_label="event_announcement",
    recommended_event_signature=esig("NVIDIA", "Stelline Developer Kit", "availability", "shipping to developers", "2026-05-15", 0.65),
    confidence=0.6,
    reason="MISCLASSIFIED AS TRIPLE-FAILURE. This is about Stelline Developer Kit shipping. Title is cryptic ('If Luigi knows you...') but card entities show 'Stelline Developer Kit, DGX Spark'. Real hardware availability event.",
    risk_notes=["Title is social-media-cryptic, hiding the real content", "Card entities correctly identified the product"],
))

# ═══════════════════════════════════════════════════════════════════
# SECTION D: BORDERLINE / INTERESTING EDGE CASES (8 rows)
# ═══════════════════════════════════════════════════════════════════

benchmark_rows.append(make_row("single", "item_a67b5ac224504c52b56f8f15fe7645d4",
    recommended_label="event_announcement",
    recommended_event_signature=esig("GitHub", "GitHub Copilot Desktop", "availability", "technical preview, waitlist", "2026-05-15", 0.8),
    confidence=0.8,
    reason="Borderline case: action=availability detected with no invalid reasons, but signature_key=None (neither accepted nor rejected). This is a real product preview announcement that fell through the cracks.",
    risk_notes=["0 invalid reasons but no signature produced — pipeline gap", "Actor should be GitHub, not Codex (extractor confused by comparison in text)"],
))

benchmark_rows.append(make_row("single", "item_eb506e3260be4c39adc3b040340afb3b",
    recommended_label="pricing_or_availability",
    recommended_event_signature=esig("LangChain", "LangSmith Fleet", "pricing", "free tier via Fireworks AI", "2026-05-14", 0.7),
    confidence=0.7,
    reason="MISCLASSIFIED AS TRIPLE-FAILURE. Clear pricing/availability change: LangSmith Fleet now has a free model tier. Triple-failure despite concrete product name and pricing action.",
    risk_notes=["False negative — 'free model' is a clear pricing signal", "Product name 'LangSmith Fleet' should have been extractable"],
))

benchmark_rows.append(make_row("single", "item_5796c79cfcca466db647657e5a79484d",
    recommended_label="pricing_or_availability",
    recommended_event_signature=esig("LangChain", "LangSmith Fleet", "pricing", "free LLMs and sandboxes", "2026-05-14", 0.7),
    confidence=0.7,
    reason="Follow-up post to item_44 about free tier. Concreteness 0.8 but only missing_concrete_event_action (not triple). Actor=langchain (lowercase). Shows single-failure mode on a real event.",
    risk_notes=["Related to item_44 — same event, different post style", "Actor normalization: 'langchain' vs 'LangChain'"],
))

benchmark_rows.append(make_row("single", "item_7f5662046d694a2d87dc541de9e41a45",
    recommended_label="company_or_funding",
    recommended_event_signature=esig("Adialante", "Adialante mobile MRI", "company_launch", "accessible cancer screening", "2026-05-13", 0.75),
    confidence=0.75,
    reason="Rejected with only missing_concrete_actor_or_product despite being a YC launch (action=launch detected). Other YC launches (Modern, PLAN0, YouArt) were accepted. Shows inconsistency in YC launch extraction.",
    risk_notes=["Inconsistent with other YC launches that were accepted", "Action=launch was detected correctly but actor missing"],
))

benchmark_rows.append(make_row("single", "item_6765a19f703848cd8351b76a76a66d91",
    recommended_label="generic_opinion",
    recommended_event_signature=None,
    confidence=0.8,
    reason="Chinese tweet about switching translation tools. Has concrete product names (DeepSeek V4 Flash, 陪读蛙) but is a personal workflow share, not an event. Single-failure with concreteness 0.48, but correctly rejected — there is no event here, just someone sharing their tool setup.",
    risk_notes=["Personal tool setup share — thread-like, not event-like", "Has concrete product names but no event action", "Correctly rejected despite having concrete entities"],
))

benchmark_rows.append(make_row("single", "item_309eddf5864848da94e8fa49608ead78",
    recommended_label="integration_or_tooling",
    recommended_event_signature=esig("Notion", "Notion CLI + Developer Platform", "release", "CLI, Workers, Agent tools, Webhooks", "2026-05-16", 0.8),
    confidence=0.8,
    reason="Third-party commentary on Notion CLI from orange.ai. Concreteness 0.8. Single-failure. This is a summary/endorsement of the Notion developer platform launch. Different from the official Notion announcement but contains same event info.",
    risk_notes=["Third-party restatement of an event, not original source", "Rich card entities capture the full platform scope"],
))

benchmark_rows.append(make_row("single", "item_10d47a60c33d4553b036a1a8fa6a02b7",
    recommended_label="integration_or_tooling",
    recommended_event_signature=esig("Notion", "Notion Agent Tools (Workers)", "feature_update", "custom agent capabilities via Workers", "2026-05-13", 0.85),
    confidence=0.85,
    reason="Notion Workers/Custom Agents feature announcement. Concreteness 0.8. Single-failure. Clear feature launch with detailed technical description. Product='Tools give your Custom Agents' is a sentence fragment.",
    risk_notes=["Related to Notion CLI and Workers posts — same launch event series"],
))

benchmark_rows.append(make_row("single", "item_a3ecca2a219e4d7b89c51bdee8157c0d",
    recommended_label="event_announcement",
    recommended_event_signature=esig("NVIDIA", "Nemotron 3 Nano Omni", "event", "Ask the Experts webinar", "2026-05-12", 0.75),
    confidence=0.75,
    reason="Webinar/livestream announcement for Nemotron 3 Nano Omni. Product identified as 'Nemotron 3'. Concreteness 0.5. Single-failure. 'Ask the Experts' is an event format, not detected as an event action.",
    risk_notes=["Webinar format not in action taxonomy", "Product correctly identified despite rejection"],
))

# ═══════════════════════════════════════════════════════════════════
# SECTION E: PAIR ROWS (15 rows)
# ═══════════════════════════════════════════════════════════════════

# E1 — near_duplicate
benchmark_rows.append(make_row("pair", "item_f14c5d1af066457dbc050b797452ddcb", "item_0bc73c59c550408d8e9b09a873d607e4",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="adoption_metric",
    recommended_event_signature=esig("Anthropic", "Claude", "adoption_metric", "enterprise share surpasses OpenAI (Ramp AI Index)", "2026-05-13", 0.9),
    recommended_relation="near_duplicate",
    should_form_event_cluster=False,
    should_form_thread_relation=False,
    should_fold=True,
    confidence=0.95,
    reason="Clear near-duplicate: The Rundown AI (English) and AI Will (Chinese) report the same Ramp AI Index data. System correctly identified relation_label=near_duplicate, should_fold=True. Both items should fold into one event signature.",
    risk_notes=["Cross-language duplicate detection works correctly here", "Good example of should_fold=True"],
))

# E2 — same_product_different_event (Codex)
benchmark_rows.append(make_row("pair", "item_be5611f94b884954915804fa926518db", "item_4d5823911a8c47cb86a7c722e3b8d5ec",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="same_product_different_event",
    recommended_event_signature=esig("OpenAI", "Codex", "feature_update", "remote control + Windows sandbox", "2026-05-14", 0.85),
    recommended_relation="same_product_different_event",
    should_form_event_cluster=False,
    should_form_thread_relation=True,
    should_fold=False,
    confidence=0.9,
    reason="Both about OpenAI Codex but different events: (A) remote control via ChatGPT mobile, (B) Windows sandbox implementation. System correctly identified same_product_different_event. Good example for thread-like relation.",
    risk_notes=["These should form a thread (same product, different features), not a cluster"],
))

# E3 — suspicious_different with high score: AK paper posts (should be same_thread)
benchmark_rows.append(make_row("pair", "item_b86f4bea90924975a2f1aef786aff460", "item_6425c9a49e3544649568bd7036bfcdb8",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="research_paper",
    recommended_event_signature=esig("", "HuggingFace papers", "research_paper", "", "2026-05-13", 0.5),
    recommended_relation="same_thread",
    should_form_event_cluster=False,
    should_form_thread_relation=True,
    should_fold=False,
    confidence=0.7,
    reason="Two different paper announcements from same source (AK@_akhaliq), both 'paper:' format. Candidate score 4.15 (highest non-duplicate). System said suspicious_different but these are same-source, same-format, same-action (paper). Should form a thread.",
    risk_notes=["URL fragments as product names ('fkR2wVD129', 'nRjIqRD2fg') — meaningless", "Same source + same format + same action = should be thread, not different"],
))

# E4 — suspicious_different: QVeris CLI vs Rundown roundup (correctly different)
benchmark_rows.append(make_row("pair", "item_5c8c1a4e54154b6288894a68bd3cfce7", "item_8a1c922a42aa475695ac012267fb87da",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="different_pair",
    recommended_event_signature=esig("QVeris", "QVeris CLI", "integration", "", "2026-05-15", 0.8),
    recommended_relation="different",
    should_form_event_cluster=False,
    should_form_thread_relation=False,
    should_fold=False,
    confidence=0.9,
    reason="False positive pair: QVeris CLI integration vs. AI news roundup that mentions Claude Code. Shared entity 'Claude Code' triggered high candidate score (4.103) but the items are unrelated. System correctly labeled suspicious_different.",
    risk_notes=["Shared entity 'Claude Code' causes false positive candidate generation", "Demonstrates need for deeper entity role understanding"],
))

# E5 — suspicious_different: PLAN0 vs Modern (same source, different products)
benchmark_rows.append(make_row("pair", "item_ce3cfb151a984123a49a53b5d7a4db4b", "item_56610f563a81415c9ed9aac9437f6ae0",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="same_product_different_event",
    recommended_event_signature=esig("Y Combinator", "YC Launches", "company_launch", "", "2026-05-14", 0.8),
    recommended_relation="same_product_different_event",
    should_form_event_cluster=False,
    should_form_thread_relation=False,
    should_fold=False,
    confidence=0.85,
    reason="Both Y Combinator launch announcements (PLAN0 and Modern) from same source, same day, same format. Candidate score 4.05. System said suspicious_different which is reasonable but same_product_different_event (product=YC launches) is more precise.",
    risk_notes=["Same source + same action (launch) + same format = borderline same_thread vs different", "YC itself is the common actor, not the launched companies"],
))

# E6 — Notion CLI vs Notion Workers (same source, related features)
benchmark_rows.append(make_row("pair", "item_eaf6591ef88f4dc58f0b86678ab3d50d", "item_a40e531db76a4d5f8043ffc79c127012",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="same_product_different_event",
    recommended_event_signature=esig("Notion", "Notion Developer Platform", "release", "CLI + Workers", "2026-05-13", 0.9),
    recommended_relation="same_product_different_event",
    should_form_event_cluster=False,
    should_form_thread_relation=True,
    should_fold=False,
    confidence=0.9,
    reason="Two Notion developer platform announcements from same source, same timestamp: (A) Notion CLI, (B) Notion Workers. Same launch event series, different specific features. Should form a thread.",
    risk_notes=["Same timestamp suggests coordinated launch — should be same_event with new_info", "Candidate title is just a URL (item_18 has title='https://t.co/BzgPmLV2qC')"],
))

# E7 — OpenShell v0.0.40 vs v0.0.41 (versioned releases)
benchmark_rows.append(make_row("pair", "item_9353d0480b5d4303bb2e9d8bb3983f5a", "item_d28c9c5b374a46f3a9a81902384e1ec3",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="related_with_new_info_candidate",
    recommended_event_signature=esig("NVIDIA", "OpenShell", "release", "v0.0.40 → v0.0.41", "2026-05-14", 0.9),
    recommended_relation="related_with_new_info",
    should_form_event_cluster=True,
    should_form_thread_relation=False,
    should_fold=False,
    confidence=0.85,
    reason="Two consecutive OpenShell releases. v0.0.40 (May 13) was accepted as security, v0.0.41 (May 14) was rejected. These should form an event cluster — same product, sequential releases.",
    risk_notes=["v0.0.40 accepted, v0.0.41 rejected — pipeline inconsistency", "These were NOT paired in relations_interesting — discovered manually"],
))

# E8 — NVIDIA agentic inference + follow-up link (near_duplicate)
benchmark_rows.append(make_row("pair", "item_9bc2bafe3e5b41569d4934c32a5e57d3", "item_d4b0d3eedde34c4d9de88af320b3643e",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl"],
    recommended_label="near_duplicate_candidate",
    recommended_event_signature=esig("NVIDIA", "agentic inference platform", "technical_blog", "", "2026-05-13", 0.6),
    recommended_relation="near_duplicate",
    should_form_event_cluster=False,
    should_form_thread_relation=False,
    should_fold=True,
    confidence=0.9,
    reason="Item 25 is a long post about NVIDIA agentic inference; item 26 is the 'Read more' link follow-up (same timestamp +1s). Clear near-duplicate: the second is just a pointer to the full article.",
    risk_notes=["Link-only follow-up post should be folded into the main post", "Same source, same timestamp pattern"],
))

# E9 — Codex remote control vs Codex sandbox (same_product_different_event — different pair than E2)
# Already covered by E2. Let me pick a different interesting pair.
# E9 — Anthropic adoption (Rundown) vs Anthropic Mythos debate (Gary Marcus)
benchmark_rows.append(make_row("pair", "item_f14c5d1af066457dbc050b797452ddcb", "item_d7354e98712e42d7bccc4800eb1ec1b3",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="same_thread",
    recommended_event_signature=esig("Anthropic", "Anthropic", "adoption_metric", "", "2026-05-13", 0.7),
    recommended_relation="same_thread",
    should_form_event_cluster=False,
    should_form_thread_relation=True,
    should_fold=False,
    confidence=0.8,
    reason="Both about Anthropic but different aspects: (A) enterprise adoption data, (B) Mythos rollout debate. Candidate score 1.572. System said suspicious_different which is mostly right, but same_thread captures the shared Anthropic topic better.",
    risk_notes=["Same company, different sub-topics — thread-like but not same event"],
))

# E10 — Recursive launch vs NVIDIA agentic inference (different)
benchmark_rows.append(make_row("pair", "item_336cf2f457b647ff8a59fdd5d590c528", "item_9bc2bafe3e5b41569d4934c32a5e57d3",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="different_pair",
    recommended_event_signature=esig("Recursive", "Recursive SI", "company_launch", "", "2026-05-14", 0.9),
    recommended_relation="different",
    should_form_event_cluster=False,
    should_form_thread_relation=False,
    should_fold=False,
    confidence=0.95,
    reason="High-scoring false positive (3.6): Recursive startup launch vs NVIDIA agentic inference. Shared 'agentic' and 'algorithm' are generic AI terms, not event-sharing signals. System correctly labeled suspicious_different.",
    risk_notes=["Generic shared tokens ('agentic', 'algorithm') inflate candidate score", "Shows entity overlap scoring weakness with common AI vocabulary"],
))

# E11 — Two YC launches: Modern vs YouArt (same source, different products)
benchmark_rows.append(make_row("pair", "item_56610f563a81415c9ed9aac9437f6ae0", "item_cf0515fcd3a14c0d890cd7abc5f5e646",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="same_product_different_event",
    recommended_event_signature=esig("Y Combinator", "YC Launches", "company_launch", "", "2026-05-14", 0.8),
    recommended_relation="same_product_different_event",
    should_form_event_cluster=False,
    should_form_thread_relation=False,
    should_fold=False,
    confidence=0.9,
    reason="Two YC launch announcements, same source, same format. System correctly said suspicious_different. Both are company launches but for completely different companies (Modern vs YouArt).",
    risk_notes=["YC launches are a recurring format — not the same event despite same source"],
))

# E12 — Vercel AI report (vista8) vs Anthropic adoption (Rundown)
benchmark_rows.append(make_row("pair", "item_e09564532cd54167b97cbb9e5cd9258c", "item_f14c5d1af066457dbc050b797452ddcb",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="same_thread",
    recommended_event_signature=esig("Anthropic", "Claude", "adoption_metric", "", "2026-05-15", 0.6),
    recommended_relation="same_thread",
    should_form_event_cluster=False,
    should_form_thread_relation=True,
    should_fold=False,
    confidence=0.65,
    reason="Both reports involve Anthropic model usage data: (A) Vercel AI Gateway report showing Anthropic 61% spend share, (B) Ramp AI Index showing Anthropic surpassing OpenAI. Different reports, different metrics, same company. Thread-like.",
    risk_notes=["Same company, different data sources — could be same_thread or different", "Shared entity 'Anthropic' causes candidate generation but relation is ambiguous"],
))

# E13 — "Skin in the game" vs CUDA commentary (same source, same philosophical theme)
benchmark_rows.append(make_row("pair", "item_3445b70e409c4853a19117c27dfacd13", "item_3ee768f4562f49879278963ed4efaaac",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl"],
    recommended_label="low_signal_social",
    recommended_event_signature=None,
    recommended_relation="same_thread",
    should_form_event_cluster=False,
    should_form_thread_relation=True,
    should_fold=False,
    confidence=0.7,
    reason="Both orange.ai philosophical posts. High candidate score (3.6) from shared CJK text fragments. Neither item should produce an event signature — both are correctly rejected as triple-failure. But they are same_thread (same author's philosophical musings).",
    risk_notes=["CJK text fragment overlap inflates entity scores artificially", "Both items are correctly rejected — no event signature should be produced", "Thread relationship is for philosophical content, not events"],
))

# E14 — AI Security Summit vs LangChain Interrupt (both event announcements)
benchmark_rows.append(make_row("pair", "item_3067df504cf4433888188c024bac275c", "item_b51cf0ea11be433e86cc0ba1302676f7",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl"],
    recommended_label="different_pair",
    recommended_event_signature=esig("", "AI conferences", "event", "", "2026-05-14", 0.5),
    recommended_relation="different",
    should_form_event_cluster=False,
    should_form_thread_relation=False,
    should_fold=False,
    confidence=0.9,
    reason="Two different event announcements: (A) AI Security Summit London May 14 by Snyk/AI Engineer, (B) LangChain Interrupt with Andrew Ng. Both are AI events but completely different organizers, topics, and venues. Different.",
    risk_notes=["Both are 'event' type — taxonomy needs sub-types to distinguish conferences"],
))

# E15 — Notion Custom Agents vs Notion Workers (same launch series)
benchmark_rows.append(make_row("pair", "item_882a0697c88d44f99a3e9cb0f21d2e7a", "item_10d47a60c33d4553b036a1a8fa6a02b7",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl"],
    recommended_label="related_with_new_info_candidate",
    recommended_event_signature=esig("Notion", "Notion Developer Platform", "release", "Custom Agents + Agent Tools + Workers", "2026-05-13", 0.9),
    recommended_relation="related_with_new_info",
    should_form_event_cluster=True,
    should_form_thread_relation=False,
    should_fold=False,
    confidence=0.85,
    reason="Two posts from same Notion launch series: (A) Custom Agents can now use any tool, (B) Tools/Workers technical details. Same timestamp (16:27:37). These describe the same platform launch from different angles.",
    risk_notes=["Same timestamp, same source, overlapping content — should cluster", "These were NOT paired in relations_interesting — discovered manually"],
))

# ═══════════════════════════════════════════════════════════════════
# SECTION F: CLUSTER CANDIDATES (2 rows)
# ═══════════════════════════════════════════════════════════════════

benchmark_rows.append(make_row("cluster_candidate", "item_6425c9a49e3544649568bd7036bfcdb8", "item_b86f4bea90924975a2f1aef786aff460",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "relations_interesting.jsonl", "cluster_seed_rejections.jsonl"],
    recommended_label="research_paper",
    recommended_event_signature=esig("AK (@_akhaliq)", "HuggingFace papers feed", "research_paper", "", "2026-05-13", 0.55),
    recommended_relation="same_thread",
    should_form_event_cluster=True,
    should_form_thread_relation=True,
    should_fold=False,
    confidence=0.55,
    reason="Both are 'paper:' link posts from AK@_akhaliq on the same day. Same source, same format, same action (paper). The system identified them as suspicious_different (relation 3) with score 4.15, but no cluster formed. Should form a same-source research paper thread cluster.",
    risk_notes=["SPECULATIVE: No true multi-item cluster existed in run output", "Products are URL fragments — actual paper titles unknown", "These are link-sharing posts, not original content"],
))

# Cluster candidate 2 — Notion Developer Platform launch series (CLI + Workers + Custom Agents)
# Using CLI as primary and Workers as candidate
benchmark_rows.append(make_row("cluster_candidate", "item_eaf6591ef88f4dc58f0b86678ab3d50d", "item_882a0697c88d44f99a3e9cb0f21d2e7a",
    source_file_refs=["semantic_items.jsonl", "event_signatures.jsonl", "item_cards.jsonl", "cluster_seed_rejections.jsonl"],
    recommended_label="integration_or_tooling",
    recommended_event_signature=esig("Notion", "Notion Developer Platform", "release", "CLI + Workers + Custom Agents + Agent Tools", "2026-05-13", 0.9),
    recommended_relation="related_with_new_info",
    should_form_event_cluster=True,
    should_form_thread_relation=False,
    should_fold=False,
    confidence=0.8,
    reason="Notion launched CLI, Workers, and Custom Agent tools as a coordinated developer platform release. Four posts from @NotionHQ on May 13 all describe aspects of the same launch. These should form an event cluster but each ended up as a single-item cluster.",
    risk_notes=["SPECULATIVE: No true multi-item cluster existed in run output", "Multiple posts from same source about same launch — strongest cluster candidate in the dataset", "Posts have different focus areas but same underlying event"],
))

# ═══════════════════════════════════════════════════════════════════
# VALIDATE
# ═══════════════════════════════════════════════════════════════════

print(f"Total benchmark rows: {len(benchmark_rows)}")
kinds = {}
for r in benchmark_rows:
    kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
print(f"By kind: {kinds}")

labels = {}
for r in benchmark_rows:
    labels[r["recommended_label"]] = labels.get(r["recommended_label"], 0) + 1
print(f"By label: {labels}")

relations = {}
for r in benchmark_rows:
    if r["recommended_relation"]:
        relations[r["recommended_relation"]] = relations.get(r["recommended_relation"], 0) + 1
print(f"By relation: {relations}")

valid_events = sum(1 for r in benchmark_rows if r["recommended_event_signature"] and r["recommended_event_signature"].get("is_event_like"))
rejected = sum(1 for r in benchmark_rows if r["recommended_event_signature"] is None)
print(f"Valid event candidates: {valid_events}, Rejected/low-signal: {rejected}")
print(f"Pair rows with candidate: {sum(1 for r in benchmark_rows if r['candidate_item_id'])}")

assert len(benchmark_rows) == 50, f"Expected 50 rows, got {len(benchmark_rows)}"
ids = [r["benchmark_id"] for r in benchmark_rows]
assert len(ids) == len(set(ids)), "Duplicate benchmark IDs!"
assert all(r["recommended_label"] for r in benchmark_rows), "Empty recommended_label!"
for r in benchmark_rows:
    assert "benchmark_id" in r
    assert "item_id" in r
    assert "recommended_label" in r
    assert "recommended_event_signature" in r or r["recommended_event_signature"] is None
    if r["kind"] == "pair" or r["kind"] == "cluster_candidate":
        assert r.get("candidate_item_id"), f"Missing candidate_item_id for {r['benchmark_id']}"

print("\nAll validations passed!")

# ═══════════════════════════════════════════════════════════════════
# WRITE OUTPUTS
# ═══════════════════════════════════════════════════════════════════

def json_default(obj):
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    return str(obj)

# JSONL
with open(OUTPUT / "signature_benchmark_50.jsonl", "w") as f:
    for row in benchmark_rows:
        f.write(json.dumps(row, ensure_ascii=False, default=json_default) + "\n")

# CSV
csv_fields = [
    "benchmark_id", "kind", "source_file_refs",
    "item_id", "candidate_item_id", "cluster_id",
    "source_name", "candidate_source_name",
    "published_at", "candidate_published_at",
    "title", "candidate_title",
    "short_summary", "candidate_short_summary",
    "current_signature", "current_invalid_reasons",
    "current_relation", "current_candidate_lane", "current_candidate_priority",
    "recommended_label", "recommended_event_signature", "recommended_relation",
    "should_form_event_cluster", "should_form_thread_relation", "should_fold",
    "confidence", "reason", "risk_notes",
    "human_label", "human_notes",
]
with open(OUTPUT / "signature_benchmark_50.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
    writer.writeheader()
    for row in benchmark_rows:
        row_copy = {}
        for k, v in row.items():
            if isinstance(v, (list, dict)):
                row_copy[k] = json.dumps(v, ensure_ascii=False)
            elif v is None:
                row_copy[k] = ""
            elif isinstance(v, bool):
                row_copy[k] = str(v).lower()
            else:
                row_copy[k] = str(v)
        writer.writerow(row_copy)

# Review sheet CSV
review_fields = [
    "benchmark_id", "kind", "source_name", "published_at", "title",
    "candidate_title", "recommended_label", "recommended_relation",
    "should_form_event_cluster", "should_form_thread_relation",
    "reason", "human_label", "human_notes"
]
with open(OUTPUT / "signature_benchmark_50_review_sheet.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=review_fields, extrasaction="ignore")
    writer.writeheader()
    for row in benchmark_rows:
        row_copy = {}
        for k in review_fields:
            v = row.get(k, "")
            if isinstance(v, (list, dict)):
                row_copy[k] = json.dumps(v, ensure_ascii=False)
            elif v is None:
                row_copy[k] = ""
            elif isinstance(v, bool):
                row_copy[k] = str(v).lower()
            else:
                row_copy[k] = str(v)
        # Add signature summary
        sig = row.get("recommended_event_signature") or {}
        if isinstance(sig, str):
            try:
                sig = json.loads(sig)
            except:
                sig = {}
        if sig:
            row_copy["recommended_signature_short"] = f"{sig.get('actor','')}|{sig.get('product_or_model','')}|{sig.get('action','')}|{sig.get('date_bucket','')}"
        else:
            row_copy["recommended_signature_short"] = "REJECTED"
        writer.writerow(row_copy)

print(f"\nWrote {len(benchmark_rows)} rows to JSONL and CSV")
print(f"Output directory: {OUTPUT}")
