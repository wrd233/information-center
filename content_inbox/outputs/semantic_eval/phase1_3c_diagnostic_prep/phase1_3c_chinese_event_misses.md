# Phase 1.3c Chinese Event Detection Miss Analysis

## Summary

- Total 300-run items: 300
- Chinese/mixed items found: 50
- Chinese event detection rate in signatures: 0.3000 (gate: >= 0.5)
- Items with event_signature level: 15
- Estimated truly event-like Chinese items: 19

## Classification Breakdown

| Classification | Count |
|---|---|
| correct_event_signature | 15 |
| correct_reject | 13 |
| correct_thread_signature | 10 |
| likely_false_negative_thread | 7 |
| likely_false_negative_event | 4 |
| correct_content_signature | 1 |

## Trigger Coverage

| Trigger Group | Hit Count |
|---|---|
| 官宣/新公司/联合创始人/创业/成立/融资 | 7 |
| 发布/发布了/刚刚发布/正式发布 | 5 |
| 支持/接入/打通/集成/连接/对接 | 3 |
| 推出/上线/开放/开源/释出 | 3 |
| 套餐/免费/降价/价格/1块钱/元/折扣/优惠 | 3 |
| 漏洞/安全/修复/补丁 | 2 |
| 超过/超越/领先/采用率/市场份额/市值/用户数/增长 | 2 |
| 评测/跑分/榜单/基准/准确率 | 2 |
| 技术预览/预览版/内测/公测/候补/waitlist | 1 |
| 大会/活动/直播/研讨会/峰会/报名 | 1 |

## Likely False Negatives (11 items)

### item_815fb633b2c14ae7ace5554fbaccd60f
- **Source**: 李继刚(@lijigang_com)
- **Title**: 在「世界刺激」和「你的反应」之间，有一片空间，那里是「你对它的解释」，像是一面观察透镜。 那片空间，目前看来，是语言搭建起来的。 当切换对一个刺激的语言描述时，「你的反应」就会跟着变。 有时候，...
- **Current Level**: reject
- **Current Action**: other
- **Actor**: 
- **Product**: 
- **Classification**: likely_false_negative_thread
- **Corrected Level**: reject
- **Corrected Actor**: 
- **Corrected Product**: 
- **Corrected Action**: other
- **Invalid Reasons**: ['missing_concrete_actor_or_product', 'weak_action_without_entity', 'semantic_level_reject']

### item_12eda743705a4e9497ce8b40bbd7c4b0
- **Source**: orange.ai(@oran_ge)
- **Title**: 五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查...
- **Current Level**: thread_signature
- **Current Action**: pricing
- **Actor**: 
- **Product**: CERX3N35
- **Classification**: likely_false_negative_thread
- **Corrected Level**: event_signature
- **Corrected Actor**: ColaOS
- **Corrected Product**: CERX3N35
- **Corrected Action**: pricing
- **Invalid Reasons**: ['semantic_level_thread_signature']

### item_4f4c39a8207b4b0187b880edfea031c4
- **Source**: orange.ai(@oran_ge)
- **Title**: 有位朋友创业做的好好的，又赚钱又开心又不用上班... 结果天天被投资人 PUA 说要融资搞架构找联创 all in 什么的 我说你活在美好的未来，他们还在苦逼的过去 别听他们的 follow your...
- **Current Level**: reject
- **Current Action**: funding
- **Actor**: 
- **Product**: 
- **Classification**: likely_false_negative_event
- **Corrected Level**: thread_signature
- **Corrected Actor**: PUA
- **Corrected Product**: 有位朋友创业做的
- **Corrected Action**: funding
- **Invalid Reasons**: ['missing_concrete_actor_or_product', 'semantic_level_reject']

### item_e891530dd3a1420da85a9d9a7ec1378d
- **Source**: orange.ai(@oran_ge)
- **Title**: 李想 × 老罗播客笔记 AI 与一人公司 李想：AI 是生产力和劳动力的技术。我现在不太相信一人公司。很多一人公司都在更新内容来验证这个概念成立，但验证了一段时间之后发现，他们每天更新的事情就是 ...
- **Current Level**: reject
- **Current Action**: adoption_metric
- **Actor**: 
- **Product**: 
- **Classification**: likely_false_negative_event
- **Corrected Level**: thread_signature
- **Corrected Actor**: OpenClaw
- **Corrected Product**: OpenClaw
- **Corrected Action**: adoption_metric
- **Invalid Reasons**: ['missing_concrete_actor_or_product', 'semantic_level_reject']

### item_ef32d9713ac8427a91271666294ec161
- **Source**: orange.ai(@oran_ge)
- **Title**: 企业里的人+Agent 协作产品 Syncless 发布了
- **Current Level**: thread_signature
- **Current Action**: release
- **Actor**: 
- **Product**: Yeuoly1
- **Classification**: likely_false_negative_thread
- **Corrected Level**: event_signature
- **Corrected Actor**: Agent
- **Corrected Product**: Yeuoly1
- **Corrected Action**: release
- **Invalid Reasons**: ['semantic_level_thread_signature']

### item_afe50ae6a16d4bf9ba653e75cf32829d
- **Source**: orange.ai(@oran_ge)
- **Title**: 我们不断地去思考协作的本质是什么 团队之间真正需要对齐的是什么 只有把沟通协作的模型想透彻 才能做出 Human-Agent 产品
- **Current Level**: reject
- **Current Action**: other
- **Actor**: 
- **Product**: 
- **Classification**: likely_false_negative_thread
- **Corrected Level**: thread_signature
- **Corrected Actor**: Human-Agent
- **Corrected Product**: 我们不断地去思考
- **Corrected Action**: other
- **Invalid Reasons**: ['missing_concrete_actor_or_product', 'weak_action_without_entity', 'semantic_level_reject']

### item_974fcb9fd04b4f188ef1c5fa2d39b98b
- **Source**: 歸藏(guizang.ai)(@op7418)
- **Title**: 嘉琛的 bridge 有些设计和能力真的很顶
- **Current Level**: reject
- **Current Action**: technical_blog
- **Actor**: 
- **Product**: 
- **Classification**: likely_false_negative_event
- **Corrected Level**: event_signature
- **Corrected Actor**: Jc He
- **Corrected Product**: bridge
- **Corrected Action**: technical_blog
- **Invalid Reasons**: ['missing_concrete_actor_or_product', 'semantic_level_reject']

### item_9d2e5c5ad045467688302f8d8df3acde
- **Source**: orange.ai(@oran_ge)
- **Title**: 开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。
- **Current Level**: reject
- **Current Action**: release
- **Actor**: 
- **Product**: 
- **Classification**: likely_false_negative_event
- **Corrected Level**: event_signature
- **Corrected Actor**: CLI
- **Corrected Product**: 开源一个月的时间
- **Corrected Action**: release
- **Invalid Reasons**: ['missing_concrete_actor_or_product', 'weak_action_without_entity', 'semantic_level_reject']

### item_ff8c9467986d426e90becc6e1ecf654e
- **Source**: orange.ai(@oran_ge)
- **Title**: 人只有在真实的环境里才能做出正确的决定。 人类学研究表明，人类的决策过程主要是由激素推动的，知识，经验，理智在这个过程中所起的作用并不大。 我们往往是做出决定之后，再用智慧去寻找证据以便证明自己的决定...
- **Current Level**: reject
- **Current Action**: research_paper
- **Actor**: 
- **Product**: 
- **Classification**: likely_false_negative_thread
- **Corrected Level**: thread_signature
- **Corrected Actor**: 
- **Corrected Product**: skin in the game
- **Corrected Action**: research_paper
- **Invalid Reasons**: ['missing_concrete_actor_or_product', 'semantic_level_reject']

### item_fd493ad98cdb483a9ae3d1da67788425
- **Source**: orange.ai(@oran_ge)
- **Title**: 实践是获得真理和获悉真相的唯一途径。
- **Current Level**: reject
- **Current Action**: case_study
- **Actor**: 
- **Product**: 
- **Classification**: likely_false_negative_thread
- **Corrected Level**: thread_signature
- **Corrected Actor**: Powered
- **Corrected Product**: 实践是获得真理和
- **Corrected Action**: case_study
- **Invalid Reasons**: ['missing_concrete_actor_or_product', 'semantic_level_reject']

### item_107661efeb1343b5b3a1576c6a4a39db
- **Source**: orange.ai(@oran_ge)
- **Title**: 老黄当年决定做 CUDA 的时候 大概也没想到后来会有一万个人为这个决定辩经 人类太沉迷寻找证据寻找因果了
- **Current Level**: reject
- **Current Action**: research_paper
- **Actor**: 
- **Product**: 
- **Classification**: likely_false_negative_thread
- **Corrected Level**: thread_signature
- **Corrected Actor**: CUDA
- **Corrected Product**: CUDA
- **Corrected Action**: research_paper
- **Invalid Reasons**: ['missing_concrete_actor_or_product', 'semantic_level_reject']


## Correct Event Signatures (15 items)

- **item_0bea403e70384581b6a16f7ed9303894**: OpenAI 如何实现规模化的低延迟语音 AI 语音交互的"自然感"完全建立在毫秒级响应之上。一旦网络抖动、首包慢、丢包，用户立刻感知为停顿、被打断或抢话失败。OpenAI 面对的约束有三条： · ... | actor=OpenAI | product=K8s | action=pricing
- **item_60e5d2df9cb74fee927334cde3f7b8c8**: Cursor 团队这篇「持续改进我们的 Agent Harness」，写的真不错，很实战： · 如何衡量 harness 的好坏？ · 如何为不同模型定制 harness？ · 中途换模型到底会有什么... | actor=Cursor | product=Agent Harness | action=technical_blog
- **item_880c11f1351143cbb4b7b1f729005c63**: 日读论文： https://t.co/ypqznEy9Ev From Context to Skills: Can Language Models Learn from Context Skill... | actor=arxiv | product=GPT-5.1 | action=funding
- **item_c1ac61882cc74c6b822c774ad9d341b2**: Claude code 发布 多任务统一窗口管理工具：Agent View 以前你同时跑多个 Claude Code 任务，要开一堆终端窗口、标签页，分不清哪个任务在等你确认、哪个还在跑、哪个已经做... | actor=Anthropic | product=Claude code | action=feature_update
- **item_c7f4f61b77a24f5b8a42cb44fa7f5667**: Anthropic 提到的典型用法包括：同时派发多个想法、让不同 Agent 配合不同 skill 生成 PR、管理长期运行任务，比如 PR babysitter、dashboard updater，... | actor=Anthropic | product=claude.com | action=feature_update
- **item_6f0455e24b574d8590f2cdf8555be2d1**: Google 刚刚发布了一个新东西：Googlebook 根据Google 自己的表述： 他们想做的已经不再是传统意义上的“操作系统”，而是一个以 Gemini 为核心的 AI Laptop 平台... | actor=Google | product=Googlebook | action=feature_update
- **item_00a7372d41284c28931a28e579a03d61**: 田渊栋 (前 Meta FAIR Director) 以联合创始人身份正式官宣新公司：Recursive @Recursive_SI Recursive 的使命是构建递归自改进超智能 (Recur... | actor=Recursive | product=Recursive | action=company_launch
- **item_050e5a4a15e24ca5b984101c4741fa54**: OpenAI 给 Codex 在 Windows 造了一个沙箱，过程比想象中曲折 ... 来自 Codex 团队 David Wiesen 非常有深度的技术博客，推荐阅读！ https://t.co... | actor=OpenAI/Codex | product=Codex | action=adoption_metric
- **item_9d1a4330d2b94b5a8efbf0dccbea5ad1**: Codex 终于支持手机上的 ChatGPT 远程控制了！ 可以自动同步你绑定的 Codex 设备上的所有对话，而且可以直接发送指令、审批权限、监控进度。 我写一下设置的教程： 1. 点击桌面端... | actor=OpenAI/Codex | product=Codex | action=feature_update
- **item_9564c5e550d04eae8642a2117d5bdcdf**: GitHub 发布了 GitHub Copilot 桌面端的技术预览版。 看起来跟 Codex 长得有点像，在 GitHub 相关功能上露出的也比较多。 现在需要申请 waitlist | actor=GitHub | product=GitHub Copilot Desktop | action=availability
- **item_bed5ef99510340718a3c9591ccfe0f6c**: 金融分析的门槛正在被 AI 降低。 QVeris CLI 把 candles、RSI、布林带、公司基本面接进 Claude Code，用户不用写复杂脚本，也能让 agent 调工具跑分析。 这类小... | actor=QVeris | product=QVeris CLI | action=integration
- **item_34c167815aea4d79bc92978d66340e95**: Notion 终于出了 CLI… 跟上了这个时代 | actor=Notion | product=Notion Developer Platform | action=integration
- **item_a7e9be5012784ce792fa7e4604ccff57**: 😂 绝了，上海电信直接把 Token 做成话费套餐了。 1块钱25万token，账单里直接就能扣。 手机厂商还在想怎么做 AI 入口，运营商先自己下场了。 甚至还说... "Token服务是中国电... | actor=China Telecom Shanghai | product=Token calling plan | action=pricing
- **item_fef20066df524b90a1044d1b1ce3ab36**: 值得试试，挺有价值的，让 Codex 帮你分析电脑操作习惯+Codex任务执行情况，给出具体的对工作习惯上的优化建议。 注意：Chronicle 是一款用于记录和分析用户电脑操作轨迹的追踪软件或系统... | actor=OpenAI/Codex | product=Codex | action=feature_update
- **item_20a0c2bcfd9f4280bf66ac1ed7508dc6**: Codex 也发布了宠物功能 8个形态 三个状态提示：running（在跑）／waiting for input（等你接话）／ready for review（等你看 diff） 打开方法：输入... | actor=OpenAI/Codex | product=Codex | action=feature_update

## Correctly Rejected (13 items)

- **item_884fdc54e867463db72c57d34b4bfd10**: 孩子明天开学要做单元测试。 把课文用任意AI工具拍照，出一套复习题，粘贴到备忘录打印即可。
- **item_82e3c15b234b466dabbdaf082b2627fa**: 我去年认为，AI 会拿走「判断」，人会守着两项能力与AI 协作： - Say Yes: 要性（wantness）, 在起点注入自己的意志 - Say No: 否决（taste），在终点筛选符合自己标...
- **item_7306f80a855048bb8fbe5418cac08bf4**: 这期播客实在是太大实话了哈哈 大模型这事儿现在太简单了 不存在个人英雄主义 可能存在一定的组织英雄主义 knowhow 啥的没那么重要，重要的是把事情做出来，把事情踏踏实实做好 talk is ch...
- **item_977581a12a2d44fcb3b52499eb97faa1**: 我和登科一起搞了个Agent坦克大战 不要天天用 AI 卷效率了 来放松一下玩会儿游戏吧！
- **item_325f8975afb647eeb8a90456e3fbb5bc**: 最近每篇帖子下面都有几条甚至几十条 AI 回复，完全不能理解这种 AI 回复的动力是什么？ 和纯垃圾黄赌毒回复还不太一样，这种 AI 回复更像是确实通读了我的内容，试图从某个角度给出 1-2 句追问...
- **item_e82fee6a274f4643adb8c341df3c2af3**: 可以 调用 Skill 舒服了啊
- **item_3a1d5cc39cb04ad1a031450e0d40b850**: 塔勒布的箴言集太好看了，一口气读完。 摘几句最喜欢的： - 要是早晨起床时，你就能预测这一天会是什么样子，那么你已经开始靠近死亡了。预测得越准确，你离死亡就越近。 - 只有当他们开始对你展开人身攻...
- **item_33e076638ab8429496f67137c0a342b4**: 执念就是明知道不理性还要做的事。 这不是科技能解决的问题。 反倒是人类最伟大的 feature。
- **item_c78ed82750544024bc0a16e42c270085**: 等我体验下，抽空写个评测，和姚老师看演示时，觉得产品有点超前，amazing
- **item_603d420bf1ce4e49b5d7fea5a7f512ed**: 成本 50万以下的短剧竟然不需要经过总局... explains a lot
- **item_3f2be349054c4d9ba957fa9d30b6c562**: 优秀模型 + Skill 就是顶级翻译学习工具。
- **item_fbccde1f48a0419e9e356f07867961c9**: 原来一个人最真的信念 是凌晨随口说给朋友听的那版。
- **item_f4f2ac8fcaa14e3eb66afe63c28a7b6e**: 今天看到一个牛逼的公式： 智力=速度x正确。 这是控制论里对智力的定义，一个人或一个组织在单位时间内进行正确选择的能力。 AI 可以无限放大速度，但是正确呢？还是个问号。 AI 可以让你 cod...
