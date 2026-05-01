# rss_sources.csv 字段说明

当前 CSV 使用单表结构，每一行是一条订阅源。`top_category` 字段对应 OPML 的一级分类：

- Articles
- SocialMedia
- Pictures
- Videos

`category_path` 字段只填写该一级分类下面的自定义子分类，不再重复填写一级分类名。

## 字段

| 字段 | 是否影响导出 | 说明 |
|---|---:|---|
| top_category | 是 | OPML 一级分类，当前使用 `Articles/SocialMedia/Pictures/Videos` |
| enabled | 是 | `Y` 导出，`N` 不导出 |
| category_path | 是 | `top_category` 下的二级/三级分类，例如 `个人博客-人生`、`开发运维/数据库` |
| title | 是 | 阅读器中显示的名称 |
| xml_url | 是 | 远程使用的 RSS/Atom 地址，必填 |
| local_xml_url | 是 | 本机使用的 RSSHub 地址；普通外部源可留空，导出本机版 OPML 时会回退到 `xml_url` |
| html_url | 是 | 网站主页，可选 |
| type | 是 | 通常为 `rss`，少数为 `atom` |
| priority | 否 | 信息价值，建议 `P0/P1/P2/P3` |
| status | 否 | 维护状态，建议 `active/review/paused/dead` |
| tags | 否 | 自定义主题标签 |
| language | 否 | 语言标记 |
| cadence | 否 | 更新频率或阅读频率 |
| owner | 否 | 维护人，可留空 |
| notes | 否 | 清理原因、判断依据、备注 |
| last_checked | 否 | 最后人工检查日期 |
| source_comment | 否 | 导入来源或系统备注 |

## OPML 分类规则

例如：

```text
top_category = Articles
category_path = 个人博客-人生
```

导出后 OPML 分类为：

```text
Articles/个人博客-人生
```

如果 `category_path` 留空，则该源会直接挂在 `top_category` 对应的一级分类下。
