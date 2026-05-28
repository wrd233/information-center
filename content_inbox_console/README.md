# content_inbox_console

`content_inbox_console` 是 `content_inbox` 的 API-driven 前端作战台。它不是 SQLite 浏览器，也不再扫描 `outputs/runs/` 做业务 fallback；所有主路径都通过后端统一 envelope API：

```json
{ "ok": true, "data": {}, "error": null, "meta": {} }
```

## 启动

后端：

```bash
cd ../content_inbox
CONTENT_INBOX_DB_PATH=data/environments/fresh_default/content_inbox.db \
CONTENT_INBOX_ENABLE_REAL_RUNS=0 \
PYTHONPATH=. python3 -m app.server
```

Console：

```bash
cd content_inbox_console
CONTENT_INBOX_FRONTEND_API_BASE=http://127.0.0.1:8787 \
uvicorn app.main:app --host 127.0.0.1 --port 8788 --reload
```

打开 `http://127.0.0.1:8788`。

## 主流程

1. 作战首页：确认当前环境、Fresh DB、real-write gate、下一步建议。
2. 环境 / Fresh DB：查看 DB identity/path、Legacy DB checksum、健康检查。
3. Source 管理：新增、check、批量导入 preview/commit、导出、编辑、启用/禁用/归档。
4. 创建 Run：选择 source 范围，配置时间和限额，先 dry-run，再 real-write。
5. Run Detail：查看 run events、source progress、items、pipeline stage、briefing/report 按钮。
6. 信息消费：事件中心、review queue、briefing、report、agent query。
7. 数据清理 / 重新开始：按 scope preview-first，然后输入确认文本 commit。
8. 高级调试：Items、Dedupe Groups、Clusters、Entities、Relations、Claims、Topics、Timeline、Evidence、Saved Views。

## 安全边界

- 主前端只调用配置的 backend API，不直接读取 SQLite。
- Legacy DB 只用于后端环境证明中的 checksum/mtime/size，不作为业务数据 fallback。
- reset 只允许在 `is_fresh_database=true` 时执行。
- real-write 由后端 `CONTENT_INBOX_ENABLE_REAL_RUNS=1` gate 控制，前端不能绕过。
- raw JSON 默认折叠，普通用户先看中文摘要和下一步按钮。

## 测试

```bash
cd ../content_inbox
PYTHONPATH=. pytest -q tests/test_ops_api.py

cd ../content_inbox_console
PYTHONPATH=. pytest -q
```

更多设计和维护说明见 `docs/ARCHITECTURE.md`、`docs/FRONTEND_OPERATION_FLOWS.md`、`docs/DATA_RESET_AND_SAFETY.md`、`docs/LOW_COGNITIVE_LOAD_UI.md`。
