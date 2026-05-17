#!/usr/bin/env python3
"""Phase 1.3b Step 3: Reclassify benchmark rows, build taxonomy, generate fixtures."""
import json, csv, os
from pathlib import Path
from copy import deepcopy

STEP1 = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/phase1_3b_signature_benchmark_step1")
OUTPUT = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/phase1_3b_taxonomy_regression_step3")

# ── Load Step 1 benchmark ───────────────────────────────────────
bench_rows = []
with open(STEP1 / "signature_benchmark_50.jsonl") as f:
    for line in f:
        line = line.strip()
        if line:
            bench_rows.append(json.loads(line))

print(f"Loaded {len(bench_rows)} benchmark rows")

# ── Semantic level assignments ───────────────────────────────────
# Each key is benchmark_id, value is (semantic_level, reason)
SEMANTIC_LEVELS = {
    # === event_signature: concrete, dated, can seed event cluster ===
    "BENCH_1_3b_single_001": ("event_signature", "Dated conference (AI Security Summit London May 14). Has organizer (Snyk), venue (London), and time context. Should seed event cluster if cross-source coverage exists."),
    "BENCH_1_3b_single_002": ("event_signature", "Versioned software release (OpenShell v0.0.40). Has actor (NVIDIA), concrete product+version, and release notes. Strong event cluster seed candidate."),
    "BENCH_1_3b_single_003": ("event_signature", "Company launch (Recursive by Tian Yuandong). Has concrete actor, product name, and launch action. High-concreteness event."),
    "BENCH_1_3b_single_005": ("event_signature", "Company launch (PLAN0 from YC). Has concrete product name and launch action. Can seed event cluster if matched with cross-source coverage."),
    "BENCH_1_3b_single_007": ("event_signature", "Product release (Googlebook by Google). Chinese release language '刚刚发布'. Has actor, product name, and launch action. Key Chinese-language event example."),
    "BENCH_1_3b_single_008": ("event_signature", "Market milestone (NVIDIA $5.5T market cap). Has actor, concrete metric, and timestamp. Valid financial event."),
    "BENCH_1_3b_single_009": ("event_signature", "Adoption metric (Anthropic surpasses OpenAI in enterprise share). Has actor, concrete data from Ramp AI Index, and clear comparison. Should seed event cluster if matched with Chinese version."),
    "BENCH_1_3b_single_010": ("event_signature", "Product release (Notion CLI). Has actor (Notion), product name, and release action. Part of Notion developer platform launch series."),
    "BENCH_1_3b_single_011": ("event_signature", "Feature update (Notion Custom Agents tool support via Workers). Has actor, product, and feature update action. Part of Notion developer platform launch."),
    "BENCH_1_3b_single_012": ("event_signature", "Technical blog tied to specific product (Codex Windows sandbox by OpenAI). Has actor, product, and technical deep-dive content. Can seed event cluster if matched with other Codex coverage."),
    "BENCH_1_3b_single_013": ("event_signature", "Feature update (Codex remote control via ChatGPT mobile). Has product and feature update action. Part of Codex product thread."),
    "BENCH_1_3b_single_014": ("event_signature", "Integration announcement (QVeris CLI + Claude Code). Has product (QVeris CLI), integration target (Claude Code), and integration action. Valid event if dated."),
    "BENCH_1_3b_single_015": ("event_signature", "Versioned software release (OpenShell v0.0.41). Same product as v0.0.40, sequential release. Should form event cluster with v0.0.40 as related_with_new_info."),
    "BENCH_1_3b_single_016": ("event_signature", "Conference/event announcement (LangChain Interrupt with Andrew Ng). Has organizer, event name, and speakers. Valid event for cluster seed."),
    "BENCH_1_3b_single_024": ("event_signature", "Pricing event (China Telecom Shanghai Token phone plan). Chinese pricing language '做成话费套餐'. Key Chinese-language false negative example. Has actor, product, and pricing action."),
    "BENCH_1_3b_single_025": ("event_signature", "Hardware availability (NVIDIA Stelline Developer Kit shipping). Cryptic title but card entities confirm product. Valid event."),
    "BENCH_1_3b_single_026": ("event_signature", "Product preview (GitHub Copilot Desktop technical preview). Has actor (GitHub), product, and availability action with waitlist. Valid event."),
    "BENCH_1_3b_single_027": ("event_signature", "Pricing change (LangSmith Fleet free tier via Fireworks AI). Has product and pricing action. Real event misclassified as triple-failure."),
    "BENCH_1_3b_single_028": ("event_signature", "Pricing announcement follow-up (LangSmith Fleet free LLMs/sandboxes). Same event as _027 but different post style. Related_with_new_info to _027."),
    "BENCH_1_3b_single_029": ("event_signature", "Company launch (Adialante mobile MRI from YC). Action=launch detected but actor missing. Same format as other YC launches. Valid event."),
    "BENCH_1_3b_single_031": ("event_signature", "Third-party product coverage (Notion CLI from orange.ai). Restates Notion developer platform launch. Same event as official Notion posts. Cross-source event signal."),
    "BENCH_1_3b_single_032": ("event_signature", "Feature announcement (Notion Agent Tools via Workers). Has actor, product, and feature action. Part of Notion developer platform launch."),
    "BENCH_1_3b_single_033": ("event_signature", "Webinar event (Nemotron 3 Nano Omni Ask the Experts). Has product and event format. Valid event with date context."),

    # === thread_signature: related sequence, same-source recurring ===
    "BENCH_1_3b_single_004": ("thread_signature", "Firsthand social anecdote about DGX Spark local testing. Has product names (DGX Spark, Hermes Agent) but is a personal experience share, not a concrete event. Thread-like for NVIDIA local-model-testing topic."),
    "BENCH_1_3b_single_006": ("reject", "One-word title 'Concerning.' with 69-character product phrase. Low-context social reaction. Should be rejected — accepted signature is a false positive."),

    # === content_signature: useful for search but not event/thread ===
    "BENCH_1_3b_single_030": ("content_signature", "Personal tool setup share (translation workflow with DeepSeek V4 Flash). Has concrete product names but no event action. Useful for source profiling and search, not event clustering."),

    # === reject: low-signal, no semantic value ===
    "BENCH_1_3b_single_017": ("reject", "One-phrase social engagement ('Great advice'). No actor, product, or event. Pure social media engagement bait."),
    "BENCH_1_3b_single_018": ("reject", "One-word post ('Banger'). Zero semantic content. Should be filtered at ingest."),
    "BENCH_1_3b_single_019": ("reject", "Chinese podcast commentary on LLM development. Philosophical opinion with no event. Correctly rejected by current extractor."),
    "BENCH_1_3b_single_020": ("reject", "Chinese startup advice ('follow your heart, follow your money'). Pure opinion. Correctly rejected."),
    "BENCH_1_3b_single_021": ("reject", "Philosophical commentary ('skin in the game'). No concrete event. Correctly rejected."),
    "BENCH_1_3b_single_022": ("reject", "Three-word social reply ('Open > closed'). Zero event content. Should be filtered at ingest."),
    "BENCH_1_3b_single_023": ("reject", "Book excerpts (Taleb aphorisms). Literary content, not an event. Correctly rejected."),

    # === Pair rows: semantic_level for the PAIR, not individual items ===
    "BENCH_1_3b_pair_034": ("event_signature", "Cross-language near-duplicate (Anthropic adoption data EN+ZH). Same event from two sources. Should fold (should_fold=True). Valid event cluster seed across languages."),
    "BENCH_1_3b_pair_035": ("thread_signature", "Same product, different events (Codex remote control vs Windows sandbox). Both are valid Codex features but different releases. Thread relation, not event cluster."),
    "BENCH_1_3b_pair_036": ("thread_signature", "Same-source paper feed (AK paper: links). Same source, same format, same action (paper). Different papers = thread, not event cluster. URL fragments as product are meaningless."),
    "BENCH_1_3b_pair_037": ("reject", "False positive candidate (QVeris CLI vs AI news roundup). Shared entity 'Claude Code' caused high candidate score but items are unrelated. Should be different."),
    "BENCH_1_3b_pair_038": ("thread_signature", "Same-source recurring format (YC PLAN0 vs Modern launches). Same source, same action (launch), same format. Different companies = same_product_different_event, not same event."),
    "BENCH_1_3b_pair_039": ("event_signature", "Same-source coordinated launch (Notion CLI + Workers). Same timestamp, same source, same launch series. These describe the same Notion Developer Platform launch. Should form event cluster as related_with_new_info."),
    "BENCH_1_3b_pair_040": ("event_signature", "Sequential versioned releases (OpenShell v0.0.40 + v0.0.41). Same product, sequential versions. Should form event cluster as related_with_new_info."),
    "BENCH_1_3b_pair_041": ("event_signature", "Near-duplicate main post + link follow-up (NVIDIA agentic inference). Same source, same timestamp +1s. Second post is a pointer to the article. Should fold."),
    "BENCH_1_3b_pair_042": ("thread_signature", "Same company, different topics (Anthropic adoption vs Mythos debate). Shared actor but different sub-topics. Thread-like, not same event."),
    "BENCH_1_3b_pair_043": ("reject", "Generic token false positive (Recursive launch vs NVIDIA inference). 'agentic' and 'algorithm' are generic AI terms. Should be different."),
    "BENCH_1_3b_pair_044": ("thread_signature", "Recurring format (YC Modern vs YouArt launches). Same source, same format, different companies. Thread-like for YC launch series."),
    "BENCH_1_3b_pair_045": ("thread_signature", "Same company, different reports (Vercel AI report vs Ramp AI Index). Both about Anthropic adoption but different data sources and metrics. Thread-like."),
    "BENCH_1_3b_pair_046": ("reject", "Same-source philosophy thread (orange.ai skin in game + CUDA). Both items are rejected (no event signatures). CJK text fragments inflated candidate score. Thread for philosophical content only — no event cluster."),
    "BENCH_1_3b_pair_047": ("reject", "Different events, same format (AI Security Summit vs LangChain Interrupt). Both are event announcements but completely different events. Should be different."),
    "BENCH_1_3b_pair_048": ("event_signature", "Same-source same-timestamp launch (Notion Custom Agents + Agent Tools). Same timestamp (16:27:37), same source, overlapping content. Should form event cluster as related_with_new_info."),

    # === Cluster candidates ===
    "BENCH_1_3b_cluster_candidate_049": ("thread_signature", "Same-source paper feed thread (AK paper: posts). Same source, format, and action. Different papers = thread cluster, not event cluster. Should form thread relation but NOT an event cluster."),
    "BENCH_1_3b_cluster_candidate_050": ("event_signature", "Coordinated developer platform launch (Notion CLI + Workers + Custom Agents). Same source, same day, overlapping content describing one platform launch. Strongest event cluster candidate in dataset."),
}

# ── Apply semantic levels ────────────────────────────────────────
taxonomy_rows = []
for row in bench_rows:
    tr = deepcopy(row)
    bid = row["benchmark_id"]
    if bid in SEMANTIC_LEVELS:
        tr["semantic_level"] = SEMANTIC_LEVELS[bid][0]
        tr["semantic_level_reason"] = SEMANTIC_LEVELS[bid][1]
    else:
        tr["semantic_level"] = "unassigned"
        tr["semantic_level_reason"] = "NOT YET CLASSIFIED — needs manual review"
        print(f"WARNING: {bid} not assigned a semantic level!")
    taxonomy_rows.append(tr)

# ── Validate ──────────────────────────────────────────────────────
levels = {}
for tr in taxonomy_rows:
    levels[tr["semantic_level"]] = levels.get(tr["semantic_level"], 0) + 1
print(f"Semantic level distribution: {levels}")
assert len(taxonomy_rows) == 50
assert "unassigned" not in levels, f"Unassigned rows exist!"
assert levels.get("event_signature", 0) >= 20, f"Need >= 20 event_signature, got {levels.get('event_signature', 0)}"

# ── Write taxonomy benchmark ──────────────────────────────────────
# JSONL
with open(OUTPUT / "signature_benchmark_with_taxonomy.jsonl", "w") as f:
    for tr in taxonomy_rows:
        f.write(json.dumps(tr, ensure_ascii=False) + "\n")

# CSV
csv_fields = [
    "benchmark_id", "kind", "semantic_level", "semantic_level_reason",
    "item_id", "candidate_item_id", "source_name", "title",
    "recommended_label", "recommended_relation",
    "should_form_event_cluster", "should_form_thread_relation", "should_fold",
    "confidence", "reason"
]
with open(OUTPUT / "signature_benchmark_with_taxonomy.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
    writer.writeheader()
    for tr in taxonomy_rows:
        rc = {}
        for k in csv_fields:
            v = tr.get(k, "")
            if isinstance(v, (list, dict)):
                rc[k] = json.dumps(v, ensure_ascii=False)
            elif v is None:
                rc[k] = ""
            elif isinstance(v, bool):
                rc[k] = str(v).lower()
            else:
                rc[k] = str(v)
        writer.writerow(rc)

print(f"Wrote taxonomy benchmark: {len(taxonomy_rows)} rows")

# ═══════════════════════════════════════════════════════════════════
# REGRESSION FIXTURES
# ═══════════════════════════════════════════════════════════════════

# ── Fixture 1: signature regression ───────────────────────────────
sig_fixtures = []
for tr in taxonomy_rows:
    if tr["kind"] != "single":
        continue
    sl = tr["semantic_level"]
    rec = tr.get("recommended_event_signature") or {}
    if isinstance(rec, str):
        try: rec = json.loads(rec)
        except: rec = {}

    fix = {
        "fixture_id": f"FIX_SIG_{tr['benchmark_id']}",
        "benchmark_id": tr["benchmark_id"],
        "item_id": tr["item_id"],
        "title": tr["title"],
        "expected_semantic_level": sl,
        "expected_action": rec.get("action", ""),
        "expected_actor": rec.get("actor", ""),
        "expected_product_or_model": rec.get("product_or_model", ""),
        "expected_should_accept_event_signature": sl == "event_signature",
        "expected_should_accept_thread_signature": sl in ("event_signature", "thread_signature"),
        "must_not_extract_as_product": [],
        "must_not_extract_as_actor": [],
        "notes": tr.get("reason", "")
    }

    # Add known must-not-extract rules based on Step 1 findings
    bid = tr["benchmark_id"]
    if bid == "BENCH_1_3b_single_001":
        fix["must_not_extract_as_product"] = ["May 14"]
        fix["must_not_extract_as_actor"] = ["unknown"]
    elif bid == "BENCH_1_3b_single_002":
        fix["must_not_extract_as_product"] = ["k8s"]
    elif bid == "BENCH_1_3b_single_003":
        fix["must_not_extract_as_product"] = ["Our 25"]
        fix["must_not_extract_as_actor"] = ["Meta"]
    elif bid == "BENCH_1_3b_single_004":
        fix["must_not_extract_as_product"] = ["for updates from my phone", "hermes agent"]
    elif bid == "BENCH_1_3b_single_009":
        fix["must_not_extract_as_product"] = ["just 0.3"]
    elif bid == "BENCH_1_3b_single_010":
        fix["must_not_extract_as_product"] = ["made just for developers and coding agents"]
    elif bid == "BENCH_1_3b_single_012":
        fix["must_not_extract_as_product"] = ["exit 1"]
    elif bid == "BENCH_1_3b_single_014":
        fix["must_not_extract_as_actor"] = ["Claude"]
    elif bid == "BENCH_1_3b_single_015":
        fix["must_not_extract_as_product"] = ["U4n62"]
    elif bid == "BENCH_1_3b_single_006":
        fix["must_not_extract_as_product"] = ["coordinated opposition campaigns around our Utah projects"]

    sig_fixtures.append(fix)

with open(OUTPUT / "regression_fixture_phase1_3b_signature.jsonl", "w") as f:
    for fix in sig_fixtures:
        f.write(json.dumps(fix, ensure_ascii=False) + "\n")
print(f"Signature fixtures: {len(sig_fixtures)}")

# ── Fixture 2: relation regression ────────────────────────────────
rel_fixtures = []
for tr in taxonomy_rows:
    if tr["kind"] not in ("pair", "cluster_candidate"):
        continue
    if not tr.get("candidate_item_id"):
        continue

    sl = tr["semantic_level"]
    rec_rel = tr.get("recommended_relation", "")

    fix = {
        "fixture_id": f"FIX_REL_{tr['benchmark_id']}",
        "benchmark_id": tr["benchmark_id"],
        "item_a_id": tr["item_id"],
        "item_b_id": tr["candidate_item_id"],
        "expected_relation": rec_rel,
        "expected_should_fold": tr.get("should_fold", False),
        "expected_should_form_event_cluster": sl == "event_signature" and tr.get("should_form_event_cluster", False),
        "expected_should_form_thread_relation": tr.get("should_form_thread_relation", False),
        "expected_can_seed_event_cluster": sl == "event_signature",
        "notes": tr.get("reason", "")
    }
    rel_fixtures.append(fix)

with open(OUTPUT / "regression_fixture_phase1_3b_relations.jsonl", "w") as f:
    for fix in rel_fixtures:
        f.write(json.dumps(fix, ensure_ascii=False) + "\n")
print(f"Relation fixtures: {len(rel_fixtures)}")

# ── Fixture 3: cluster regression ─────────────────────────────────
cluster_fixtures = []

# Notion Developer Platform cluster
cluster_fixtures.append({
    "fixture_id": "FIX_CLUSTER_001",
    "benchmark_id": "BENCH_1_3b_cluster_candidate_050",
    "candidate_item_ids": [
        "item_eaf6591ef88f4dc58f0b86678ab3d50d",  # Notion CLI
        "item_a40e531db76a4d5f8043ffc79c127012",  # Notion Workers
        "item_882a0697c88d44f99a3e9cb0f21d2e7a",  # Custom Agents
        "item_10d47a60c33d4553b036a1a8fa6a02b7",  # Agent Tools/Workers
    ],
    "expected_cluster_type": "event_cluster",
    "expected_should_form_event_cluster": True,
    "expected_should_form_thread_relation": False,
    "expected_signature": {
        "actor": "Notion",
        "product_or_model": "Notion Developer Platform",
        "action": "release",
        "object": "CLI + Workers + Custom Agents + Agent Tools",
        "date_bucket": "2026-05-13",
        "confidence": 0.9
    },
    "notes": "Coordinated developer platform launch from @NotionHQ. Four posts on May 13 describe different aspects of the same launch. Same source, overlapping timestamps, overlapping entities. Strongest event cluster candidate in Phase 1.3 evidence."
})

# OpenShell sequential releases
cluster_fixtures.append({
    "fixture_id": "FIX_CLUSTER_002",
    "benchmark_id": "BENCH_1_3b_pair_040",
    "candidate_item_ids": [
        "item_9353d0480b5d4303bb2e9d8bb3983f5a",  # v0.0.40
        "item_d28c9c5b374a46f3a9a81902384e1ec3",  # v0.0.41
    ],
    "expected_cluster_type": "event_cluster",
    "expected_should_form_event_cluster": True,
    "expected_should_form_thread_relation": False,
    "expected_signature": {
        "actor": "NVIDIA",
        "product_or_model": "OpenShell",
        "action": "release",
        "object": "v0.0.40 → v0.0.41",
        "date_bucket": "2026-05-14",
        "confidence": 0.9
    },
    "notes": "Sequential versioned releases of OpenShell. Same product, same source, consecutive versions. v0.0.40 accepted by current extractor, v0.0.41 rejected — pipeline inconsistency. Should form event cluster as related_with_new_info."
})

# Anthropic adoption cross-language near-duplicate
cluster_fixtures.append({
    "fixture_id": "FIX_CLUSTER_003",
    "benchmark_id": "BENCH_1_3b_pair_034",
    "candidate_item_ids": [
        "item_f14c5d1af066457dbc050b797452ddcb",  # EN: The Rundown AI
        "item_0bc73c59c550408d8e9b09a873d607e4",  # ZH: AI Will
    ],
    "expected_cluster_type": "event_cluster",
    "expected_should_form_event_cluster": True,
    "expected_should_form_thread_relation": False,
    "expected_signature": {
        "actor": "Anthropic",
        "product_or_model": "Claude",
        "action": "adoption_metric",
        "object": "enterprise share surpasses OpenAI (Ramp AI Index)",
        "date_bucket": "2026-05-13",
        "confidence": 0.95
    },
    "notes": "Cross-language near-duplicate. Both report same Ramp AI Index data. System correctly identified as near_duplicate with should_fold=True. Strong should-fold event cluster example."
})

# AK paper thread (NOT event cluster — thread only)
cluster_fixtures.append({
    "fixture_id": "FIX_CLUSTER_004",
    "benchmark_id": "BENCH_1_3b_cluster_candidate_049",
    "candidate_item_ids": [
        "item_6425c9a49e3544649568bd7036bfcdb8",
        "item_b86f4bea90924975a2f1aef786aff460",
    ],
    "expected_cluster_type": "thread_candidate",
    "expected_should_form_event_cluster": False,
    "expected_should_form_thread_relation": True,
    "expected_signature": {
        "actor": "AK (@_akhaliq)",
        "product_or_model": "HuggingFace papers feed",
        "action": "research_paper",
        "object": "",
        "date_bucket": "2026-05-13",
        "confidence": 0.55
    },
    "notes": "Same-source same-format paper link posts. Should form thread relation, NOT event cluster. Different papers = different events. Products are URL fragments. This is a key example of thread_signature vs event_signature distinction."
})

# YC launch series (NOT event cluster — recurring format)
cluster_fixtures.append({
    "fixture_id": "FIX_CLUSTER_005",
    "benchmark_id": "BENCH_1_3b_pair_038",
    "candidate_item_ids": [
        "item_ce3cfb151a984123a49a53b5d7a4db4b",  # PLAN0
        "item_56610f563a81415c9ed9aac9437f6ae0",  # Modern
        "item_cf0515fcd3a14c0d890cd7abc5f5e646",  # YouArt
        "item_7f5662046d694a2d87dc541de9e41a45",  # Adialante
    ],
    "expected_cluster_type": "thread_candidate",
    "expected_should_form_event_cluster": False,
    "expected_should_form_thread_relation": True,
    "expected_signature": {
        "actor": "Y Combinator",
        "product_or_model": "YC Launches",
        "action": "company_launch",
        "object": "",
        "date_bucket": "2026-05-14",
        "confidence": 0.8
    },
    "notes": "Recurring YC launch format. Same source, same action, same format, but different companies. Should NOT form event cluster — these are different events. Thread relation for YC launch series is appropriate. Key example of when same source + same format should NOT cluster."
})

# Low-signal pair (should not cluster or thread)
cluster_fixtures.append({
    "fixture_id": "FIX_CLUSTER_006",
    "benchmark_id": "BENCH_1_3b_pair_046",
    "candidate_item_ids": [
        "item_3445b70e409c4853a19117c27dfacd13",
        "item_3ee768f4562f49879278963ed4efaaac",
    ],
    "expected_cluster_type": "reject",
    "expected_should_form_event_cluster": False,
    "expected_should_form_thread_relation": True,
    "expected_signature": None,
    "notes": "Same-source philosophical content. Both items are correctly rejected (triple-failure). CJK text fragments inflated candidate score. Thread relation is for content navigation only — neither item produces event signatures. No cluster should form."
})

with open(OUTPUT / "regression_fixture_phase1_3b_clusters.jsonl", "w") as f:
    for fix in cluster_fixtures:
        f.write(json.dumps(fix, ensure_ascii=False) + "\n")
print(f"Cluster fixtures: {len(cluster_fixtures)}")

print("\n=== ALL OUTPUTS WRITTEN ===")
print(f"Output directory: {OUTPUT}")
