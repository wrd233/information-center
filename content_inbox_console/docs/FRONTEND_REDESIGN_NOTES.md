# 前端重构说明 — 低心智负担作战台

## 1. 本轮重构目标

将 `content_inbox_console` 从前端工程控制台深度重构为"低心智负担、中文优先、任务流驱动"的信息中心作战台。

### 重构前的问题

- 视觉像未设计的调试页（Pico CSS 默认样式）
- 导航暴露过多后端对象（Items/Dedupe/Clusters/Entities/Relations 等平铺在主导航）
- 缺乏任务流引导，用户不知道先点哪里
- 中英文混杂，技术术语没有解释
- 空状态不友好，没有下一步行动建议
- 表单过于裸露，没有分组和帮助文本
- htmx 已加载但未使用，长时间任务不可观测

### 重构后的改进

- 完整的自定义 CSS 设计系统，移除 Pico CSS 依赖
- 左侧固定侧边栏导航，5 个清晰分组，高级对象默认折叠
- 中文优先词汇表，英文作为括注保留
- 任务流驱动的心智模型：准备 → 执行 → 处理 → 消费 → 维护
- 所有核心页面有空白状态和下一步行动引导
- 卡片式布局、状态徽标、流水线进度条等丰富组件
- HTMX 局部刷新实现任务状态实时观测

## 2. 信息架构变化

### 旧导航结构
```
水平导航栏 → 环境 | Sources | 创建 Run | Runs | 事件 | 待审核 | Briefing | Report | Agent | 数据清理 | 设置 | 高级(...)
```

### 新导航结构
```
左侧固定侧边栏
├── 信息中心 / 作战台 (品牌)
├── [环境指示器: DB | real-write badge]
├── 作战首页
├── 开始使用
│   ├── 信息源
│   ├── 创建任务
│   └── 任务历史
├── 信息消费
│   ├── 事件
│   ├── 待审核
│   ├── 简报
│   ├── 报告
│   └── 智能查询
├── 维护
│   ├── 数据清理
│   ├── 环境
│   └── 设置
└── 高级调试 (默认折叠)
    ├── 原始信息、去重组、聚合线索
    ├── 实体、关系、断言、主题
    └── 时间线、证据、视图
```

## 3. 视觉系统说明

### CSS 架构

| 文件 | 内容 |
|------|------|
| `static/css/tokens.css` | CSS 自定义属性：颜色、排版、间距、圆角、阴影、过渡、布局尺寸 |
| `static/css/reset.css` | 标准化 CSS 重置、表单样式、表格样式 |
| `static/css/layout.css` | 应用外壳网格（侧边栏+顶部栏+主内容区）、响应式断点 |
| `static/css/components.css` | 可复用组件：卡片、按钮、徽标、警告、空状态、表单、流水线等 |
| `static/css/utilities.css` | 间距、排版、弹性布局辅助类 |

### 设计标记（Design Tokens）

- **颜色**: 保留原有 ink/muted/paper/panel/line/accent 色调，扩展 warn/ok/danger/info 语义色
- **排版**: PingFang SC / Microsoft YaHei 中文字体栈，6 级字号
- **间距**: 6 级间距（xs ~ 3xl）
- **布局**: --sidebar-width: 220px, --topbar-height: 48px
- **响应式断点**: 1280px（缩小侧边栏至 200px）、860px（折叠为顶部导航）

### 关键组件

- `.metric-card` — 大数字 + 小标签 + 颜色编码趋势的指标卡片
- `.action-card` — 图标 + 标题 + 描述 + CTA 按钮的下一步行动卡片
- `.status-badge` — success/warning/danger/muted/info 状态徽标
- `.pipeline-stepper` — 流水线阶段进度条
- `.event-timeline` — 运行事件时间线
- `.empty-state` — 空白状态（图标 + 标题 + 描述 + 行动按钮）
- `.debug-panel` — 可折叠的原始数据面板
- `.hero-panel` — 首页 Hero 区域
- `.mode-cards` — 预演/写入模式对比卡片

## 4. 路由变化

### 新增路由

| 路由 | 用途 |
|------|------|
| `GET /runs/{run_id}/fragment/status` | HTMX 片段：运行状态 + 流水线进度 |
| `GET /runs/{run_id}/fragment/timeline` | HTMX 片段：运行事件时间线 |
| `GET /dashboard/fragment/recent` | HTMX 片段：最近任务列表 |

### 修改路由

| 路由 | 变化 |
|------|------|
| `GET /events` | 从 `simple_list.html` 改为专用 `events.html` 模板 |

### 保留兼容

所有现有路由均保留，无删除。书签和测试不会失效。

## 5. 模板变化

### 新建文件 (~20)

- 5 个 CSS 文件 (tokens.css ~ utilities.css)
- 2 个布局组件 (sidebar.html, topbar.html)
- 3 个 HTMX 片段 (run_status, run_timeline, dashboard_recent)
- 1 个专用事件页 (events.html)
- 2 个文档 (FRONTEND_OPERATING_GUIDE.md, FRONTEND_REDESIGN_NOTES.md)

### 重写文件 (~18)

- base.html, nav.html, db_selector.html
- dashboard.html, sources.html, run_wizard.html, run_preview.html, run_detail.html, data_reset.html
- review_queue.html, briefings.html, reports.html, agent_query.html
- simple_list.html, object_detail.html, items.html, item_detail.html
- environment.html, runs.html, settings.html, source_detail.html

### 修改文件

- app/routes/ops.py: events 路由改为专用模板 + 新增 3 个 HTMX 片段路由
- tests/test_api.py: 完全重写测试覆盖

## 6. 后端 API 影响

**无后端 API 改动。** 本轮重构仅修改前端模板、CSS 和路由逻辑，所有后端 `/api/*` 契约保持不变。

## 7. 测试结果

### 前端测试
```bash
cd content_inbox_console && PYTHONPATH=. pytest -q
# 10 passed
```

测试覆盖：
- 所有核心和调试页面返回 200
- 新布局结构（sidebar + topbar + app-shell）存在
- 中文优先词汇出现在各页面
- HTMX 片段路由返回 200
- 空状态和导航分组存在

### 后端测试
```bash
cd content_inbox && PYTHONPATH=. pytest tests/test_ops_api.py -q
# 13 passed
```

## 8. 未完成但建议后续做的事项

1. **Playwright/E2E 测试**: 目前仅做路由测试，建议增加浏览器端到端测试验证视觉和交互
2. **深色主题**: 当前仅支持浅色主题，设计系统已预留暗色主题扩展点
3. **搜索功能增强**: 信息源和条目的全文搜索可以进一步提升
4. **通知/告警**: 任务失败或异常时的桌面通知
5. **i18n 完整国际化**: 目前中文硬编码在模板中，可提取为翻译文件
6. **运行历史图表**: 任务执行趋势的图表可视化
7. **Source 分组/标签管理**: 更丰富的信息源组织能力
