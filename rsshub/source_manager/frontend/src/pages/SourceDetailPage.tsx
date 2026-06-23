import { Activity, ArrowLeft, Edit3, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { SourceDetail } from "../api/types";
import { SourceForm } from "../components/SourceForm";

interface Props {
  sourceId: string;
  onBack: () => void;
}

export function SourceDetailPage({ sourceId, onBack }: Props) {
  const [detail, setDetail] = useState<SourceDetail | null>(null);
  const [editing, setEditing] = useState(false);
  const [message, setMessage] = useState("");

  async function load() {
    setDetail(await api.detail(sourceId));
  }

  useEffect(() => {
    load().catch((error) => setMessage(error.message));
  }, [sourceId]);

  async function run(action: () => Promise<unknown>, done: string) {
    try {
      setMessage("running");
      await action();
      setMessage(done);
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "failed");
    }
  }

  if (!detail) return <div className="notice">loading</div>;
  const source = detail.source;

  return (
    <div className="page-stack">
      <div className="toolbar">
        <button onClick={onBack}><ArrowLeft size={16} aria-hidden="true" />Back</button>
        <h2>{source.display_name}</h2>
        <div className="spacer" />
        <button onClick={() => setEditing(true)}><Edit3 size={16} aria-hidden="true" />Edit</button>
        <button onClick={() => run(() => api.check(sourceId), "check done")}><Activity size={16} aria-hidden="true" />Check</button>
        <button onClick={() => run(() => api.fetch(sourceId), "fetch done")}><RefreshCw size={16} aria-hidden="true" />Fetch</button>
      </div>
      {message && <div className="notice">{message}</div>}
      {editing && (
        <SourceForm
          source={source}
          onSubmit={async (payload) => {
            await api.updateSource(sourceId, payload);
            setEditing(false);
            await load();
          }}
          onCancel={() => setEditing(false)}
        />
      )}
      <section className="detail-grid">
        <div className="panel">
          <h3>元信息</h3>
          <dl>
            <dt>source_id</dt><dd>{source.source_id}</dd>
            <dt>type</dt><dd>{source.source_type}</dd>
            <dt>category</dt><dd>{source.category}</dd>
            <dt>tags</dt><dd>{source.tags.join(", ") || "-"}</dd>
            <dt>rating</dt><dd>{source.rating}</dd>
            <dt>status</dt><dd><span className={`status ${source.status}`}>{source.status}</span></dd>
            <dt>feed</dt><dd>{source.resolved_feed_url || source.feed_url || source.route_path}</dd>
          </dl>
        </div>
        <div className="panel">
          <h3>健康</h3>
          <dl>
            <dt>last_checked_at</dt><dd>{source.last_checked_at || "-"}</dd>
            <dt>last_check_status</dt><dd>{source.last_check_status || "-"}</dd>
            <dt>last_success_at</dt><dd>{source.last_success_at || "-"}</dd>
            <dt>last_failure_at</dt><dd>{source.last_failure_at || "-"}</dd>
            <dt>consecutive_failures</dt><dd>{source.consecutive_failures}</dd>
            <dt>last_error</dt><dd>{source.last_error || "-"}</dd>
          </dl>
        </div>
      </section>
      <section className="panel">
        <h3>最近 entries</h3>
        <div className="table-wrap small">
          <table>
            <thead><tr><th>title</th><th>published</th><th>last seen</th><th>seen</th></tr></thead>
            <tbody>{detail.recent_entries.map((entry) => (
              <tr key={entry.entry_id}><td>{entry.title || entry.url}</td><td>{entry.published_at || "-"}</td><td>{entry.last_seen_at || "-"}</td><td>{entry.seen_count}</td></tr>
            ))}</tbody>
          </table>
        </div>
      </section>
      <section className="panel">
        <h3>最近 fetch_runs</h3>
        <div className="table-wrap small">
          <table>
            <thead><tr><th>run</th><th>status</th><th>scanned</th><th>new</th><th>existing</th><th>reason</th></tr></thead>
            <tbody>{detail.recent_fetch_runs.map((run) => (
              <tr key={run.fetch_run_id}><td>{run.fetch_run_id}</td><td>{run.status}</td><td>{run.scanned_count}</td><td>{run.new_count}</td><td>{run.existing_count}</td><td>{run.stopped_reason || run.error_message || "-"}</td></tr>
            ))}</tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

