# Phase 1.2d Review Bundle

## 1. Export metadata

- repo path: /Users/wangrundong/work/infomation-center
- git commit: b30e4834ebf710177acced15fca3e1befb97f550
- export time: 2026-05-17T06:23:12.897917+00:00
- DB path: /Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3
- backup path: None
- semantic run output dir: outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244
- evidence dir: outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244
- concurrency: 5
- scope: api.xgo.ing*
- write_real_db: False
- read-only export: True

## 2. Files included

- evidence zip: outputs/exports/phase1_2d_review_export_20260517_142312/phase1_2d_review_evidence.zip
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/semantic_items.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/semantic_items.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/item_cards.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/item_cards.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/item_card_failures.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/relations_all.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/relations_all.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/relations_interesting.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/relations_interesting.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/event_hotspots.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/event_hotspot_items.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/cluster_candidates.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/cluster_attachments.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/clusters_final.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/cluster_diagnostics.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/llm_calls.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/llm_errors.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/budget_skips.jsonl
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/stage_metrics.json
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/ingest_summary_phase1_2d.json
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/ingest_runs_phase1_2d.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/ingest_run_sources_phase1_2d.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/ingest_partial_write_suspects.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/items_added_phase1_2d.csv
- outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/items_added_by_source_phase1_2d.csv

## 3. Ingest summary

{
  "backup_path": null,
  "failures": 0,
  "ingest_performed": false,
  "item_delta": 0,
  "partial_write_suspects": 0,
  "phase": "phase1_2d",
  "reason": "Data was already refreshed in Phase 1.2c; this phase focused on dry-run evidence persistence.",
  "running_run_residue": "not_checked_no_ingest",
  "selected_sources": 0,
  "successes": 0,
  "timeouts": 0
}

## 4. Semantic coverage

{
  "clusters": {
    "actions": {
      "attach_to_cluster": 19
    },
    "attached_existing_clusters": 1,
    "avg_confidence": 0.618,
    "avg_items_per_cluster": 1.056,
    "candidate_clusters_considered": 18,
    "cluster_samples": [
      {
        "cluster_status": "active",
        "cluster_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
        "core_facts": [
          "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new research on how to actually structure AI use at work. msft.it/6016vKxQm Your browser does not support the video tag. 🔗 View on Twitter 💬 7 🔄 13 ❤️ 50 👀 9018 📊 18 ⚡ Powered by xgo.ing"
        ],
        "item_count": 2,
        "known_angles": [],
        "representative_items": [
          "item_153b053b4e2f4f7d845156e8b418851c"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "NVIDIA AI highlights local AI agent capability",
        "core_facts": [
          "NVIDIA AI shares a user experience of running a 121B model locally on DGX Spark via a Hermes agent that autonomously passed all tests."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_15c586321ecc435d84c9603a5c96de7e"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Ray Dalio on the battle between feelings and rational thinking",
        "core_facts": [
          "Ray Dalio discusses the internal battle between subconscious feelings (amygdala) and conscious rational thinking (prefrontal cortex)."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_8f18e494f5a14811ae5b5b2c41a9c28f"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Monica AI launches Claude 4.7 Opus and GPT Image 2",
        "core_facts": [
          "Monica AI announced the launch of Claude 4.7 Opus and GPT Image 2 on their platform."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_4d31618a325b457babfe6de93534a9e4"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "播客讨论：李想与老罗谈AI与商业",
        "core_facts": [
          "播客笔记记录李想与老罗关于AI、一人公司、增效降本、裁员、出海、具身智能、人的价值等话题的讨论。"
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_3965e6d5ecd14787aa50b9cda05a3672"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Mem0 and BasisSet announce 2026 AI Fellowship Agentic Memory Track",
        "core_facts": [
          "Mem0 partners with BasisSet for 2026 AI Fellowship Agentic Memory Track, applications due May 1."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_cbf825c399f3462e8e01444668c676f3"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "OpenAI builds sandbox for Codex on Windows",
        "core_facts": [
          "Detailed summary of OpenAI Codex sandbox for Windows, covering design iterations and final elevated sandbox solution."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_0ef913313e7040aba5790f2990e052fa"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Book release: The Book of Elon",
        "core_facts": [
          "Eric Jorgenson's 'The Book of Elon' launched, compiled from Elon Musk's public appearances."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_2ae8b16d066e4ce6803f040b7ad3524a"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Gemini API docs, cookbook, and Cloudflare worker example",
        "core_facts": [
          "Links to Gemini API docs, cookbook, and Cloudflare worker example repo."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_ef11c4ff68b140edb01534cb11a4aa18"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Qwen3.6-27B benchmark results",
        "core_facts": [
          "Qwen announces Qwen3.6-27B outperforming Qwen3.5-397B-A17B on SWE-bench Verified, SWE-bench Pro, Terminal-Bench 2.0, and SkillsBench."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_f1c16295e60c464ab1d12dc414e98358"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Case study of Datagraphs integrating Qdrant for Graph RAG",
        "core_facts": [
          "Qdrant presents a case study of Datagraphs, which built a knowledge graph platform integrating Qdrant for semantic search, highlighting complementary roles of vector and graph retrieval."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_97d257ff339f4c49a1ba251516d1dccd"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Qwen3.6 Plus achieves Code Arena #7 and Text Arena #36 improvements",
        "core_facts": [
          "Qwen3.6 Plus lands at #7 in Code Arena with score 1476, up 16 points, and at #36 in Text Arena, up 13 points. AlibabaGroup moves to #3 lab in Code Arena."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_beb942d4df9f410c938301d606a48137"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Satya Nadella reports Microsoft Copilot milestones",
        "core_facts": [
          "Satya Nadella reports over 20 million M365 Copilot seats, nearly 140,000 orgs using GitHub Copilot, and 2x increase in Security Copilot customers YoY."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_b1a9fa40cd1540ab8fac1aefdb1f272c"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Gemma 4 gets Multi-Token Prediction drafters",
        "core_facts": [
          "Multi-Token Prediction drafters are here for Gemma 4, making inference up to 3x faster with zero quality loss. Available for E2B and E4B versions under Apache 2.0 license."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_071af4614d46408c8e5e9d8f3ea01606"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Replit teases Episode 2 of Race To Revenue",
        "core_facts": [
          "Now it's time to really execute. Episode 2 is coming. Two builders, two wildly different bets. One building AI voice tools from a farm. The other turning bartending gigs into a career engine. Who hits revenue first? Race To Revenue out Wednesday. Don't miss it."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_c63c9cb40415424a95ef922becbc51f4"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "3D soft toy character 'FEEL MORE / THINK LESS' prompt",
        "core_facts": [
          "Prompt describes a 3D soft toy-like character with glossy texture, holding a floating heart, with typography 'FEEL MORE / THINK LESS' and caption 'emotion update v2'."
        ],
        "item_count": 1,
        "known_angles": [
          "The design combines a cute character with a philosophical message."
        ],
        "representative_items": [
          "item_187faea341af48678e92d006028e10b1"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Stanford SAIL and ETH demonstrate SDPO for RL with rich feedback",
        "core_facts": [
          "Stanford SAIL and ETH collaboration shows RL with rich feedback significantly outperforms scalar rewards on hard tasks, introducing SDPO."
        ],
        "item_count": 1,
        "known_angles": [
          "Rich feedback provides more granular signal for hard tasks than scalar rewards."
        ],
        "representative_items": [
          "item_eb48830993f3442688d0f4d4f262c974"
        ]
      },
      {
        "cluster_status": "active",
        "cluster_title": "Debate on AI's impact on labor market",
        "core_facts": [
          "Yann LeCun states that Dario (likely Dario Amodei) is wrong about AI's labor market effects and advises listening to economists."
        ],
        "item_count": 1,
        "known_angles": [],
        "representative_items": [
          "item_342aa6368b3f4c39bc3051fe86d68d4b"
        ]
      }
    ],
    "created_clusters": 18,
    "follow_up_event": {
      "false": 19
    },
    "manual_review_suggestions": {
      "high_uncertain": [],
      "possible_miscluster": [],
      "possible_missplit": [],
      "top_review_items_or_clusters": []
    },
    "multi_item_cluster_count": 1,
    "relations": {
      "new_info": 13,
      "repeat": 1,
      "source_material": 5
    },
    "same_event": {
      "true": 19
    },
    "same_topic": {
      "true": 19
    },
    "should_notify_count": 0,
    "should_update_cluster_card_count": 18,
    "top_clusters": [
      {
        "cluster_id": "cluster_4e7dc4612e0b4942805c884e47560f1a",
        "cluster_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
        "item_count": 2
      },
      {
        "cluster_id": "cluster_9a8723057cb646c18f98d692b6eeb192",
        "cluster_title": "NVIDIA AI highlights local AI agent capability",
        "item_count": 1
      },
      {
        "cluster_id": "cluster_3bfe3368634e4e9baed3a7131ebff5a3",
        "cluster_title": "Ray Dalio on the battle between feelings an

## 5. Item-card fallback/failure cases

- FAILURE item_c2f31709de764e72bb607ed80c5d85db | socialmedia-paul-couvert-itspaulai | This could solve the main issue with context windows Because this new model has a context window of... | llm_error: Unterminated string starting at: line 49 column 26 (char 2680)
- FAILURE item_733e18039ee240cba7e30c0c1161566d | socialmedia-richard-socher-richardsocher | Clawd/Molt/OpenClaw is the first glimpse of a personal AI for many people and that is the most amazi... | llm_error: Unterminated string starting at: line 49 column 26 (char 2680)
- FAILURE item_1f340940f86f4a22a5698039b0061da0 | socialmedia-scott-wu-scottwu46 | Katrin, Ola, and the whole @MercedesBenz team have been incredible partners already - excited to do... | llm_error: Unterminated string starting at: line 49 column 26 (char 2680)
- FAILURE item_0ce4945c216546108170bce10351cb1b | socialmedia-replicate-replicate | HappyHorse-1.0 from Alibaba is here. 🐎💨 This surprise 15B-parameter model has claimed the #1 spot... | llm_error: Unterminated string starting at: line 49 column 26 (char 2680)
- FAILURE item_94276ca377c24c0d8eda81bc68c1cfc9 | socialmedia-vista8 | 躺平神器开源！Xbox手柄秒变Mac万能遥控器~ 躺床上就能控制播放Youtube、B站视频，全屏、快进、快退、调整音量。 支持微信读书、浏览器，甚至任意Mac软件Tab切换，上下滚动、翻页等操作... | llm_error: Unterminated string starting at: line 49 column 26 (char 2680)
- FAILURE item_13670ebf245448e8bb16e5d333ebefaa | socialmedia-the-rundown-ai-therundownai | Announcement from Anthropic: https://t.co/90LWwzgOLK Original scoop from WSJ: https://t.co/ml8HQLZa... | timeout: DeepSeek request failed: The read operation timed out
- FAILURE item_da4cfaea117448de90c3283d76aaca64 | socialmedia-paul-graham-paulg | You can't get the same effect from the "Innovation Center" set up by the provincial government. You ... | timeout: DeepSeek request failed: The read operation timed out
- FAILURE item_e763c05e913842a383031796bba2276f | socialmedia-poe-poe-platform | Alibaba's Wan 2.7-Image is now live on Poe. Generate a cohesive set of images from a single prompt ... | timeout: DeepSeek request failed: The read operation timed out
- FAILURE item_187faea341af48678e92d006028e10b1 | socialmedia-recraft-recraftai | Prompt 1: 3D soft toy-like character with glossy texture and a slightly uncanny smile, holding a flo... | timeout: DeepSeek request failed: The read operation timed out
- FAILURE item_72f476a0be454dd28d77cf45787a3a84 | socialmedia-sundar-pichai-sundarpichai | You can now ask Gemini to create Docs, Sheets, Slides, PDFs, and more directly in your chat. No more... | timeout: DeepSeek request failed: The read operation timed out
- FAILURE item_be8b6bac777f4a4482d8558cc725dc20 | socialmedia-replicate-replicate | Try Granite 4.1 here 👇 Language: https://t.co/5EWzEgRFk5 Speech: https://t.co/AiVdlV1vGj | llm_error: Expecting value: line 1 column 1 (char 0)
- FAILURE item_a3b6607d6b14432fb8c62679db210654 | socialmedia-satya-nadella-satyanadella | 3/ These same capabilities also show up in everyday work. In M365 Copilot, we support multiple mode... | llm_error: Expecting value: line 1 column 1 (char 0)
- FAILURE item_9fe692cffac2452e8391e8d1f03edccd | socialmedia-richard-socher-richardsocher | Oh no. The "soulless music machine" will take all the musicians' jobs! ... Actually, we have more mu... | llm_error: Expecting value: line 1 column 1 (char 0)
- FAILURE item_7efc985f8fa94eb49a9362ae6dcadb5a | socialmedia-suhail-suhail | I spent a ton of time exploring everything from interning at a Robotics Startup to Lunar Space Rover... | llm_error: Expecting value: line 1 column 1 (char 0)
- FAILURE item_ac395ce086e749cea879e698dae595d4 | socialmedia-runway-runwayml | It used to take a miracle to bring an idea to life. Now all it needs is your point of view. Every po... | llm_error: Expecting value: line 1 column 1 (char 0)
- FAILURE item_023cc431a62b4c13ab300e0c4d05bea7 | socialmedia-taranjeet-taranjeetio | We just crossed 100k developers using Mem0 What began as an experiment to solve AI amnesia problem ... | llm_error: Unterminated string starting at: line 76 column 25 (char 6918)
- FAILURE item_17492a1440a04e5a8ea885ff3b802b37 | socialmedia-thomas-wolf-thom-wolf | Codexing games together with my 12 yo has been a surprisingly fun dad-son activity over the past cou... | llm_error: Unterminated string starting at: line 76 column 25 (char 6918)
- FAILURE item_1f48d169a9c24da182419dfbd32be9c5 | socialmedia-the-rundown-ai-therundownai | Also today: OpenAI starting its own $10 B venture reportedly called "The Deployment Company". Big d... | llm_error: Unterminated string starting at: line 76 column 25 (char 6918)
- FAILURE item_9ec086b4c8224cf6ac585973541f0e7e | socialmedia-thomas-wolf-thom-wolf | wow! | llm_error: Unterminated string starting at: line 76 column 25 (char 6918)
- FAILURE item_1202c2c321fe4f74b950f97aeb33434b | socialmedia-yann-lecun-ylecun | The tensor engine was first implemented inside SN3 (before it was called Lush) in 1992 at Bell Labs ... | llm_error: Unterminated string starting at: line 76 column 25 (char 6918)
- FAILURE item_87d4ee35b02a42e7a7a30a8a00bad4c2 | socialmedia-varun-mohan-mohansolo | Just to add some clarification, we have purely blocked usage of the Antigravity product for these us... | llm_error: Unterminated string starting at: line 105 column 18 (char 7066)
- FAILURE item_b05b1f45684e44cf9aee2961031278bb | socialmedia-weaviate-vector-database-weaviate-io | Production-ready legal AI within 24 hours. Here's the technical breakdown of how we did it for our ... | llm_error: Unterminated string starting at: line 105 column 18 (char 7066)
- FAILURE item_664b1512a1664ac5a08ffca1f3d85c1d | socialmedia-weaviate-vector-database-weaviate-io | PDF import just landed in Weaviate Agent Skills! Point Claude Code (or any agent) at a PDF, and it ... | llm_error: Unterminated string starting at: line 105 column 18 (char 7066)
- FAILURE item_7a515f49240b46dbab966cf186996af3 | socialmedia-weaviate-vector-database-weaviate-io | Your AI agents are burning tokens solving the same problems over and over. Long context windows won... | llm_error: Unterminated string starting at: line 105 column 18 (char 7066)
- FAILURE item_5cffe86b665c44e996a44ac0319acab4 | socialmedia-weaviate-vector-database-weaviate-io | Weaviate 1.37 is here 🚀 and it makes your database a first-class citizen of the agentic-AI stack wi... | llm_error: Unterminated string starting at: line 105 column 18 (char 7066)

Fallback count in bundle: 25. First 50:
- item_023cc431a62b4c13ab300e0c4d05bea7 | socialmedia-taranjeet-taranjeetio | We just crossed 100k developers using Mem0 What began as an experiment to solve AI amnesia problem ... | LLM skipped or failed
- item_0ce4945c216546108170bce10351cb1b | socialmedia-replicate-replicate | HappyHorse-1.0 from Alibaba is here. 🐎💨 This surprise 15B-parameter model has claimed the #1 spot... | LLM skipped or failed
- item_1202c2c321fe4f74b950f97aeb33434b | socialmedia-yann-lecun-ylecun | The tensor engine was first implemented inside SN3 (before it was called Lush) in 1992 at Bell Labs ... | LLM skipped or failed
- item_13670ebf245448e8bb16e5d333ebefaa | socialmedia-the-rundown-ai-therundownai | Announcement from Anthropic: https://t.co/90LWwzgOLK Original scoop from WSJ: https://t.co/ml8HQLZa... | LLM skipped or failed
- item_17492a1440a04e5a8ea885ff3b802b37 | socialmedia-thomas-wolf-thom-wolf | Codexing games together with my 12 yo has been a surprisingly fun dad-son activity over the past cou... | LLM skipped or failed
- item_187faea341af48678e92d006028e10b1 | socialmedia-recraft-recraftai | Prompt 1: 3D soft toy-like character with glossy texture and a slightly uncanny smile, holding a flo... | LLM skipped or failed
- item_1f340940f86f4a22a5698039b0061da0 | socialmedia-scott-wu-scottwu46 | Katrin, Ola, and the whole @MercedesBenz team have been incredible partners already - excited to do... | LLM skipped or failed
- item_1f48d169a9c24da182419dfbd32be9c5 | socialmedia-the-rundown-ai-therundownai | Also today: OpenAI starting its own $10 B venture reportedly called "The Deployment Company". Big d... | LLM skipped or failed
- item_5cffe86b665c44e996a44ac0319acab4 | socialmedia-weaviate-vector-database-weaviate-io | Weaviate 1.37 is here 🚀 and it makes your database a first-class citizen of the agentic-AI stack wi... | LLM skipped or failed
- item_664b1512a1664ac5a08ffca1f3d85c1d | socialmedia-weaviate-vector-database-weaviate-io | PDF import just landed in Weaviate Agent Skills! Point Claude Code (or any agent) at a PDF, and it ... | LLM skipped or failed
- item_72f476a0be454dd28d77cf45787a3a84 | socialmedia-sundar-pichai-sundarpichai | You can now ask Gemini to create Docs, Sheets, Slides, PDFs, and more directly in your chat. No more... | LLM skipped or failed
- item_733e18039ee240cba7e30c0c1161566d | socialmedia-richard-socher-richardsocher | Clawd/Molt/OpenClaw is the first glimpse of a personal AI for many people and that is the most amazi... | LLM skipped or failed
- item_7a515f49240b46dbab966cf186996af3 | socialmedia-weaviate-vector-database-weaviate-io | Your AI agents are burning tokens solving the same problems over and over. Long context windows won... | LLM skipped or failed
- item_7efc985f8fa94eb49a9362ae6dcadb5a | socialmedia-suhail-suhail | I spent a ton of time exploring everything from interning at a Robotics Startup to Lunar Space Rover... | LLM skipped or failed
- item_87d4ee35b02a42e7a7a30a8a00bad4c2 | socialmedia-varun-mohan-mohansolo | Just to add some clarification, we have purely blocked usage of the Antigravity product for these us... | LLM skipped or failed
- item_94276ca377c24c0d8eda81bc68c1cfc9 | socialmedia-vista8 | 躺平神器开源！Xbox手柄秒变Mac万能遥控器~ 躺床上就能控制播放Youtube、B站视频，全屏、快进、快退、调整音量。 支持微信读书、浏览器，甚至任意Mac软件Tab切换，上下滚动、翻页等操作... | LLM skipped or failed
- item_9ec086b4c8224cf6ac585973541f0e7e | socialmedia-thomas-wolf-thom-wolf | wow! | LLM skipped or failed
- item_9fe692cffac2452e8391e8d1f03edccd | socialmedia-richard-socher-richardsocher | Oh no. The "soulless music machine" will take all the musicians' jobs! ... Actually, we have more mu... | LLM skipped or failed
- item_a3b6607d6b14432fb8c62679db210654 | socialmedia-satya-nadella-satyanadella | 3/ These same capabilities also show up in everyday work. In M365 Copilot, we support multiple mode... | LLM skipped or failed
- item_ac395ce086e749cea879e698dae595d4 | socialmedia-runway-runwayml | It used to take a miracle to bring an idea to life. Now all it needs is your point of view. Every po... | LLM skipped or failed
- item_b05b1f45684e44cf9aee2961031278bb | socialmedia-weaviate-vector-database-weaviate-io | Production-ready legal AI within 24 hours. Here's the technical breakdown of how we did it for our ... | LLM skipped or failed
- item_be8b6bac777f4a4482d8558cc725dc20 | socialmedia-replicate-replicate | Try Granite 4.1 here 👇 Language: https://t.co/5EWzEgRFk5 Speech: https://t.co/AiVdlV1vGj | LLM skipped or failed
- item_c2f31709de764e72bb607ed80c5d85db | socialmedia-paul-couvert-itspaulai | This could solve the main issue with context windows Because this new model has a context window of... | LLM skipped or failed
- item_da4cfaea117448de90c3283d76aaca64 | socialmedia-paul-graham-paulg | You can't get the same effect from the "Innovation Center" set up by the provincial government. You ... | LLM skipped or failed
- item_e763c05e913842a383031796bba2276f | socialmedia-poe-poe-platform | Alibaba's Wan 2.7-Image is now live on Poe. Generate a cohesive set of images from a single prompt ... | LLM skipped or failed

## 6. Relation evidence

### near_duplicate

count: 4
- A: 🚀 Monica 9.0 is LIVE now Meet Monica Agent, your most powerful agent yet. Deep Research: Research... (Monica_IM(@hey_im_monica), 2026-01-14T07:58:09+00:00)
  B: 🚀 Monica 9.0 is LIVE now Meet Monica Agent, your most powerful agent yet. Deep Research: Research... (Monica_IM(@hey_im_monica), 2026-01-14T10:52:31+00:00)
  confidence=1.0 should_fold=True reason=deterministic duplicate rule matched
- A: 🚀 Monica 9.0 is LIVE now Meet Monica Agent, your most powerful agent yet. Deep Research: Research... (Monica_IM(@hey_im_monica), 2026-01-14T10:52:31+00:00)
  B: 🚀 Monica 9.0 is LIVE now Meet Monica Agent, your most powerful agent yet. Deep Research: Research... (Monica_IM(@hey_im_monica), 2026-01-14T07:58:09+00:00)
  confidence=1.0 should_fold=True reason=deterministic duplicate rule matched
- A: 🚀 Introducing FlashQLA: high-performance linear attention kernels built on TileLang. ⚡ 2–3× forwar... (Qwen(@Alibaba_Qwen), 2026-04-29T12:15:51+00:00)
  B: 🚀 Introducing FlashQLA: high-performance linear attention kernels built on TileLang. ⚡ 2–3× forwar... (Qwen(@Alibaba_Qwen), 2026-04-29T12:16:13+00:00)
  confidence=1.0 should_fold=True reason=deterministic duplicate rule matched
- A: 🚀 Introducing FlashQLA: high-performance linear attention kernels built on TileLang. ⚡ 2–3× forwar... (Qwen(@Alibaba_Qwen), 2026-04-29T12:16:13+00:00)
  B: 🚀 Introducing FlashQLA: high-performance linear attention kernels built on TileLang. ⚡ 2–3× forwar... (Qwen(@Alibaba_Qwen), 2026-04-29T12:15:51+00:00)
  confidence=1.0 should_fold=True reason=deterministic duplicate rule matched

### related_with_new_info

count: 24
- A: Recraft V4 helps you create expressive, story-driven scenes full of awkward timing, emotional chaos,... (Recraft(@recraftai), 2026-05-11T09:54:46+00:00)
  B: Playful 3D characters, bold type, instant mood. Made in Recraft V4. Prompts ↓ (Recraft(@recraftai), 2026-05-04T11:31:35+00:00)
  confidence=0.9 should_fold=False reason=Both about Recraft V4 and prompts, but new item adds specific style descriptions.
- A: Hallelujah I found something but I won’t reveal due to selfish gpu hoarding. (Suhail(@Suhail), 2026-03-20T03:59:12+00:00)
  B: Having trouble finding 1 8xH100 today to launch some experiments I am working on. If you know of a p... (Suhail(@Suhail), 2026-03-19T20:53:02+00:00)
  confidence=0.9 should_fold=False reason=Same person reporting resolution of GPU availability issue.
- A: Third Skill: UGC Ads Have your agent promote your project (or anything, really). Input for this vid... (Pika(@pika_labs), 2026-05-01T19:20:28+00:00)
  B: Meet Skywork with Hermes Agent capabilities. An agent that evolves with you. Turn routine tasks i... (Skywork(@Skywork_ai), 2026-04-30T11:31:32+00:00)
  confidence=0.7 should_fold=False reason=Both items discuss agent skills. The candidate introduces Skywork with Hermes Agent capabilities; the new item details a specific skill (UGC Ads) that can be performed by an agent, adding new, specific information.
- A: You can give Replit Agent 4 a try right here: https://t.co/BHgQ5SUFxb (And you’re getting $10 credi... (Paul Couvert(@itsPaulAi), 2026-05-01T15:22:59+00:00)
  B: 3 things you can build for $0 on May 2nd: your website, your research, your internal systems. We’re... (Replit ⠕(@Replit), 2026-05-02T13:01:09+00:00)
  confidence=0.75 should_fold=False reason=Both about Replit Agent promotion; new item adds referral link and credit incentive, targets Agent 4 specifically.
- A: Watching @jarredsumner and @bcherny at Code w/ Code talking about robobun, the Bun project's GitHub ... (Simon Willison(@simonw), 2026-05-06T21:08:17+00:00)
  B: Sure looks like Bun is at least exploring a port from Zig to Rust given this docs/PORTING.md guide f... (Simon Willison(@simonw), 2026-05-05T01:39:37+00:00)
  confidence=0.6 should_fold=False reason=Both involve Bun project; new item adds distinct information about a specific bot and its contributions.
- A: DeepSeek v4 Pro还是可以的。 几轮对话，实现一个工具，用xbox手柄控制电脑应用和浏览器。 当遥控器，躺床上刷小说和看视频。 (向阳乔木(@vista8), 2026-05-04T09:33:29+00:00)
  B: 躺平神器开源！Xbox手柄秒变Mac万能遥控器~ 躺床上就能控制播放Youtube、B站视频，全屏、快进、快退、调整音量。 支持微信读书、浏览器，甚至任意Mac软件Tab切换，上下滚动、翻页等操作... (向阳乔木(@vista8), 2026-05-04T14:03:51+00:00)
  confidence=0.85 should_fold=False reason=Both items describe the same Xbox controller tool for Mac, but the new item specifically highlights its creation using DeepSeek v4 Pro and provides a firsthand experience, adding new information about the generative process.
- A: Make anything. From anywhere. On any device. Runway is now on both Android and iOS. Get started at ... (Runway(@runwayml), 2026-05-01T17:47:51+00:00)
  B: It used to take a miracle to bring an idea to life. Now all it needs is your point of view. Every po... (Runway(@runwayml), 2026-05-04T14:09:41+00:00)
  confidence=0.7 should_fold=False reason=Both items are about Runway, but new item adds mobile app availability.
- A: I had Claude Code for web build me this WebAssembly playground for trying out the new Redis array co... (Simon Willison(@simonw), 2026-05-04T17:08:48+00:00)
  B: New Redis data type just dropped - arrays, accessible by index, with a new text grep search mechanis... (Simon Willison(@simonw), 2026-05-04T14:37:25+00:00)
  confidence=0.85 should_fold=False reason=Both cover the new Redis array type, but the new item adds a hands-on WebAssembly playground and personal notes.
- A: Source via Meta: https://t.co/l22aISUzys I break down stories like this every day in my free newsle... (Rowan Cheung(@rowancheung), 2026-05-04T15:18:21+00:00)
  B: Top stories in robotics today: - Meta snaps up robotics startup ARI - 1X opens massive NEO humanoid... (The Rundown AI(@TheRundownAI), 2026-05-04T15:30:10+00:00)
  confidence=0.92 should_fold=False reason=Both cover Meta's robotics startup acquisition; new item adds the original source link.
- A: Research paper link: https://t.co/XPbDNPcU6m I break down stories like this every day in my free ne... (Rowan Cheung(@rowancheung), 2026-04-13T15:13:38+00:00)
  B: Source via Meta: https://t.co/l22aISUzys I break down stories like this every day in my free newsle... (Rowan Cheung(@rowancheung), 2026-05-04T15:18:21+00:00)
  confidence=0.55 should_fold=False reason=Same promotional post but adds a research paper link.
- A: Research paper link: https://t.co/XPbDNPcU6m I break down stories like this every day in my free ne... (Rowan Cheung(@rowancheung), 2026-04-13T15:13:38+00:00)
  B: I break down stories like this every day in my free newsletter. Keep up with the latest in AI/Roboti... (Rowan Cheung(@rowancheung), 2026-04-09T15:17:33+00:00)
  confidence=0.55 should_fold=False reason=Same promotional post but adds a research paper link.
- A: Research paper link: https://t.co/XPbDNPcU6m I break down stories like this every day in my free ne... (Rowan Cheung(@rowancheung), 2026-04-13T15:13:38+00:00)
  B: Try it now for free: https://t.co/y7IZARLPZ5 (xAI(@xai), 2026-04-23T22:23:20+00:00)
  confidence=0.55 should_fold=False reason=Same promotional post but adds a research paper link.
- A: Research paper link: https://t.co/XPbDNPcU6m I break down stories like this every day in my free ne... (Rowan Cheung(@rowancheung), 2026-04-13T15:13:38+00:00)
  B: Read more: https://t.co/yZgH0hEATU (The Rundown AI(@TheRundownAI), 2026-05-13T10:30:20+00:00)
  confidence=0.55 should_fold=False reason=Same promotional post but adds a research paper link.
- A: Research paper link: https://t.co/XPbDNPcU6m I break down stories like this every day in my free ne... (Rowan Cheung(@rowancheung), 2026-04-13T15:13:38+00:00)
  B: https://t.co/cfwFhKL5Aw (Yann LeCun(@ylecun), 2026-05-02T20:07:19+00:00)
  confidence=0.55 should_fold=False reason=Same promotional post but adds a research paper link.
- A: Learn more about building Runway Characters: https://t.co/TLg3XBH544 (Runway(@runwayml), 2026-05-04T17:30:29+00:00)
  B: It used to take a miracle to bring an idea to life. Now all it needs is your point of view. Every po... (Runway(@runwayml), 2026-05-04T14:09:41+00:00)
  confidence=0.7 should_fold=False reason=Both about Runway, but new item focuses on building characters, while candidate promotes Runway Academy for film/ad generation.
- A: Your agent can now add memory with @mem0ai CLI Agent-first and seamlessly integrated with your stack... (Taranjeet(@taranjeetio), 2026-04-08T19:19:17+00:00)
  B: This is what token-efficient memory looks like @mem0ai You can now run agent memory that is cost-e... (Taranjeet(@taranjeetio), 2026-04-16T18:08:20+00:00)
  confidence=0.7 should_fold=False reason=Both refer to mem0ai and agent memory, but the new item introduces a CLI tool for adding memory, which is not present in the candidate.
- A: This is what token-efficient memory looks like @mem0ai You can now run agent memory that is cost-e... (Taranjeet(@taranjeetio), 2026-04-16T18:08:20+00:00)
  B: Your agent can now add memory with @mem0ai CLI Agent-first and seamlessly integrated with your stack... (Taranjeet(@taranjeetio), 2026-04-08T19:19:17+00:00)
  confidence=0.85 should_fold=False reason=Both items discuss mem0ai agent memory. New item adds token efficiency and cost-efficiency information.
- A: Introducing Windsurf 2.0. Manage all your agents from one place and delegate work to the cloud with... (Windsurf(@windsurf_ai), 2026-04-15T20:28:31+00:00)
  B: Download the latest version of Windsurf to try the Agent Command Center, Spaces, and Devin: https://... (Windsurf(@windsurf_ai), 2026-04-15T20:28:32+00:00)
  confidence=0.85 should_fold=False reason=Both items are about Windsurf and mention Devin, but the new item is an announcement of version 2.0 with additional features not present in the candidate's download prompt.
- A: Download the latest version of Windsurf to try the Agent Command Center, Spaces, and Devin: https://... (Windsurf(@windsurf_ai), 2026-04-15T20:28:32+00:00)
  B: Introducing Windsurf 2.0. Manage all your agents from one place and delegate work to the cloud with... (Windsurf(@windsurf_ai), 2026-04-15T20:28:31+00:00)
  confidence=0.85 should_fold=False reason=Same product launch, new item adds download link and blog post reference.
- A: Download the latest version of Windsurf to try the Agent Command Center, Spaces, and Devin: https://... (Windsurf(@windsurf_ai), 2026-04-15T20:28:32+00:00)
  B: Devin runs in its own VM in the cloud. You plan locally, delegate to Devin with one click, and keep... (Windsurf(@windsurf_ai), 2026-04-15T20:28:32+00:00)
  confidence=0.75 should_fold=False reason=Same event, new item provides access to the update.
- A: Download the latest version of Windsurf to try the Agent Command Center, Spaces, and Devin: https://... (Windsurf(@windsurf_ai), 2026-04-15T20:28:32+00:00)
  B: Devin for Terminal is available for all Windsurf users, and can even be used directly from Windsurf ... (Windsurf(@windsurf_ai), 2026-04-27T18:56:43+00:00)
  confidence=0.75 should_fold=False reason=Same event, new item provides access to the update.
- A: We've partnered with @OpenAI to offer GPT-5.5 in Windsurf at 50% off through May 14 starting today. (Windsurf(@windsurf_ai), 2026-04-30T17:14:35+00:00)
  B: GPT-5.5 is now available in Windsurf 2.0! (Windsurf(@windsurf_ai), 2026-04-24T18:23:35+00:00)
  confidence=0.75 should_fold=False reason=Both concern GPT-5.5 availability in Windsurf, but new item adds partnership and discount details.
- A: We've partnered with @OpenAI to offer GPT-5.5 in Windsurf at 50% off through May 14 starting today. (Windsurf(@windsurf_ai), 2026-04-30T17:14:35+00:00)
  B: GPT-5.5 is a giant leap forward for handling ambiguity compared to previous GPT models. As Windsurf ... (Windsurf(@windsurf_ai), 2026-04-24T18:23:36+00:00)
  confidence=0.7 should_fold=False reason=Both promote GPT-5.5 in Windsurf, but new item adds specific promotional details.
- A: Tools give your Custom Agents capabilities that Notion and MCP don’t cover on their own. Write your ... (Notion(@NotionHQ), 2026-05-13T16:27:37+00:00)
  B: Notion 终于出了 CLI… 跟上了这个时代 (orange.ai(@oran_ge), 2026-05-16T06:44:39+00:00)
  confidence=0.85 should_fold=False reason=New item adds specific detail about custom agents using Workers, an extension of the same launch.

### uncertain

count: 2
- A: Read more: https://t.co/3YEhHmqg3g (The Rundown AI(@TheRundownAI), 2026-05-04T15:30:11+00:00)
  B: Source via Meta: https://t.co/l22aISUzys I break down stories like this every day in my free newsle... (Rowan Cheung(@rowancheung), 2026-05-04T15:18:21+00:00)
  confidence=0.5 should_fold=False reason=Both mention Meta and robotics, but the candidate is a source link and the new item is a news summary; it's unclear if they refer to the same event.
- A: Curious what people are running locally these days 👀 (NVIDIA AI(@NVIDIAAI), 2026-05-13T13:31:37+00:00)
  B: Meet Skywork with Hermes Agent capabilities. An agent that evolves with you. Turn routine tasks i... (Skywork(@Skywork_ai), 2026-04-30T11:31:32+00:00)
  confidence=0.5 should_fold=False reason=Both mention 'Hermes Agent', but candidate is about Skywork with Hermes Agent capabilities, while new item is about NVIDIA AI showcasing a local agent on DGX Spark. Insufficient evidence to determine relation.

### suspicious_different_sample

count: 30
- A: Source via Meta: https://t.co/l22aISUzys I break down stories like this every day in my free newsle... (Rowan Cheung(@rowancheung), 2026-05-04T15:18:21+00:00)
  B: Research paper link: https://t.co/XPbDNPcU6m I break down stories like this every day in my free ne... (Rowan Cheung(@rowancheung), 2026-04-13T15:13:38+00:00)
  confidence=0.95 should_fold=False reason=Different topics: new item about Meta news, candidate about research paper.
- A: Source via Meta: https://t.co/l22aISUzys I break down stories like this every day in my free newsle... (Rowan Cheung(@rowancheung), 2026-05-04T15:18:21+00:00)
  B: I break down stories like this every day in my free newsletter. Keep up with the latest in AI/Roboti... (Rowan Cheung(@rowancheung), 2026-04-09T15:17:33+00:00)
  confidence=0.95 should_fold=False reason=Different content: new item specifically about Meta source, candidate generic newsletter promotion.
- A: I break down stories like this every day in my free newsletter. Keep up with the latest in AI/Roboti... (Rowan Cheung(@rowancheung), 2026-04-09T15:17:33+00:00)
  B: Source via Meta: https://t.co/l22aISUzys I break down stories like this every day in my free newsle... (Rowan Cheung(@rowancheung), 2026-05-04T15:18:21+00:00)
  confidence=0.5 should_fold=False reason=New item is a generic newsletter promotion; candidate is about a specific Meta source.
- A: I break down stories like this every day in my free newsletter. Keep up with the latest in AI/Roboti... (Rowan Cheung(@rowancheung), 2026-04-09T15:17:33+00:00)
  B: Research paper link: https://t.co/XPbDNPcU6m I break down stories like this every day in my free ne... (Rowan Cheung(@rowancheung), 2026-04-13T15:13:38+00:00)
  confidence=0.5 should_fold=False reason=New item is a generic newsletter promotion; candidate is about a research paper link.
- A: Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config... (OpenAI(@OpenAI), 2026-05-01T19:05:50+00:00)
  B: You can now ask Gemini to create Docs, Sheets, Slides, PDFs, and more directly in your chat. No more... (Sundar Pichai(@sundarpichai), 2026-04-29T16:00:49+00:00)
  confidence=0.95 should_fold=False reason=The new item is about Codex workflow import, while the candidate is about Gemini integration with Docs/Sheets - unrelated.
- A: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear... (Microsoft Research(@MSFTResearch), 2026-05-04T16:57:40+00:00)
  B: Introducing Windsurf 2.0. Manage all your agents from one place and delegate work to the cloud with... (Windsurf(@windsurf_ai), 2026-04-15T20:28:31+00:00)
  confidence=0.95 should_fold=False reason=The new item discusses AI agents leaking data, a smarter OS, and structuring AI use at work, which are unrelated to the candidate's content about Windsurf 2.0.
- A: Introducing Windsurf 2.0. Manage all your agents from one place and delegate work to the cloud with... (Windsurf(@windsurf_ai), 2026-04-15T20:28:31+00:00)
  B: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear... (Microsoft Research(@MSFTResearch), 2026-05-04T16:57:40+00:00)
  confidence=0.95 should_fold=False reason=Candidate item is about AI agents leaking data and other research topics, unrelated to Windsurf.
- A: Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config... (OpenAI(@OpenAI), 2026-05-01T19:05:50+00:00)
  B: Introducing Windsurf 2.0. Manage all your agents from one place and delegate work to the cloud with... (Windsurf(@windsurf_ai), 2026-04-15T20:28:31+00:00)
  confidence=0.95 should_fold=False reason=The new item is about Codex workflow import, while the candidate is about Windsurf 2.0 - unrelated products/services.
- A: Introducing Windsurf 2.0. Manage all your agents from one place and delegate work to the cloud with... (Windsurf(@windsurf_ai), 2026-04-15T20:28:31+00:00)
  B: Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config... (OpenAI(@OpenAI), 2026-05-01T19:05:50+00:00)
  confidence=0.95 should_fold=False reason=Candidate item is about bringing workflow to Codex, unrelated to Windsurf.
- A: Perplexity Computer is now available in Microsoft Teams. Run research, analysis, and document creat... (Perplexity(@perplexity_ai), 2026-05-04T18:05:59+00:00)
  B: You can now ask Gemini to create Docs, Sheets, Slides, PDFs, and more directly in your chat. No more... (Sundar Pichai(@sundarpichai), 2026-04-29T16:00:49+00:00)
  confidence=0.95 should_fold=False reason=The new item is about Perplexity Computer integration with Microsoft Teams, while the candidate is about Gemini creating documents. No shared entities or events.
- A: Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config... (OpenAI(@OpenAI), 2026-05-01T19:05:50+00:00)
  B: You can build a full pitch deck in Replit without touching a single slide. Just describe what you w... (Replit ⠕(@Replit), 2026-05-04T19:00:28+00:00)
  confidence=0.95 should_fold=False reason=The new item is about Codex workflow import, while the candidate is about Replit pitch deck feature - unrelated.
- A: https://t.co/iMifqBlNHZ (Philipp Schmid(@_philschmid), 2026-04-30T13:34:47+00:00)
  B: wow! (Thomas Wolf(@Thom_Wolf), 2026-03-14T17:05:13+00:00)
  confidence=0.1 should_fold=False reason=New item is about a workflow demo for Stripe Link; candidate is about an open-source dataset. No shared entities or event.
- A: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear... (Microsoft Research(@MSFTResearch), 2026-05-04T16:57:40+00:00)
  B: wow! (Thomas Wolf(@Thom_Wolf), 2026-03-14T17:05:13+00:00)
  confidence=0.95 should_fold=False reason=The new item discusses AI agents leaking data, a smarter OS, and structuring AI use at work, which are unrelated to the candidate's content about an open-source dataset of computer-use recordings.
- A: Create with GPT Image 2 in Skywork. Claim your gift from Skywork by RT, Like, Quote, & Subscr... (Skywork(@Skywork_ai), 2026-04-28T12:31:35+00:00)
  B: Bullet time, generated. Made with Seedance 2.0 in Skywork. (Skywork(@Skywork_ai), 2026-04-29T13:44:14+00:00)
  confidence=0.95 should_fold=False reason=Different products: Seedance 2.0 vs GPT Image 2; distinct events.
- A: Bullet time, generated. Made with Seedance 2.0 in Skywork. (Skywork(@Skywork_ai), 2026-04-29T13:44:14+00:00)
  B: Create with GPT Image 2 in Skywork. Claim your gift from Skywork by RT, Like, Quote, & Subscr... (Skywork(@Skywork_ai), 2026-04-28T12:31:35+00:00)
  confidence=0.9 should_fold=False reason=New item is about Seedance 2.0, candidate about GPT Image 2 promotion. Only common entity is 'Skywork' but in different contexts.
- A: Check out our latest SAIL blog post on VAGEN, a reinforcement learning framework that trains VLM age... (Stanford AI Lab(@StanfordAILab), 2026-03-09T22:10:59+00:00)
  B: Can AI actively explore and build mental maps of space, or just answer when handed observations? C... (Stanford AI Lab(@StanfordAILab), 2026-02-26T00:28:14+00:00)
  confidence=0.95 should_fold=False reason=Both are SAIL blog posts but about different topics: Theory of Space benchmark vs VAGEN RL framework.
- A: Create with GPT Image 2 in Skywork. Claim your gift from Skywork by RT, Like, Quote, & Subscr... (Skywork(@Skywork_ai), 2026-04-28T12:31:35+00:00)
  B: You can now ask Gemini to create Docs, Sheets, Slides, PDFs, and more directly in your chat. No more... (Sundar Pichai(@sundarpichai), 2026-04-29T16:00:49+00:00)
  confidence=0.95 should_fold=False reason=Different products: Gemini vs GPT Image 2; distinct events.
- A: Third Skill: UGC Ads Have your agent promote your project (or anything, really). Input for this vid... (Pika(@pika_labs), 2026-05-01T19:20:28+00:00)
  B: Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config... (OpenAI(@OpenAI), 2026-05-01T19:05:50+00:00)
  confidence=0.95 should_fold=False reason=New item is about UGC Ads agent skill; candidate is about importing workflow to Codex. Different topics.
- A: SF Happy Hour on April 28 In town for AI Dev? Come hang with the Qdrant team 👇 → Meet builders → ... (Qdrant(@qdrant_engine), 2026-04-23T16:00:02+00:00)
  B: Meet Skywork with Hermes Agent capabilities. An agent that evolves with you. Turn routine tasks i... (Skywork(@Skywork_ai), 2026-04-30T11:31:32+00:00)
  confidence=0.95 should_fold=False reason=The new item is an event announcement for an SF Happy Hour by Qdrant, while the candidate is about Skywork with Hermes Agent capabilities. No shared topic or entities.
- A: Perplexity Computer is now available in Microsoft Teams. Run research, analysis, and document creat... (Perplexity(@perplexity_ai), 2026-05-04T18:05:59+00:00)
  B: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear... (Microsoft Research(@MSFTResearch), 2026-05-04T16:57:40+00:00)
  confidence=0.95 should_fold=False reason=The candidate is a research focus summary about AI agents and cloud deployment, unrelated to Perplexity or Teams.
- A: Meet Skywork with Hermes Agent capabilities. An agent that evolves with you. Turn routine tasks i... (Skywork(@Skywork_ai), 2026-04-30T11:31:32+00:00)
  B: SF Happy Hour on April 28 In town for AI Dev? Come hang with the Qdrant team 👇 → Meet builders → ... (Qdrant(@qdrant_engine), 2026-04-23T16:00:02+00:00)
  confidence=0.9 should_fold=False reason=Candidate is a social event (SF Happy Hour) not related to new item about Hermes Agent.
- A: DeepSeek v4 Pro还是可以的。 几轮对话，实现一个工具，用xbox手柄控制电脑应用和浏览器。 当遥控器，躺床上刷小说和看视频。 (向阳乔木(@vista8), 2026-05-04T09:33:29+00:00)
  B: We're incrementally rolling out Nano Banana Pro to Antigravity. It's not only a step change in image... (Varun Mohan(@_mohansolo), 2025-11-20T17:41:52+00:00)
  confidence=0.95 should_fold=False reason=Unrelated topic: Nano Banana Pro image generation.
- A: We're incrementally rolling out Nano Banana Pro to Antigravity. It's not only a step change in image... (Varun Mohan(@_mohansolo), 2025-11-20T17:41:52+00:00)
  B: DeepSeek v4 Pro还是可以的。 几轮对话，实现一个工具，用xbox手柄控制电脑应用和浏览器。 当遥控器，躺床上刷小说和看视频。 (向阳乔木(@vista8), 2026-05-04T09:33:29+00:00)
  confidence=0.95 should_fold=False reason=Different products: DeepSeek v4 Pro vs Nano Banana Pro; different event: Xbox controller tool vs image generation rollout.
- A: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear... (Microsoft Research(@MSFTResearch), 2026-05-04T16:57:40+00:00)
  B: Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config... (OpenAI(@OpenAI), 2026-05-01T19:05:50+00:00)
  confidence=0.95 should_fold=False reason=The new item discusses AI agents leaking data, a smarter OS, and structuring AI use at work, which are unrelated to the candidate's content about importing workflow to Codex.
- A: Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config... (OpenAI(@OpenAI), 2026-05-01T19:05:50+00:00)
  B: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear... (Microsoft Research(@MSFTResearch), 2026-05-04T16:57:40+00:00)
  confidence=0.95 should_fold=False reason=The new item is about Codex workflow import, while the candidate is a general research newsletter - unrelated.
- A: Meet Skywork with Hermes Agent capabilities. An agent that evolves with you. Turn routine tasks i... (Skywork(@Skywork_ai), 2026-04-30T11:31:32+00:00)
  B: Third Skill: UGC Ads Have your agent promote your project (or anything, really). Input for this vid... (Pika(@pika_labs), 2026-05-01T19:20:28+00:00)
  confidence=0.9 should_fold=False reason=Candidate is about UGC Ads for Pika; new item is about Skywork Hermes Agent. Unrelated.
- A: Build it. Break it. Fix it. From campaign trackers to financial planners, @CalStateEastBay students... (OpenAI Developers(@OpenAIDevs), 2026-05-04T21:14:13+00:00)
  B: You can build a full pitch deck in Replit without touching a single slide. Just describe what you w... (Replit ⠕(@Replit), 2026-05-04T19:00:28+00:00)
  confidence=0.95 should_fold=False reason=New item is about Codex challenge; candidate is about Replit pitch deck feature. Unrelated topics.
- A: We’ll take it 😊 Copilot is getting better fast, and Excel is one of the best places to see that. Mo... (Satya Nadella(@satyanadella), 2026-05-02T12:11:51+00:00)
  B: Oh no. The "soulless music machine" will take all the musicians' jobs! ... Actually, we have more mu... (Richard Socher(@RichardSocher), 2026-05-04T04:34:32+00:00)
  confidence=0.95 should_fold=False reason=The new item is about Copilot and Excel, while the candidate discusses music and AI taking jobs. No thematic overlap.
- A: Make anything. From anywhere. On any device. Runway is now on both Android and iOS. Get started at ... (Runway(@runwayml), 2026-05-01T17:47:51+00:00)
  B: You can now ask Gemini to create Docs, Sheets, Slides, PDFs, and more directly in your chat. No more... (Sundar Pichai(@sundarpichai), 2026-04-29T16:00:49+00:00)
  confidence=0.95 should_fold=False reason=Candidate is about Gemini creating Docs, unrelated to Runway.
- A: SF Happy Hour on April 28 In town for AI Dev? Come hang with the Qdrant team 👇 → Meet builders → ... (Qdrant(@qdrant_engine), 2026-04-23T16:00:02+00:00)
  B: wow! (Thomas Wolf(@Thom_Wolf), 2026-03-14T17:05:13+00:00)
  confidence=0.95 should_fold=False reason=The candidate is about a dataset of computer-use recordings, unrelated to the Qdrant Happy Hour event.

## 7. Cluster diagnostics

{
  "actions": {
    "attach_to_cluster": 19
  },
  "attached_existing_clusters": 1,
  "avg_confidence": 0.618,
  "avg_items_per_cluster": 1.056,
  "candidate_clusters_considered": 18,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "core_facts": [
        "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new research on how to actually structure AI use at work. msft.it/6016vKxQm Your browser does not support the video tag. 🔗 View on Twitter 💬 7 🔄 13 ❤️ 50 👀 9018 📊 18 ⚡ Powered by xgo.ing"
      ],
      "item_count": 2,
      "known_angles": [],
      "representative_items": [
        "item_153b053b4e2f4f7d845156e8b418851c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "NVIDIA AI highlights local AI agent capability",
      "core_facts": [
        "NVIDIA AI shares a user experience of running a 121B model locally on DGX Spark via a Hermes agent that autonomously passed all tests."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_15c586321ecc435d84c9603a5c96de7e"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Ray Dalio on the battle between feelings and rational thinking",
      "core_facts": [
        "Ray Dalio discusses the internal battle between subconscious feelings (amygdala) and conscious rational thinking (prefrontal cortex)."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_8f18e494f5a14811ae5b5b2c41a9c28f"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Monica AI launches Claude 4.7 Opus and GPT Image 2",
      "core_facts": [
        "Monica AI announced the launch of Claude 4.7 Opus and GPT Image 2 on their platform."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_4d31618a325b457babfe6de93534a9e4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "播客讨论：李想与老罗谈AI与商业",
      "core_facts": [
        "播客笔记记录李想与老罗关于AI、一人公司、增效降本、裁员、出海、具身智能、人的价值等话题的讨论。"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_3965e6d5ecd14787aa50b9cda05a3672"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Mem0 and BasisSet announce 2026 AI Fellowship Agentic Memory Track",
      "core_facts": [
        "Mem0 partners with BasisSet for 2026 AI Fellowship Agentic Memory Track, applications due May 1."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_cbf825c399f3462e8e01444668c676f3"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "OpenAI builds sandbox for Codex on Windows",
      "core_facts": [
        "Detailed summary of OpenAI Codex sandbox for Windows, covering design iterations and final elevated sandbox solution."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_0ef913313e7040aba5790f2990e052fa"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Book release: The Book of Elon",
      "core_facts": [
        "Eric Jorgenson's 'The Book of Elon' launched, compiled from Elon Musk's public appearances."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_2ae8b16d066e4ce6803f040b7ad3524a"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Gemini API docs, cookbook, and Cloudflare worker example",
      "core_facts": [
        "Links to Gemini API docs, cookbook, and Cloudflare worker example repo."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ef11c4ff68b140edb01534cb11a4aa18"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Qwen3.6-27B benchmark results",
      "core_facts": [
        "Qwen announces Qwen3.6-27B outperforming Qwen3.5-397B-A17B on SWE-bench Verified, SWE-bench Pro, Terminal-Bench 2.0, and SkillsBench."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_f1c16295e60c464ab1d12dc414e98358"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Case study of Datagraphs integrating Qdrant for Graph RAG",
      "core_facts": [
        "Qdrant presents a case study of Datagraphs, which built a knowledge graph platform integrating Qdrant for semantic search, highlighting complementary roles of vector and graph retrieval."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_97d257ff339f4c49a1ba251516d1dccd"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Qwen3.6 Plus achieves Code Arena #7 and Text Arena #36 improvements",
      "core_facts": [
        "Qwen3.6 Plus lands at #7 in Code Arena with score 1476, up 16 points, and at #36 in Text Arena, up 13 points. AlibabaGroup moves to #3 lab in Code Arena."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_beb942d4df9f410c938301d606a48137"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Satya Nadella reports Microsoft Copilot milestones",
      "core_facts": [
        "Satya Nadella reports over 20 million M365 Copilot seats, nearly 140,000 orgs using GitHub Copilot, and 2x increase in Security Copilot customers YoY."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_b1a9fa40cd1540ab8fac1aefdb1f272c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Gemma 4 gets Multi-Token Prediction drafters",
      "core_facts": [
        "Multi-Token Prediction drafters are here for Gemma 4, making inference up to 3x faster with zero quality loss. Available for E2B and E4B versions under Apache 2.0 license."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_071af4614d46408c8e5e9d8f3ea01606"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Replit teases Episode 2 of Race To Revenue",
      "core_facts": [
        "Now it's time to really execute. Episode 2 is coming. Two builders, two wildly different bets. One building AI voice tools from a farm. The other turning bartending gigs into a career engine. Who hits revenue first? Race To Revenue out Wednesday. Don't miss it."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c63c9cb40415424a95ef922becbc51f4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "3D soft toy character 'FEEL MORE / THINK LESS' prompt",
      "core_facts": [
        "Prompt describes a 3D soft toy-like character with glossy texture, holding a floating heart, with typography 'FEEL MORE / THINK LESS' and caption 'emotion update v2'."
      ],
      "item_count": 1,
      "known_angles": [
        "The design combines a cute character with a philosophical message."
      ],
      "representative_items": [
        "item_187faea341af48678e92d006028e10b1"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Stanford SAIL and ETH demonstrate SDPO for RL with rich feedback",
      "core_facts": [
        "Stanford SAIL and ETH collaboration shows RL with rich feedback significantly outperforms scalar rewards on hard tasks, introducing SDPO."
      ],
      "item_count": 1,
      "known_angles": [
        "Rich feedback provides more granular signal for hard tasks than scalar rewards."
      ],
      "representative_items": [
        "item_eb48830993f3442688d0f4d4f262c974"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Debate on AI's impact on labor market",
      "core_facts": [
        "Yann LeCun states that Dario (likely Dario Amodei) is wrong about AI's labor market effects and advises listening to economists."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_342aa6368b3f4c39bc3051fe86d68d4b"
      ]
    }
  ],
  "created_clusters": 18,
  "follow_up_event": {
    "false": 19
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 1,
  "relations": {
    "new_info": 13,
    "repeat": 1,
    "source_material": 5
  },
  "same_event": {
    "true": 19
  },
  "same_topic": {
    "true": 19
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 18,
  "top_clusters": [
    {
      "cluster_id": "cluster_4e7dc4612e0b4942805c884e47560f1a",
      "cluster_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "item_count": 2
    },
    {
      "cluster_id": "cluster_9a8723057cb646c18f98d692b6eeb192",
      "cluster_title": "NVIDIA AI highlights local AI agent capability",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_3bfe3368634e4e9baed3a7131ebff5a3",
      "cluster_title": "Ray Dalio on the battle between feelings and rational thinking",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_429b7806cd2d44d7ad8b8f1272433a98",
      "cluster_title": "Monica AI launches Claude 4.7 Opus and GPT Image 2",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_b138cc46cefc4b88a597ee9aff6d898c",
      "cluster_title": "播客讨论：李想与老罗谈AI与商业",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_7ba7956fd9b846ac987dd57fb67f9e4b",
      "cluster_title": "Mem0 and BasisSet announce 2026 AI Fellowship Agentic Memory Track",
      "item_count"

## 8. Event hotspots

- hotspot_001_xgo.ing `xgo.ing` size=300 non_different=30 multi_cluster=True reason=None
- hotspot_002_powered `powered` size=300 non_different=0 multi_cluster=True reason=None
- hotspot_003_xgoing `xgoing` size=300 non_different=0 multi_cluster=True reason=None
- hotspot_004_view `view` size=139 non_different=0 multi_cluster=True reason=None
- hotspot_005_not `not` size=118 non_different=0 multi_cluster=True reason=None
- hotspot_006_your `your` size=123 non_different=0 multi_cluster=True reason=None
- hotspot_007_you `you` size=104 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_008_support `support` size=96 non_different=0 multi_cluster=True reason=None
- hotspot_009_video `video` size=92 non_different=0 multi_cluster=True reason=None
- hotspot_010_does `does` size=92 non_different=0 multi_cluster=True reason=None
- hotspot_011_browser `browser` size=89 non_different=0 multi_cluster=True reason=None
- hotspot_012_twitter `twitter` size=88 non_different=0 multi_cluster=True reason=None
- hotspot_013_tag `tag` size=88 non_different=0 multi_cluster=True reason=None
- hotspot_014_tag. `tag.` size=87 non_different=0 multi_cluster=True reason=None
- hotspot_015_now `now` size=79 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_016_more `more` size=69 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_017_can `can` size=76 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_018_our `our` size=67 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_019_quoted `quoted` size=74 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_020_tweet `tweet` size=74 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_021_are `are` size=67 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_022_just `just` size=59 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_023_model `model` size=52 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_024_one `one` size=49 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_025_what `what` size=53 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_026_all `all` size=48 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_027_agents `agents` size=39 non_different=0 multi_cluster=True reason=None
- hotspot_028_but `but` size=52 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_029_most `most` size=35 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_030_new `new` size=41 non_different=0 multi_cluster=True reason=None
- hotspot_031_have `have` size=40 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_032_out `out` size=40 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_033_https `https` size=39 non_different=0 multi_cluster=True reason=None
- hotspot_034_how `how` size=37 non_different=0 multi_cluster=True reason=None
- hotspot_035_agent `agent` size=40 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_036_tco `tco` size=37 non_different=0 multi_cluster=True reason=None
- hotspot_037_into `into` size=38 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_038_t.co `t.co` size=36 non_different=0 multi_cluster=True reason=None
- hotspot_039_will `will` size=34 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_040_use `use` size=31 non_different=0 multi_cluster=True reason=None
- hotspot_041_models `models` size=37 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_042_like `like` size=36 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_043_than `than` size=33 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_044_today `today` size=30 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_045_work `work` size=35 non_different=0 multi_cluster=True reason=None
- hotspot_046_every `every` size=34 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_047_them `them` size=30 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_048_built `built` size=29 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_049_don `don` size=28 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members
- hotspot_050_get `get` size=27 non_different=0 multi_cluster=False reason=no final multi-item cluster among hotspot members

## 9. Source-profile review

{
  "disabled_for_llm_candidates": [],
  "high_candidates": [],
  "llm_total_tokens_by_source": {
    "socialmedia-microsoft-research-msftresearch": 9630,
    "socialmedia-mike-krieger-mikeyk": 6156,
    "socialmedia-naval-naval": 9972,
    "socialmedia-nvidia-ai-nvidiaai": 8889,
    "socialmedia-openai-developers-openaidevs": 5678,
    "socialmedia-openai-openai": 5555,
    "socialmedia-orange-ai-oran-ge": 5833,
    "socialmedia-paul-couvert-itspaulai": 6313,
    "socialmedia-perplexity-perplexity-ai": 5606,
    "socialmedia-pika-pika-labs": 11440,
    "socialmedia-qdrant-qdrant-engine": 10262,
    "socialmedia-recraft-recraftai": 9646,
    "socialmedia-rowan-cheung-rowancheung": 17108,
    "socialmedia-runway-runwayml": 24958,
    "socialmedia-sahil-lavingia-shl": 14596,
    "socialmedia-sam-altman-sama": 40570,
    "socialmedia-satya-nadella-satyanadella": 27615,
    "socialmedia-scott-wu-scottwu46": 20967,
    "socialmedia-simon-willison-simonw": 33599,
    "socialmedia-skywork-skywork-ai": 26785,
    "socialmedia-stanford-ai-lab-stanfordailab": 7675,
    "socialmedia-sualeh-asif-sualehasif996": 11144,
    "socialmedia-suhail-suhail": 20855,
    "socialmedia-taranjeet-taranjeetio": 9539,
    "socialmedia-the-rundown-ai-therundownai": 22611,
    "socialmedia-thomas-wolf-thom-wolf": 5636,
    "socialmedia-v0-v0": 11053,
    "socialmedia-varun-mohan-mohansolo": 15155,
    "socialmedia-vista8": 17451,
    "socialmedia-windsurf-windsurf-ai": 19530
  },
  "low_candidates": [],
  "pending_reviews_created": 0,
  "pending_reviews_created_all_types": 480,
  "reviews_suppressed_due_to_insufficient_data": 57,
  "sources_recomputed": 57,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
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
      "source_id": "socialmedia-lovartai-lovart-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5261,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-marc-andreessen-127482-127480-pmarca",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
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
      "source_id": "socialmedia-mem0-mem0ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
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
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9630,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
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
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6156,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
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
      "source_id": "socialmedia-milvus-milvusio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
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
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
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
      "source_id": "socialmedia-mustafa-suleyman-mustafasuleyman",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_valu

## 10. Readiness recommendation

{
  "cluster_signal_count": 19,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "8 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}

## 11. Known gaps

- Cluster candidate alternatives are reconstructed from persisted decisions/logs; the pre-LLM candidate list is only partially available unless future runs persist it at candidate-generation time.
- Ingest source-level diagnostic CSVs are omitted when this phase runs without fresh ingest.
