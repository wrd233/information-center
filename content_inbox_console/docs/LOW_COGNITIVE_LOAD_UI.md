# Low Cognitive Load UI

本次前端定位是“信息处理作战台”，不是数据库对象浏览器。

## 原则

- 中文优先，保留必要领域词：source、run、dry-run、real-write、event、review queue、briefing、report、Fresh DB、Legacy DB。
- 普通路径先展示“我在哪、安全吗、下一步做什么”。
- 危险操作和普通操作分区，危险区必须 preview-first。
- JSON 默认折叠，只有高级调试才展开。
- 每个空状态都告诉用户下一步。
- 一级导航服务任务，高级对象折叠到“高级调试”。

## 页面模式

- Page Header：标题 + 一句话解释 + 主操作。
- Status Strip：环境、DB path、real-write、Legacy fallback。
- Stat Card：source/item/run/review 等关键数字。
- Next Action Card：下一步建议和按钮。
- Preview Panel：危险操作影响预览。
- Danger Zone：reset、archive、real-write 等。
- Data Table：搜索/过滤/批量操作。
- Raw JSON Collapse：原始 envelope/debug 数据。
- Timeline：run events。

## 当前落地

- `templates/components/nav.html`：按任务分组的导航。
- `templates/base.html`：全局 status strip 和错误摘要。
- `templates/ops/dashboard.html`：下一步建议、最近 run、review、briefing/report。
- `templates/ops/data_reset.html`：独立 reset 页面。
- `static/css/app.css`：统一后台风格、badge、danger zone、preview panel、响应式布局。

## Accessibility Notes

- 使用语义化 header/nav/main/section/article。
- 操作按钮保留文本，不只靠颜色。
- danger/warning 同时使用文字和边框。
- 移动端降为单列，导航横向滚动但不阻塞内容。
