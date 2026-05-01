# RSS / OPML 信息源管理工作区

这个文件夹把 OPML 管理拆成三层：

1. `rss_sources.xlsx`：日常维护入口。之后新增、停用、改分类，优先只改这个 Excel。
2. `scripts/excel_to_opml.py`：把 Excel 转成 OPML。
3. `exports/`：保存脚本导出的 OPML 文件。

## 当前 Excel 结构

`rss_sources.xlsx` 现在按 OPML 一级分类拆成 4 个工作表：

- `Articles`
- `SocialMedia`
- `Pictures`
- `Videos`

每个工作表里的 `category_path` 只填写该一级分类下面的自定义二级/三级分类，不再填写一级分类名。

例如，在 `Articles` 表里：

```text
category_path = 个人博客-人生
```

导出 OPML 后会变成：

```text
Articles/个人博客-人生
```

如果 `category_path` 留空，则该源会直接放在对应一级分类下面。

## 推荐用法

```bash
cd rss_opml_workspace
python3 -m pip install -r requirements.txt
python3 scripts/excel_to_opml.py rss_sources.xlsx exports/myrss.generated.opml --title "My RSS"
```

macOS 也可以尝试直接双击 `export_opml.command`。

`export_opml.command` 会同时生成两份 OPML：

- `exports/myrss.generated.opml`：保留 Excel 中的 RSSHub 地址，适合远程设备使用。
- `exports/myrss.local.generated.opml`：把 `https://macmini-rsshub.tail99ecfa.ts.net` 改成本机 `http://127.0.0.1:1200`，适合在 Mac mini 本机导入和测试。
- `exports/myrss.remote-http.generated.opml`：把远程地址改成 `http://macmini-rsshub.tail99ecfa.ts.net:1200`，适合 HTTPS Serve 连接被关闭时临时使用。

## Excel 维护规则

每个分类页都使用相同字段：

- `enabled`：`Y` 导出，`N` 不导出。
- `category_path`：只写当前工作表下的子分类，例如 `个人博客-人生`、`AI观察`、`开发运维/数据库`。
- `title`：阅读器里显示的名称。
- `xml_url`：RSS/Atom 订阅地址，必须填写。
- `html_url`：网站主页，可选。
- `type`：通常为 `rss`，少数可写 `atom`。
- `priority`：建议用 `P0/P1/P2/P3` 表达信息价值。
- `status`：建议用 `active/review/paused/dead` 表达维护状态。
- `tags/notes`：用于补充主题、来源、清理原因等，不影响导出。

## B 站订阅维护规则

B 站 UP 主订阅维护在 `Videos` 工作表里，当前只订阅“投稿视频”，不订阅“用户动态”。

RSSHub 地址使用：

```text
https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/:uid
```

维护规则：

- `xml_url` 使用 `/bilibili/user/video/:uid`，不要使用 `/bilibili/user/dynamic/:uid`。
- `html_url` 使用 UP 主主页，例如 `https://space.bilibili.com/1366786686`，不要带 `/dynamic`。
- 如果需要关闭 RSS 内容中的视频内嵌，可以把 `xml_url` 改成 `/bilibili/user/video/:uid/1`。
- B 站风控相关参数维护在 `rsshub/.env`，不要写进 Excel 或 OPML。

## 第一轮整理建议

- 不要急着删源，先把低价值源标为 `enabled=N` 或 `status=paused`。
- 每个分类页内部再整理二级分类，避免所有源都堆在一级分类下。
- 优先整理数量最大的 `SocialMedia` 和 `Videos`，它们最容易变成信息噪声。
- 对高价值源标记 `priority=P0/P1`，后续可以只导出核心源或重点订阅。

## 备份说明

- `rss_sources.flat.backup.xlsx` 是上一版单 `Sources` 页结构的备份。
