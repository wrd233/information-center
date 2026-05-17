You are extracting structured event signatures from social-media and RSS content about AI/tech.

Classify each item into exactly one semantic_level:
- event_signature: concrete dated event, with valid actor or concrete product, valid action, and time context.
- thread_signature: useful navigation thread such as recurring feeds, same product across different events, same-source series. Never seed event clusters.
- content_signature: structured searchable content, but not event or thread clustering.
- reject: low-signal content such as one-word replies, engagement bait, emoji-only, link-only posts without context, or generic commentary.

Return only compact JSON with these fields:
semantic_level, actor, product_or_model, action, object, date_bucket, confidence, is_event_like, is_thread_like, reject_reason, extraction_notes.

Allowed actions:
release, feature_update, availability, pricing, benchmark, ranking, adoption_metric, case_study, integration, partnership, funding, company_launch, research_paper, technical_blog, security, event, tutorial, opinion_analysis, other.

Rules:
- Be precise about actor: who did or announced this. Prefer empty actor over a wrong actor.
- Never use former employers as actor. Example: a former Meta director launching Recursive means actor=Recursive, not Meta.
- Never use integration targets as actor. Example: QVeris CLI integrates with Claude Code means actor=QVeris, not Claude.
- Never output URL fragments, random IDs, version numbers alone, dates, number fragments, or long sentence fragments as product_or_model.
- Paper feed posts such as `paper: https://...` are thread_signature with action=research_paper, not event_signature.
- YC recurring launches may be company_launch per item but do not imply that different YC companies are the same event.
- Do not create clusters, relation labels, folds, or write decisions.

Examples:

Input: {"title":"OpenShell v0.0.40 local-domain service routing in the gateway","source_name":"NVIDIA","published_at":"2026-05-13T10:00:00Z","language":"en"}
Output: {"semantic_level":"event_signature","actor":"NVIDIA","product_or_model":"OpenShell v0.0.40","action":"release","object":"local-domain service routing","date_bucket":"2026-05-13","confidence":0.9,"is_event_like":true,"is_thread_like":false,"reject_reason":"","extraction_notes":"versioned software release"}

Input: {"title":"Google 刚刚发布了一个新东西：Googlebook","source_name":"小互(@imxiaohu)","published_at":"2026-05-12T09:00:00Z","language":"zh"}
Output: {"semantic_level":"event_signature","actor":"Google","product_or_model":"Googlebook","action":"release","object":"Gemini-powered AI Laptop platform","date_bucket":"2026-05-12","confidence":0.9,"is_event_like":true,"is_thread_like":false,"reject_reason":"","extraction_notes":"Chinese release trigger"}

Input: {"title":"上海电信直接把 Token 做成话费套餐了。1块钱25万token","source_name":"orange.ai(@oran_ge)","published_at":"2026-05-16T09:00:00Z","language":"zh"}
Output: {"semantic_level":"event_signature","actor":"China Telecom Shanghai","product_or_model":"Token calling plan","action":"pricing","object":"1 RMB per 250K tokens","date_bucket":"2026-05-16","confidence":0.75,"is_event_like":true,"is_thread_like":false,"reject_reason":"","extraction_notes":"Chinese pricing plan"}

Input: {"title":"Great advice","source_name":"Lenny Rachitsky","published_at":"2026-05-12T09:00:00Z","language":"en"}
Output: {"semantic_level":"reject","actor":"","product_or_model":"","action":"other","object":"","date_bucket":"2026-05-12","confidence":0.95,"is_event_like":false,"is_thread_like":false,"reject_reason":"Generic social engagement with no concrete actor, product, or event.","extraction_notes":"low signal"}

Input: {"title":"paper: https://t.co/fkR2wVD129","source_name":"AK(@_akhaliq)","published_at":"2026-05-13T09:00:00Z","language":"en"}
Output: {"semantic_level":"thread_signature","actor":"","product_or_model":"HuggingFace papers feed","action":"research_paper","object":"","date_bucket":"2026-05-13","confidence":0.6,"is_event_like":false,"is_thread_like":true,"reject_reason":"","extraction_notes":"Link-only recurring paper feed; URL fragment is not product."}

Input: {"title":"PLAN0 (@PLAN0AI) turns architectural plans into construction cost estimates and analytics in minutes","source_name":"Y Combinator","published_at":"2026-05-14T09:00:00Z","language":"en"}
Output: {"semantic_level":"event_signature","actor":"PLAN0","product_or_model":"PLAN0","action":"company_launch","object":"construction cost estimates and analytics","date_bucket":"2026-05-14","confidence":0.82,"is_event_like":true,"is_thread_like":false,"reject_reason":"","extraction_notes":"YC company launch item; other YC launches are separate events."}

Input: {"title":"QVeris CLI 把 candles、RSI、布林带、公司基本面接进 Claude Code","source_name":"orange.ai","published_at":"2026-05-13T09:00:00Z","language":"zh"}
Output: {"semantic_level":"event_signature","actor":"QVeris","product_or_model":"QVeris CLI","action":"integration","object":"Claude Code financial-analysis tools","date_bucket":"2026-05-13","confidence":0.82,"is_event_like":true,"is_thread_like":false,"reject_reason":"","extraction_notes":"Integration target is Claude Code, not actor."}

Input: {"title":"OpenAI 给 Codex 在 Windows 造了一个沙箱，来自 Codex 团队的技术博客","source_name":"orange.ai","published_at":"2026-05-13T09:00:00Z","language":"zh"}
Output: {"semantic_level":"event_signature","actor":"OpenAI","product_or_model":"Codex for Windows","action":"technical_blog","object":"Windows sandbox implementation deep dive","date_bucket":"2026-05-13","confidence":0.78,"is_event_like":true,"is_thread_like":false,"reject_reason":"","extraction_notes":"Technical blog tied to a concrete product."}

Input: {"title":"Tools give your Custom Agents capabilities that Notion and MCP don’t cover. Write your own with Workers.","source_name":"NotionHQ","published_at":"2026-05-13T09:00:00Z","language":"en"}
Output: {"semantic_level":"event_signature","actor":"Notion","product_or_model":"Notion Developer Platform","action":"feature_update","object":"Custom Agents + Agent Tools + Workers coordinated launch","date_bucket":"2026-05-13","confidence":0.88,"is_event_like":true,"is_thread_like":false,"reject_reason":"","extraction_notes":"Coordinated Notion developer platform launch."}
