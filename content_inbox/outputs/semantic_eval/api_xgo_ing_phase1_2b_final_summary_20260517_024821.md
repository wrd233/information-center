# api.xgo.ing Phase 1.2b Final Summary

## 1. Source Refresh Summary

{
  "backup_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/backups/content_inbox.sqlite3.before_api_xgo_semantic_phase1_2b_20260517_013814.sqlite3",
  "sources_selected": 151,
  "sources_succeeded_final_bounded_pass": 5,
  "sources_failed_final_bounded_pass": 146,
  "failures_by_reason": {
    "ingest_failed": 1,
    "source_ingest_timeout": 145
  },
  "items_before_final_bounded_pass": 2550,
  "items_after_final_bounded_pass": 2551,
  "db_item_delta_final_bounded_pass": 1,
  "duplicates_final_bounded_pass": 54,
  "latest_item_time_before": "2026-05-16T10:18:27+00:00",
  "latest_item_time_after": "2026-05-16T10:18:27+00:00",
  "note": "Earlier interrupted scoped attempts inserted additional api.xgo.ing items before the final bounded report; probe before/after is the authoritative net refresh view."
}

## 2. Probe Before/After Comparison

{
  "before_items": 728,
  "after_items": 782,
  "net_new_linked_items": 54,
  "before_latest_item_time": "2026-05-05T03:57:57+00:00",
  "after_latest_item_time": "2026-05-16T10:18:27+00:00",
  "before_sources_with_items": 146,
  "after_sources_with_items": 147,
  "zero_item_sources_before": 5,
  "zero_item_sources_after": 4,
  "scope_missing_source_id_items_after": 0,
  "scope_missing_feed_url_items_after": 0,
  "html_entity_source_name_issues_after": 5
}

## 3. Prompt/Chain Iteration Log

[
  {
    "iteration": "initial smoke",
    "finding": "item_card LLM batches failed and all 50 cards fell back to heuristic; output JSON was often truncated/unterminated."
  },
  {
    "iteration": "prompt/cap fix",
    "changes": [
      "item_card prompt tightened for AI model/company/product preservation, fact/opinion split, summary-only warnings",
      "item_relation and item_cluster prompts clarified same-event vs same-topic/follow-up and AI entity overlap",
      "cluster_card prompt clarified compact titles/core facts/known angles",
      "candidate recall now scores normalized entity overlap, semantic tokens, cross-source bonus, and 24/72h time windows",
      "increased output caps: item_card 4000, item_relation 2200, item_cluster_relation 2600"
    ]
  },
  {
    "iteration": "corrected smoke",
    "result": "item_card failures dropped to 1 batch; heuristic fallback dropped to 5/50; related_with_new_info and near_duplicate appeared."
  },
  {
    "iteration": "larger runs",
    "finding": "default 200k token budget is consumed largely by item_card generation, limiting downstream item_relation/cluster coverage at 150/300 items."
  }
]

## 4. Concurrency Comparison

{
  "generated_at": "2026-05-17T02:47:39.696911",
  "note": "c2 comparator reuses the corrected api_xgo_ing_full_150_c2 run copied into c2_cmp to avoid duplicate live token spend; c3 and c4 were fresh comparison runs.",
  "reason": "concurrency=3 had the shortest duration with no rate-limit or DB-lock errors and fewer final failures than c2/c4 under the same 200k token budget; c4 did not improve throughput and had higher p95 latency/failures.",
  "recommended_concurrency": 3,
  "runs": [
    {
      "actual_calls": 44,
      "actual_tokens": 206094,
      "avg_latency_ms": 20789.8,
      "cache_hit_rate": 0.1845,
      "cache_hit_tokens": 38016,
      "calls_per_sec": 0.0741,
      "cluster_relations": {
        "new_info": 14,
        "source_material": 4
      },
      "concurrency": 2,
      "db_lock_errors": 0,
      "duration_seconds": 594.173,
      "final_failures": 3,
      "heuristic_card_fallback_count": 15,
      "item_card_failed": 3,
      "p50_latency_ms": 21257,
      "p95_latency_ms": 30208,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "relations": {
        "different": 55,
        "near_duplicate": 2,
        "related_with_new_info": 15
      },
      "repair_retry_count": 3,
      "source_path": "outputs/semantic_eval/api_xgo_ing_full_150_c2_cmp/semantic_quality_summary.json",
      "successful_cluster_card_patches": 0,
      "successful_item_cards": 27,
      "successful_item_cluster_relations": 0,
      "successful_item_relations": 14,
      "tokens_per_sec": 346.86
    },
    {
      "actual_calls": 43,
      "actual_tokens": 209040,
      "avg_latency_ms": 21531.6,
      "cache_hit_rate": 0.1763,
      "cache_hit_tokens": 36864,
      "calls_per_sec": 0.1216,
      "cluster_relations": {
        "new_info": 17,
        "source_material": 3
      },
      "concurrency": 3,
      "db_lock_errors": 0,
      "duration_seconds": 353.698,
      "final_failures": 1,
      "heuristic_card_fallback_count": 5,
      "item_card_failed": 1,
      "p50_latency_ms": 22439,
      "p95_latency_ms": 29555,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "relations": {
        "different": 53,
        "near_duplicate": 4,
        "related_with_new_info": 12
      },
      "repair_retry_count": 1,
      "source_path": "outputs/semantic_eval/api_xgo_ing_full_150_c3_cmp/semantic_quality_summary.json",
      "successful_cluster_card_patches": 0,
      "successful_item_cards": 29,
      "successful_item_cluster_relations": 0,
      "successful_item_relations": 13,
      "tokens_per_sec": 591.01
    },
    {
      "actual_calls": 49,
      "actual_tokens": 212231,
      "avg_latency_ms": 20962.6,
      "cache_hit_rate": 0.2352,
      "cache_hit_tokens": 49920,
      "calls_per_sec": 0.1231,
      "cluster_relations": {
        "new_info": 17,
        "source_material": 5
      },
      "concurrency": 4,
      "db_lock_errors": 0,
      "duration_seconds": 398.016,
      "final_failures": 3,
      "heuristic_card_fallback_count": 15,
      "item_card_failed": 3,
      "p50_latency_ms": 20752,
      "p95_latency_ms": 33846,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "relations": {
        "different": 73,
        "near_duplicate": 4,
        "related_with_new_info": 18
      },
      "repair_retry_count": 3,
      "source_path": "outputs/semantic_eval/api_xgo_ing_full_150_c4_cmp/semantic_quality_summary.json",
      "successful_cluster_card_patches": 0,
      "successful_item_cards": 27,
      "successful_item_cluster_relations": 0,
      "successful_item_relations": 19,
      "tokens_per_sec": 533.22
    }
  ]
}

## 5. Final Full Evaluation Summary

{
  "items_sampled": 300,
  "actual_calls": 35,
  "actual_tokens": 216872,
  "item_cards": {
    "avg_confidence": 0.629,
    "content_role_distribution": {
      "aggregator": 3,
      "analysis": 21,
      "commentary": 32,
      "firsthand": 16,
      "low_signal": 33,
      "report": 117,
      "source_material": 78
    },
    "entity_count_distribution": {
      "0": 12,
      "1": 25,
      "2": 46,
      "3": 55,
      "4": 48,
      "5": 36,
      "6": 32,
      "7": 28,
      "8": 8,
      "9": 4,
      "10": 3,
      "11": 1,
      "14": 1,
      "15": 1
    },
    "heuristic_card_fallback_count": 125,
    "item_cards_failed": 0,
    "item_cards_generated": 300,
    "item_cards_generated_or_reused": 300,
    "item_cards_reused": 0,
    "samples": [
      {
        "item_id": "item_005146f422b44ef0b9111375fc37c1bc",
        "role": "source_material",
        "summary": "Mistral AI announced public preview of Workflows, an orchestration layer for enterprise AI, used by organizations including ASML, ABANCA, CMA-CGM, France Travail, La Banque Postale, Moeve.",
        "title": "Mistral AI releases public preview of Workflows, the orchestration layer for enterprise AI"
      },
      {
        "item_id": "item_008568ca63864852a278b6196a5592fd",
        "role": "report",
        "summary": "Andrew Dai launched ElorianAI, a multimodal reasoning lab, after 12 years at Brain/DeepMind.",
        "title": "My former Brain colleague @AndrewDai just launched @ElorianAI"
      },
      {
        "item_id": "item_00a898ed350745bfba572359d4f4d24c",
        "role": "low_signal",
        "summary": "Alex Albert recommends Jack Raines' book 'Young Money' for teens/20s.",
        "title": "Jack's young money blog had a big impact on me when I was in college"
      },
      {
        "item_id": "item_028ebef302864044b56032ed693483ae",
        "role": "analysis",
        "summary": "Want to move faster with AI without losing human oversight? ⏸️ Join our live session on April 8th for a quick introduction to Dify’s Human Input node, including how it works, how to use it, and real workflow demos. You’ll see how to seamlessly add a review step into your workflow so outputs can be paused, checked, and approved before they go live. When AI s…",
        "title": "Want to move faster with AI without losing human oversight? ⏸️ Join our live session on April 8th f..."
      },
      {
        "item_id": "item_03126b51b80e4bebbcbd350dae2387bc",
        "role": "aggregator",
        "summary": "Latent.Space posts 'ImageGen is on the Path to AGI'.",
        "title": "[AINews] ImageGen is on the Path to AGI"
      },
      {
        "item_id": "item_04c96d0dfc174175b19634543bd29dc9",
        "role": "report",
        "summary": "I've been working on this essay for a while, and it is mainly about AI and about the future. But given the horror we're seeing in Minnesota, its emphasis on the importance of preserving democratic values and rights at home is particularly relevant. 💬 298 🔄 413 ❤️ 6661 👀 1114750 📊 903 ⚡ Powered by xgo.ing",
        "title": "I've been working on this essay for a while, and it is mainly about AI and about the future. But giv..."
      },
      {
        "item_id": "item_04e656f80035418f80d5efa6868b17ff",
        "role": "analysis",
        "summary": "happy horse is insanely happy Chetaslua @chetaslua 🚨 Happy Horse First Output This model beats seedance 2 on artificial analysis for more information check quoted tweet Your browser does not support the video tag. 🔗 View on Twitter 🔗 View Quoted Tweet 💬 7 🔄 2 ❤️ 69 👀 24907 📊 12 ⚡ Powered by xgo.ing",
        "title": "happy horse is insanely happy"
      },
      {
        "item_id": "item_050f2b0c19cd4d3e807948aed3dae097",
        "role": "low_signal",
        "summary": "Promotional tweet with link to skywork.ai.",
        "title": "Make your own: skywork.ai"
      },
      {
        "item_id": "item_05280d3f568e4d85993f4e21c7f2a05e",
        "role": "report",
        "summary": "Our lying Ontario premier has just stolen $50 from every single person in Ontario. The estimated cost of repairing our beloved Science Center was 200 million dollars. The firm that made the estimate was told to multiply it by 1.85 to make it bigger. We were then told it would be better to build a new science center. Now we learn the new center will be small…",
        "title": "Our lying Ontario premier has just stolen $50 from every single person in Ontario. The estimated cos..."
      },
      {
        "item_id": "item_05df64b7139c4d63a534344df9adbbf6",
        "role": "source_material",
        "summary": "DeepSeek announces API availability for deepseek-v4-pro and deepseek-v4-flash, with 1M context and dual modes, and retirement of deepseek-chat and deepseek-reasoner by July 24, 2026.",
        "title": "API is Available Today! DeepSeek v4 Pro and v4 Flash Models"
      }
    ],
    "warnings_distribution": {
      "anecdotal_evidence": 1,
      "anecdote": 1,
      "announcement_teaser": 1,
      "claim_unverified": 1,
      "claims about 'better than any other model' may be unverified": 1,
      "claims research-backed without citation": 1,
      "contains opinion": 1,
      "contains speculation": 1,
      "contains_quoted_content": 1,
      "firsthand experience": 1,
      "heuristic_card": 125,
      "link_only": 1,
      "low_detail": 1,
      "low_information": 1,
      "low_signal": 2,
      "marketing": 1,
      "marketing_giveaway": 1,
      "marketing_promotion": 1,
      "no_details": 1,
      "opinion": 2,
      "opinion/analysis": 1,
      "opinion_heavy": 1,
      "opinion_only": 5,
      "opinion_piece": 1,
      "opinion_tweet": 1,
      "personal opinion": 1,
      "personal reaction": 1,
      "product_announcement": 1,
      "promotional": 7,
      "promotional content": 1,
      "promotional_content": 4,
      "promotional_language": 1,
      "promotional_tweet": 1,
      "quote_tweet": 1,
      "request/query": 1,
      "short announcement": 1,
      "short_content": 1,
      "source is employee not official account": 1,
      "subjective claim": 1,
      "summary_only": 19,
      "thin_content": 1,
      "too_short": 19,
      "tutorial": 1,
      "unclear_context": 1,
      "unverified_claim": 1,
      "vague_content": 3
    }
  },
  "item_relations": {
    "near_duplicate": 11
  },
  "item_clusters": {
    "new_info": 18,
    "source_material": 7
  },
  "multi_item_cluster_count": 0,
  "source_profiles_recomputed": 82,
  "pending_reviews_created": 612,
  "errors_fallbacks": {
    "db_lock_errors": 0,
    "final_failures": 0,
    "llm_parse_failures": 0,
    "repair_retry_count": 0,
    "review_queue_entries_due_to_failure": 553,
    "skipped_due_to_max_calls": false,
    "skipped_due_to_missing_card": 0,
    "skipped_due_to_no_candidate": 0,
    "skipped_due_to_token_budget": false
  }
}

## 6. Relation Distribution

{
  "avg_confidence": 1.0,
  "candidate_pairs_considered": 11,
  "different": 0,
  "duplicate": 0,
  "examples": [
    {
      "candidate_item_title": "🚀 Introducing FlashQLA: high-performance linear attention kernels built on TileLang. ⚡ 2–3× forwar...",
      "confidence": 1.0,
      "new_item_title": "🚀 Introducing FlashQLA: high-performance linear attention kernels built on TileLang. ⚡ 2–3× forwar...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-04-29T12:16:13+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-qwen-alibaba-qwen"
    },
    {
      "candidate_item_title": "🚀 Introducing FlashQLA: high-performance linear attention kernels built on TileLang. ⚡ 2–3× forwar...",
      "confidence": 1.0,
      "new_item_title": "🚀 Introducing FlashQLA: high-performance linear attention kernels built on TileLang. ⚡ 2–3× forwar...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-04-29T12:15:51+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-qwen-alibaba-qwen"
    },
    {
      "candidate_item_title": "The $15B Physical AI Company: 4 stack rewrites, end-to-end RL, neural sim, android for vehicles, tru...",
      "confidence": 1.0,
      "new_item_title": "The $15B Physical AI Company: 4 stack rewrites, end-to-end RL, neural sim, android for vehicles, tru...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-04-27T23:08:13+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-latent-space-latentspacepod"
    },
    {
      "candidate_item_title": "Coming May 14 at Microsoft Research Forum: a new release and demo from MSR AI Frontiers. Plus new ...",
      "confidence": 1.0,
      "new_item_title": "Coming May 14 at Microsoft Research Forum: a new release and demo from MSR AI Frontiers. Plus new ...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-04-27T22:20:09+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "The $15B Physical AI Company: 4 stack rewrites, end-to-end RL, neural sim, android for vehicles, tru...",
      "confidence": 1.0,
      "new_item_title": "The $15B Physical AI Company: 4 stack rewrites, end-to-end RL, neural sim, android for vehicles, tru...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-04-28T15:00:02+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-latent-space-latentspacepod"
    },
    {
      "candidate_item_title": "Coming May 14 at Microsoft Research Forum: a new release and demo from MSR AI Frontiers. Plus new ...",
      "confidence": 1.0,
      "new_item_title": "Coming May 14 at Microsoft Research Forum: a new release and demo from MSR AI Frontiers. Plus new ...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-04-27T16:30:15+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "🚀 Sovereign AI for the World. Cohere & Aleph Alpha form transatlantic AI powerhouse anchored in Ca...",
      "confidence": 1.0,
      "new_item_title": "🚀 Sovereign AI for the world. Cohere & Aleph Alpha form transatlantic AI powerhouse anchored in Ca...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-04-24T11:00:21+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-cohere-cohere"
    },
    {
      "candidate_item_title": "🚀 Sovereign AI for the world. Cohere & Aleph Alpha form transatlantic AI powerhouse anchored in Ca...",
      "confidence": 1.0,
      "new_item_title": "🚀 Sovereign AI for the World. Cohere & Aleph Alpha form transatlantic AI powerhouse anchored in Ca...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-04-24T10:19:20+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-cohere-cohere"
    },
    {
      "candidate_item_title": "Tweet",
      "confidence": 1.0,
      "new_item_title": "Tweet",
      "primary_relation": "near_duplicate",
      "published_at": "2026-03-01T11:39:34+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-junyang-lin-justinlin610"
    },
    {
      "candidate_item_title": "🚀 Monica 9.0 is LIVE now Meet Monica Agent, your most powerful agent yet. Deep Research: Research...",
      "confidence": 1.0,
      "new_item_title": "🚀 Monica 9.0 is LIVE now Meet Monica Agent, your most powerful agent yet. Deep Research: Research...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-01-14T10:52:31+00:00",
      "reason": "deterministic duplicate rule matched",
      "secondary_roles": [
        "same_title_hash"
      ],
      "should_fold": true,
      "source": "socialmedia-monica-im-hey-im-monica"
    }
  ],
  "fold_candidates": 11,
  "llm_item_relation_calls": 0,
  "low_confidence_examples": [],
  "near_duplicate": 11,
  "related_with_new_info": 0,
  "related_with_new_info_count": 0,
  "relations_by_primary_relation": {
    "near_duplicate": 11
  },
  "uncertain_count": 0
}

## 7. Cluster Quality Summary

{
  "actions": {
    "attach_to_cluster": 25
  },
  "attached_existing_clusters": 0,
  "avg_confidence": 0.6,
  "avg_items_per_cluster": 1.0,
  "candidate_clusters_considered": 25,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "Google DeepMind signs MoU with Korea Ministry of Science and ICT",
      "core_facts": [
        "Google DeepMind CEO Demis Hassabis announces signing of MoU with Korea Ministry of Science and ICT to collaborate on AI for scientific discovery and talent development."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_7dc849c1699346858493e1aef635ee47"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Qwen posts benchmark results",
      "core_facts": [
        "Qwen (@Alibaba_Qwen) posted forward and backward benchmark results across common configurations."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_3dcd3f32e0da437f977a77e38f7f86b3"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Qdrant attending AI Dev Conference",
      "core_facts": [
        "Qdrant is at AI Dev Conference, invites attendees to visit their booth on Day 2."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_259ac9df11e742b6ae635b2cbee3bca0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "DeepSeek-V4-Pro discount extension and integration updates",
      "core_facts": [
        "DeepSeek extends DeepSeek-V4-Pro API 75% discount until May 31, 2026; integration updates for Claude Code, OpenCode, OpenClaw."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c7843e818ca14d75ad88dc5ece5fe7ea"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Working at Gumroad",
      "core_facts": [
        "Sahil Lavingia tweets about working at Gumroad."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_5799b4a546674545b4fb905936b520a7"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Release of Eleven Album Vol. 2",
      "core_facts": [
        "Eleven Album Vol. 2 is released, featuring tracks from multiple artists."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_dd7a3e4542934912a24e90b710e9ea9a"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Promotion of Skywork platform",
      "core_facts": [
        "Promotional tweet with link to skywork.ai."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_050f2b0c19cd4d3e807948aed3dae097"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Lovable nearly reached 4,000-hour Discord chat record",
      "core_facts": [
        "Lovable nearly reached a 4,000-hour Discord chat record."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_1d4afe1a5bbe4d52a56a96fef1816d44"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Mustafa Suleyman's AI chip thought experiment",
      "core_facts": [
        "Mustafa Suleyman illustrates AI chip capability with a thought experiment: all humans using calculators non-stop for 22 days equals one GB300 chip's one second computation."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_4b98dab7129a4f5ba03f6960d5926aac"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Dify hands-on session at NYU Abu Dhabi",
      "core_facts": [
        "Dify's Alvin and Kelvin conducted a hands-on session with NYU Abu Dhabi MBA students, demonstrating scheduled financial analyst agent with human-in-the-loop, Knowledge Pipeline, and sharing insights on scaling AI projects."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_0cffc7a8e9024f1d852e1b221a5e3ca4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Speculative analogy between psychohistory and diffusion models",
      "core_facts": [
        "Andrew Chen speculates that psychohistory from Foundation could be a diffusion model trained on date cutoffs to extrapolate future events, describing a methodology to test future-predictive latent structure."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_28e7dccd17d14acfb8783012d46b99aa"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Adam D'Angelo wants Waymo route preferences",
      "core_facts": [
        "Adam D'Angelo expresses desire to tell his Waymo to take a specific route."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ecf18772ea2849819be4ed47c415487d"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Mistral AI releases public preview of Workflows for enterprise AI orchestration",
      "core_facts": [
        "Mistral AI announced public preview of Workflows, an orchestration layer for enterprise AI, used by organizations including ASML, ABANCA, CMA-CGM, France Travail, La Banque Postale, Moeve."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_005146f422b44ef0b9111375fc37c1bc"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Example: web infrastructure 1. Do less work...",
      "core_facts": [
        "Lee Robinson gives examples for web infrastructure optimization: cache at CDN, use brotli over gzip, WebP over PNG, and offload to web workers."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_8ef6aa98e3e94738b98b0c4623ccd01c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Genspark x AnthropicAI Hackathon in Singapore",
      "core_facts": [
        "Eric Jing congratulates on a successful Genspark x AnthropicAI Hackathon in Singapore, noting 40+ projects and $18,000 in credits awarded."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_8a959feef405458f8828947caaaf473c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "GPT-5.5 and GPT-5.5 Pro launch on Poe",
      "core_facts": [
        "GPT-5.5 and GPT-5.5 Pro are live on Poe. Internal evals show 12% higher task completion, 16% fewer retries, 19% better long-context performance."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_64809cd78c4445f9badf8d4fa1479a1c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "NotebookLM auto-label feature rollout",
      "core_facts": [
        "NotebookLM can auto-label and categorize sources when you have 5 or more."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_a5fb158d35eb43b09d155e11d80db5b6"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "open vs closed AI developments",
      "core_facts": [
        "It’s going to be a few very interesting weeks for open versus closed AI"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_df1053b501484fa581216d7ab5cd62cf"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Scott Wu shares deep dive by Walden Yan",
      "core_facts": [
        "Scott Wu praises a deep dive by Walden Yan."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_fa089d543d4042cc92216ad9a7691ac5"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Upcoming Ideogram announcement at noon ET tomorrow",
      "core_facts": [
        "Ideogram teases an announcement for tomorrow noon ET."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_51698d4a7d9242c6ab2a2ce69263c3f6"
      ]
    }
  ],
  "created_clusters": 25,
  "follow_up_event": {
    "false": 25
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 0,
  "relations": {
    "new_info": 18,
    "source_material": 7
  },
  "same_event": {
    "true": 25
  },
  "same_topic": {
    "true": 25
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 25,
  "top_clusters": [
    {
      "cluster_id": "cluster_4ee0132745934f1f94a7d9f5157d201b",
      "cluster_title": "Google DeepMind signs MoU with Korea Ministry of Science and ICT",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_c78fa846c6f54a21b0ee0880643bbb22",
      "cluster_title": "Qwen posts benchmark results",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_b810561cb5ef4b66a23f54971f28a4e4",
      "cluster_title": "Qdrant attending AI Dev Conference",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_72c65cc13dee41f2b3f7828b531ea40c",
      "cluster_title": "DeepSeek-V4-Pro discount extension and integration updates",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_66627fb2525e445ea79e82c8b7e99b2e",
      "cluster_title": "Working at Gumroad",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_af377301e1644eedb49ff4cfe995b44a",
      "cluster_title": "Release of Eleven Album Vol. 2",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_b715630397ec4a1a99c4446afa6117ba",
      "cluster_title": "Promotion of Skywork platform",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_a6267cdcf6d14d258e7260e8cbb55ee6",
      "cluster_title": "Lovable nearly reached 4,000-hour Discord chat record",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_a6b91f2f08d24db5b3d2d7b3cbc9e06d",
      "cluster_title": "Mustafa Suleyman's AI chip thought experiment",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_70da458980924a5da36aa27a9c175e86",
      "cluster_title": "Dify hands-on session at NYU Abu Dhabi",
      "item_count": 1
    }
  ],
  "uncertain_clusters": 0
}

## 8. Source Profile Summary

{
  "disabled_for_llm_candidates": [],
  "high_candidates": [],
  "llm_total_tokens_by_source": {
    "socialmedia-adam-d-angelo-adamdangelo": 0,
    "socialmedia-ai-at-meta-aiatmeta": 0,
    "socialmedia-ai-breakfast-aibreakfast": 0,
    "socialmedia-ai-sdk-aisdk": 0,
    "socialmedia-alex-albert-alexalbert": 0,
    "socialmedia-aman-sanger-amanrsanger": 0,
    "socialmedia-andrej-karpathy-karpathy": 0,
    "socialmedia-andrew-chen-andrewchen": 0,
    "socialmedia-andrew-ng-andrewyng": 0,
    "socialmedia-arthur-mensch-arthurmensch": 0,
    "socialmedia-barsee-128054-heybarsee": 0,
    "socialmedia-berkeley-ai-research-berkeley-ai": 0,
    "socialmedia-binyuan-hui-huybery": 0,
    "socialmedia-bolt-new-boltdotnew": 0,
    "socialmedia-cat-catwu": 0,
    "socialmedia-character-ai-character-ai": 0,
    "socialmedia-cohere-cohere": 0,
    "socialmedia-dario-amodei-darioamodei": 0,
    "socialmedia-deeplearning-ai-deeplearningai": 0,
    "socialmedia-deepseek-deepseek-ai": 0,
    "socialmedia-demis-hassabis-demishassabis": 0,
    "socialmedia-dia-diabrowser": 0,
    "socialmedia-dify-dify-ai": 0,
    "socialmedia-elevenlabs-elevenlabsio": 0,
    "socialmedia-eric-jing-ericjing-ai": 0,
    "socialmedia-fei-fei-li-drfeifei": 0,
    "socialmedia-fellou-fellouai": 0,
    "socialmedia-firecrawl-firecrawl-dev": 0,
    "socialmedia-fireworks-ai-fireworksai-hq": 0,
    "socialmedia-fish-audio-fishaudio": 0
  },
  "low_candidates": [
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 0.0,
      "priority_suggestion": "low",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-latent-space-latentspacepod",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 0.0,
      "priority_suggestion": "low",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    }
  ],
  "pending_reviews_created": 612,
  "sources_recomputed": 82,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-barsee-128054-heybarsee",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-deeplearning-ai-deeplearningai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-eric-jing-ericjing-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-fellou-fellouai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-firecrawl-firecrawl-dev",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-fireworks-ai-fireworksai-hq",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-google-ai-googleai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-hailuo-ai-minimax-hailuo-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-julien-chaumond-julien-c",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-lee-robinson-leerob",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-lovable-lovable-dev",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mem0-mem0ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-midjourney-midjourney",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ollama-ollama",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-replicate-replicate",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-sahil-lavingia-shl",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "normal",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "normal",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "normal",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "normal",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "normal",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-ng-andrewyng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "normal",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-deepseek-deepseek-ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-dify-dify-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-eric-jing-ericjing-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-fish-audio-fishaudio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-hugging-face-huggingface",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-deepseek-deepseek-ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-jim-fan-drjimfan",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-poe-poe-platform",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-deepseek-deepseek-ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-dify-dify-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-eric-jing-ericjing-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-fish-audio-fishaudio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    },
    {
      "created_at": "2026-05-16T18:47:05.379959+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-hugging-face-huggingface",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:47:05.379959+00:00"
    }
  ]
}

## 9. Token/Cost Summary

[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 24656.9,
    "cache_hit_tokens": 42624,
    "cache_miss_tokens": 0,
    "calls": 35,
    "failed": 0,
    "input_tokens": 107471,
    "llm_call_count": 35,
    "operation_count": 60,
    "output_tokens": 109401,
    "p50_latency_ms": 25292,
    "p95_latency_ms": 31053,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 25,
    "success": 35,
    "task_type": "item_card",
    "total_tokens": 216872
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 0.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 0,
    "failed": 0,
    "input_tokens": 0,
    "llm_call_count": 0,
    "operation_count": 289,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 289,
    "success": 0,
    "task_type": "item_relation",
    "total_tokens": 0
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 0.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 0,
    "failed": 0,
    "input_tokens": 0,
    "llm_call_count": 0,
    "operation_count": 264,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 264,
    "success": 0,
    "task_type": "item_cluster_relation",
    "total_tokens": 0
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 0.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 0,
    "failed": 0,
    "input_tokens": 0,
    "llm_call_count": 0,
    "operation_count": 28,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 28,
    "success": 0,
    "task_type": "cluster_card_patch",
    "total_tokens": 0
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 0.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 0,
    "failed": 0,
    "input_tokens": 0,
    "llm_call_count": 0,
    "operation_count": 0,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 0,
    "task_type": "cluster_card_rebuild",
    "total_tokens": 0
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 0.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 0,
    "failed": 0,
    "input_tokens": 0,
    "llm_call_count": 0,
    "operation_count": 0,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 0,
    "task_type": "source_review",
    "total_tokens": 0
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 0.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 0,
    "failed": 0,
    "input_tokens": 0,
    "llm_call_count": 0,
    "operation_count": 0,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 0,
    "task_type": "json_repair",
    "total_tokens": 0
  }
]

## 10. Errors/Fallbacks Summary

{
  "db_lock_errors": 0,
  "final_failures": 0,
  "llm_parse_failures": 0,
  "repair_retry_count": 0,
  "review_queue_entries_due_to_failure": 553,
  "skipped_due_to_max_calls": false,
  "skipped_due_to_missing_card": 0,
  "skipped_due_to_no_candidate": 0,
  "skipped_due_to_token_budget": false
}

## 11. Readiness Assessment

{
  "write_real_db_semantic_pass_recommended": false,
  "reasons": [
    "Final scoped ingest was not clean: 146/151 sources failed or timed out in the bounded pass, although net linked items improved from 728 to 782.",
    "At 300 items, heuristic_card fallback was 125/300 (>20%) because token budget was consumed during item cards.",
    "Final 300 run had no LLM item_relation calls and no multi-item clusters; relation/cluster quality is not sufficiently exercised at that scale.",
    "Source profile pending reviews were very high (612), indicating review aggregation/tuning is needed before production writes.",
    "Candidate recall improved and works on small/medium samples, but still lacks vector index and produces mostly single-item clusters."
  ],
  "next_recommended_fixes": [
    "Fix api.xgo.ing feed fetch latency/timeouts with source-level concurrency and robust per-source timeout reporting in the production ingest path.",
    "Reduce item_card token cost: smaller batch size or shorter inputs for social posts, stricter output fields, and reliable retry/repair logging.",
    "Make token budget stage-aware so item_relation and item_cluster_relation receive reserved budget after item_cards.",
    "Add vector or stronger entity index for relation/cluster candidates, then rerun source_scope_full.",
    "Aggregate source_profile review entries per source instead of many item-level pending reviews."
  ]
}

## 12. Whether Write-Real-DB Semantic Pass Is Recommended

No. See readiness blockers above.

## 13. Next Recommended Fixes

- Fix api.xgo.ing feed fetch latency/timeouts with source-level concurrency and robust per-source timeout reporting in the production ingest path.
- Reduce item_card token cost: smaller batch size or shorter inputs for social posts, stricter output fields, and reliable retry/repair logging.
- Make token budget stage-aware so item_relation and item_cluster_relation receive reserved budget after item_cards.
- Add vector or stronger entity index for relation/cluster candidates, then rerun source_scope_full.
- Aggregate source_profile review entries per source instead of many item-level pending reviews.

## Report Paths

{
  "probe_before_json": "outputs/semantic_eval/api_xgo_ing_probe_before_20260517_011815.json",
  "probe_after_json": "outputs/semantic_eval/api_xgo_ing_probe_after_20260517_015754.json",
  "ingest_json": "outputs/semantic_eval/api_xgo_ing_ingest_20260517_013814.json",
  "smoke_iter2_json": "outputs/semantic_eval/api_xgo_ing_smoke_c2_iter2/semantic_quality_summary.json",
  "required_smoke_json_initial": "outputs/semantic_eval/api_xgo_ing_smoke_c2/semantic_quality_summary.json",
  "full150_json": "outputs/semantic_eval/api_xgo_ing_full_150_c2/semantic_quality_summary.json",
  "comparison_json": "outputs/semantic_eval/api_xgo_ing_concurrency_comparison_20260517_024739.json",
  "final300_json": "outputs/semantic_eval/api_xgo_ing_full_300_final/semantic_quality_summary.json"
}
