import { CheckCircle, Download, Upload } from "lucide-react";
import { useEffect, useState } from "react";
import { api, downloadUrl } from "../api/client";
import { ImportPreview } from "../components/ImportPreview";

export function ImportExportPage() {
  const [kind, setKind] = useState<"csv" | "opml">("csv");
  const [fileName, setFileName] = useState("");
  const [content, setContent] = useState("");
  const [strategy, setStrategy] = useState("skip");
  const [preview, setPreview] = useState<any>(null);
  const [history, setHistory] = useState<Record<string, unknown>[]>([]);
  const [createdIds, setCreatedIds] = useState<string[]>([]);
  const [message, setMessage] = useState("");

  async function loadHistory() {
    const result = await api.importHistory();
    setHistory(result.import_runs);
  }

  useEffect(() => {
    loadHistory().catch(() => undefined);
  }, []);

  async function readFile(file: File | null) {
    if (!file) return;
    setFileName(file.name);
    setContent(await file.text());
  }

  async function doPreview() {
    const result = await api.importPreview(kind, content, fileName);
    setPreview(result);
  }

  async function doCommit() {
    const result: any = await api.importCommit(kind, content, strategy, fileName);
    setCreatedIds(result.created_source_ids || []);
    setMessage(JSON.stringify(result.summary));
    await loadHistory();
  }

  async function checkCreated() {
    const result = await api.batchCheck({ source_ids: createdIds });
    setMessage(`batch check started: ${result.batch_run_id}`);
  }

  return (
    <div className="page-stack">
      <section className="panel import-grid">
        <label>类型
          <select value={kind} onChange={(event) => setKind(event.target.value as "csv" | "opml")}>
            <option value="csv">CSV</option>
            <option value="opml">OPML</option>
          </select>
        </label>
        <label>文件<input type="file" accept={kind === "csv" ? ".csv,text/csv" : ".opml,.xml,text/xml"} onChange={(event) => readFile(event.target.files?.[0] || null)} /></label>
        <label>策略
          <select value={strategy} onChange={(event) => setStrategy(event.target.value)}>
            <option value="skip">skip</option>
            <option value="fill_empty">fill_empty</option>
            <option value="overwrite_metadata">overwrite_metadata</option>
            <option value="overwrite_all">overwrite_all</option>
          </select>
        </label>
        <div className="toolbar wide">
          <button disabled={!content} onClick={doPreview}><Upload size={16} aria-hidden="true" />Preview</button>
          <button disabled={!preview} onClick={doCommit}><CheckCircle size={16} aria-hidden="true" />Commit</button>
          <button disabled={createdIds.length === 0} onClick={checkCreated}><CheckCircle size={16} aria-hidden="true" />Check</button>
        </div>
      </section>
      {message && <div className="notice">{message}</div>}
      <ImportPreview preview={preview} />
      <section className="panel">
        <div className="toolbar">
          <button onClick={() => downloadUrl("/exports/csv?mode=clean")}><Download size={16} aria-hidden="true" />CSV clean</button>
          <button onClick={() => downloadUrl("/exports/csv?mode=full")}><Download size={16} aria-hidden="true" />CSV full</button>
          <button onClick={() => downloadUrl("/exports/opml?profile=local")}><Download size={16} aria-hidden="true" />OPML local</button>
          <button onClick={() => downloadUrl("/exports/opml?profile=original")}><Download size={16} aria-hidden="true" />OPML original</button>
        </div>
      </section>
      <section className="panel">
        <h3>import history</h3>
        <div className="table-wrap small">
          <table>
            <thead><tr><th>run</th><th>type</th><th>status</th><th>created</th><th>updated</th><th>skipped</th></tr></thead>
            <tbody>{history.map((run) => (
              <tr key={String(run.import_run_id)}><td>{String(run.import_run_id)}</td><td>{String(run.import_type)}</td><td>{String(run.status)}</td><td>{String(run.created_count)}</td><td>{String(run.updated_count)}</td><td>{String(run.skipped_count)}</td></tr>
            ))}</tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
