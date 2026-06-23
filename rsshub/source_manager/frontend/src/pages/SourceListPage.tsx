import { Plus } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { api, type SourcePayload } from "../api/client";
import type { Source, SourceStatus, SourceType } from "../api/types";
import { BatchToolbar } from "../components/BatchToolbar";
import { HealthSummary } from "../components/HealthSummary";
import { SourceForm } from "../components/SourceForm";
import { SourceTable } from "../components/SourceTable";
import { SourceDetailPage } from "./SourceDetailPage";

export function SourceListPage() {
  const [sources, setSources] = useState<Source[]>([]);
  const [stats, setStats] = useState<Record<string, unknown>>({});
  const [total, setTotal] = useState(0);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [search, setSearch] = useState("");
  const [sourceType, setSourceType] = useState("");
  const [status, setStatus] = useState("");
  const [editing, setEditing] = useState<Source | null>(null);
  const [creating, setCreating] = useState<SourceType | null>(null);
  const [detail, setDetail] = useState<string | null>(null);
  const [message, setMessage] = useState("");

  async function load() {
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (sourceType) params.set("source_type", sourceType);
    if (status) params.set("status", status);
    params.set("limit", "300");
    const result = await api.listSources(params);
    setSources(result.sources);
    setStats(result.stats);
    setTotal(result.total);
  }

  useEffect(() => {
    load().catch((error) => setMessage(error.message));
  }, [search, sourceType, status]);

  const selectedIds = useMemo(() => Array.from(selected), [selected]);

  async function save(payload: SourcePayload) {
    if (editing) await api.updateSource(editing.source_id, payload);
    else await api.createSource(payload);
    setEditing(null);
    setCreating(null);
    await load();
  }

  async function run(action: () => Promise<unknown>, done = "done") {
    try {
      setMessage("running");
      await action();
      setMessage(done);
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "failed");
    }
  }

  if (detail) {
    return <SourceDetailPage sourceId={detail} onBack={() => { setDetail(null); load(); }} />;
  }

  return (
    <div className="page-stack">
      <HealthSummary stats={stats} total={total} />
      <div className="toolbar">
        <input aria-label="Search sources" placeholder="search" value={search} onChange={(event) => setSearch(event.target.value)} />
        <select aria-label="Source type" value={sourceType} onChange={(event) => setSourceType(event.target.value)}>
          <option value="">type</option>
          <option value="rsshub">rsshub</option>
          <option value="wechat">wechat</option>
          <option value="native">native</option>
        </select>
        <select aria-label="Status" value={status} onChange={(event) => setStatus(event.target.value)}>
          <option value="">status</option>
          <option value="active">active</option>
          <option value="paused">paused</option>
          <option value="broken">broken</option>
          <option value="disabled">disabled</option>
        </select>
        <div className="spacer" />
        <button onClick={() => setCreating("rsshub")}><Plus size={16} aria-hidden="true" />RSSHub</button>
        <button onClick={() => setCreating("wechat")}><Plus size={16} aria-hidden="true" />微信</button>
        <button onClick={() => setCreating("native")}><Plus size={16} aria-hidden="true" />RSS/Atom</button>
      </div>
      <BatchToolbar
        selectedCount={selected.size}
        onCheck={() => run(() => api.batchCheck(selectedIds), "batch check done")}
        onFetch={() => run(() => api.batchFetch(selectedIds), "batch fetch done")}
        onApply={(updates) => run(() => api.batchUpdate(selectedIds, updates), "batch update done")}
      />
      {message && <div className="notice">{message}</div>}
      {(editing || creating) && (
        <SourceForm
          source={editing}
          initialType={creating || editing?.source_type || "native"}
          onSubmit={save}
          onCancel={() => { setEditing(null); setCreating(null); }}
        />
      )}
      <SourceTable
        sources={sources}
        selected={selected}
        onSelect={(id, isSelected) => {
          const copy = new Set(selected);
          if (isSelected) copy.add(id); else copy.delete(id);
          setSelected(copy);
        }}
        onOpen={(source) => setDetail(source.source_id)}
        onEdit={(source) => setEditing(source)}
        onCheck={(source) => run(() => api.check(source.source_id), "check done")}
        onFetch={(source) => run(() => api.fetch(source.source_id), "fetch done")}
        onStatus={(source, nextStatus: SourceStatus) => run(() => api.updateSource(source.source_id, { status: nextStatus }), "status updated")}
        onDelete={(source) => run(() => api.remove(source.source_id), "disabled")}
      />
    </div>
  );
}

