# content_inbox_console — 信息中心作战台

`content_inbox_console` 是 `content_inbox` 的 API 驱动前端作战台。采用低心智负担、中文优先、Inbox Operating Loop 驱动的设计，帮助用户从 latest/selected registry_full Inbox Run 消费今日情报、Agent 处理、信息源健康和输出记录。

## 技术栈

- **后端 API 调用**: BackendClient (httpx) → `content_inbox` /api/*
- **前端框架**: FastAPI + Jinja2 模板
- **样式系统**: 自定义 CSS 设计系统（tokens.css + reset.css + layout.css + components.css + utilities.css）
- **实时更新**: HTMX v2.0.4 局部刷新
- **语言**: 中文优先，英文作为辅助括注

## 启动

后端 (端口 8787):

```bash
cd ../content_inbox
CONTENT_INBOX_DB_PATH=data/environments/fresh_default/content_inbox.db \
CONTENT_INBOX_ENABLE_REAL_RUNS=0 \
PYTHONPATH=. python3 -m app.server
```

前端控制台 (端口 8788):

```bash
cd content_inbox_console
CONTENT_INBOX_FRONTEND_API_BASE=http://127.0.0.1:8787 \
uvicorn app.main:app --host 127.0.0.1 --port 8788 --reload
```

打开 `http://127.0.0.1:8788`。

## 信息架构

### 导航分组

| 分组 | 页面 | 说明 |
|------|------|------|
| **作战首页** | /dashboard | latest Inbox Run 状态 + 下一步建议 |
| **Inbox Operating Loop** | /inbox-loop, /today-intel, /agent-processing, /runs, /source-health, /outputs | Inbox Loop、今日情报、Agent 处理、运行记录、信息源健康、输出记录 |
| **准备与上下文** | /sources, /runs/new, /context-query | 信息源、创建运行、上下文包查询 |
| **维护** | /reset, /environment, /settings | 数据清理、环境管理、设置 |
| **高级调试 / Legacy / 历史数据** (折叠) | /events, /review-queue, /briefings, /reports, /agent-query, /items, /dedupe-groups, /clusters, /entities, /relations, /claims, /topics, /timeline, /evidence, /saved-views | 旧全库/Legacy 数据对象调试视图 |

### 中文词汇表

| 后端/工程术语 | 前端显示 |
|---|---|
| Source | 信息源 |
| Run | 抓取任务 |
| dry-run | 预演模式 |
| real-write | 写入模式 |
| Item | 原始信息 |
| Event | 可信事件 |
| Weak Signal | 弱信号 |
| Cluster | 聚合线索 |
| Review Queue | Legacy 待审核队列 |
| Agent Packet | Agent 处理包 |
| Decision Ledger | Agent 决策账本 |
| Briefing / Report | 输出记录 |
| Agent Query | 上下文包查询；旧全库查询为 Legacy/Debug |
| Fresh DB | 当前工作区 |
| Legacy DB | 历史数据库 |

## 主流程

1. **Inbox Loop** (/inbox-loop): 触发或查看 latest registry_full Inbox Run
2. **今日情报** (/today-intel): 分开展示可信事件、弱信号、需要你裁决、静默处理摘要和信息源异常
3. **Agent 处理** (/agent-processing): 查看 Agent Packet、待 Agent 处理、Decision Ledger 和需要你裁决
4. **运行记录** (/runs, /runs/{id}): 查看 run 记录、运行详情和带 scope 的输出触发入口
5. **信息源健康** (/source-health): 查看 selected run 的 source 成功率和异常摘要
6. **输出记录** (/outputs): 查看绑定 run/object/context scope 的简报和报告；历史未绑定输出标记 Legacy
7. **上下文包查询** (/context-query): 默认基于 selected Context Pack 组装回答上下文，不查全库
8. **高级调试 / Legacy**: 旧事件、旧待审核、旧简报、旧报告、旧全库查询和 raw objects 默认折叠

## 视觉设计

- **布局**: 左侧固定侧边栏 + 顶部状态栏 + 主内容区
- **设计标记**: CSS 自定义属性（颜色、排版、间距、圆角、阴影）
- **组件**: 指标卡片、行动卡片、状态徽标、警告横幅、空状态、流水线进度条、事件时间线、调试面板
- **响应式**: 1280px（缩小侧边栏）、860px（折叠为顶部导航）

## HTMX 实时更新

- Run Detail 运行中时，状态指标和事件时间线每 5 秒自动刷新
- 仪表盘最近任务列表每 10 秒自动刷新
- HTMX 是渐进增强，无 JavaScript 时页面仍可完整使用

## 安全边界

- 前端只调用后端 API，不直接读取 SQLite
- Legacy DB 只用于环境校验，不作为业务数据
- reset 仅允许在 Fresh DB 上执行
- real-write 由后端 `CONTENT_INBOX_ENABLE_REAL_RUNS=1` 控制
- 所有危险操作为 Preview → Confirmation → Commit 三步流程

## 测试

```bash
# 后端测试
cd content_inbox
PYTHONPATH=. pytest -q tests/test_ops_api.py

# 前端测试
cd content_inbox_console
PYTHONPATH=. pytest -q
```

## 文档

- `docs/FRONTEND_OPERATING_GUIDE.md` — 用户操作指南
- `docs/FRONTEND_REDESIGN_NOTES.md` — 本轮重构说明
- `docs/ARCHITECTURE.md` — 架构说明
- `docs/DATA_RESET_AND_SAFETY.md` — 数据清理安全策略
