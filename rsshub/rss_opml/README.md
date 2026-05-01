# RSS / OPML 信息源管理工作区

这个文件夹把 OPML 管理拆成三层：

1. `rss_sources.csv`：日常维护入口。之后新增、停用、改分类，优先只改这个 CSV。
2. `scripts/excel_to_opml.py`：把 CSV 转成 OPML，同时保留旧 XLSX 输入的兼容能力。
3. `exports/`：保存脚本导出的 OPML 文件。

## 当前 CSV 结构

`rss_sources.csv` 使用单表结构，`top_category` 字段对应 OPML 的一级分类：

- `Articles`
- `SocialMedia`
- `Pictures`
- `Videos`

`category_path` 只填写该一级分类下面的自定义二级/三级分类，不再填写一级分类名。

例如：

```text
top_category = Articles
category_path = 个人博客-人生
```

导出 OPML 后会变成：

```text
Articles/个人博客-人生
```

如果 `category_path` 留空，则该源会直接放在对应一级分类下面。

## 推荐用法

```bash
cd /Users/wangrundong/work/infomation-center/rsshub/rss_opml
./export_opml.command
```

macOS 也可以尝试直接双击 `export_opml.command`。

`export_opml.command` 从 `rss_sources.csv` 生成三份 OPML：

- `exports/myrss(远程用).opml`：保留 CSV 中的 RSSHub HTTPS 地址，适合远程设备使用。
- `exports/myrss(本机用).opml`：把 `https://macmini-rsshub.tail99ecfa.ts.net` 改成本机 `http://127.0.0.1:1200`，适合在 Mac mini 本机导入和测试。
- `exports/myrss(远程备用-HTTP).opml`：把远程地址改成 `http://macmini-rsshub.tail99ecfa.ts.net:1200`，适合 HTTPS Serve 连接被关闭时临时使用。

## CSV 维护规则

每一行是一条订阅源：

- `top_category`：OPML 一级分类，当前使用 `Articles/SocialMedia/Pictures/Videos`。
- `enabled`：`Y` 导出，`N` 不导出。
- `category_path`：只写 `top_category` 下的子分类，例如 `个人博客-人生`、`AI观察`、`开发运维/数据库`。
- `title`：阅读器里显示的名称。
- `xml_url`：RSS/Atom 订阅地址，必须填写。
- `html_url`：网站主页，可选。
- `type`：通常为 `rss`，少数可写 `atom`。
- `priority`：建议用 `P0/P1/P2/P3` 表达信息价值。
- `status`：建议用 `active/review/paused/dead` 表达维护状态。
- `tags/notes`：用于补充主题、来源、清理原因等，不影响导出。

## B 站订阅维护规则

B 站 UP 主订阅使用 `top_category=Videos`，当前只订阅“投稿视频”，不订阅“用户动态”。

RSSHub 地址使用：

```text
https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/:uid
```

维护规则：

- `xml_url` 使用 `/bilibili/user/video/:uid`，不要使用 `/bilibili/user/dynamic/:uid`。
- `html_url` 使用 UP 主主页，例如 `https://space.bilibili.com/1366786686`，不要带 `/dynamic`。
- 如果需要关闭 RSS 内容中的视频内嵌，可以把 `xml_url` 改成 `/bilibili/user/video/:uid/1`。
- B 站风控相关参数维护在 `rsshub/.env`，不要写进 CSV 或 OPML。

## 第一轮整理建议

- 不要急着删源，先把低价值源标为 `enabled=N` 或 `status=paused`。
- 每个分类页内部再整理二级分类，避免所有源都堆在一级分类下。
- 优先整理数量最大的 `SocialMedia` 和 `Videos`，它们最容易变成信息噪声。
- 对高价值源标记 `priority=P0/P1`，后续可以只导出核心源或重点订阅。

## 旧文件说明

- `rss_sources.xlsx` 是旧版维护入口，仅保留作备份；后续以 `rss_sources.csv` 为准。
