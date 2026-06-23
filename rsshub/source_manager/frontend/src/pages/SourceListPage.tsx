import { Plus } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { api, type SourcePayload } from "../api/client";
import type { BatchAction, BatchFilter, BatchRun, BatchRunItem, Source, SourceStatus, SourceType } from "../api/types";
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
  const [allFilteredSelected, setAllFilteredSelected] = useState(false);
  const [search, setSearch] = useState("");
  const [sourceType, setSourceType] = useState("");
  const [status, setStatus] = useState("");
  const [editing, setEditing] = useState<Source | null>(null);
  const [creating, setCreating] = useState<SourceType | null>(null);
  const [detail, setDetail] = useState<string | null>(null);
  const [message, setMessage] = useState("");
  const [activeBatch, setActiveBatch] = useState<{ id: string; action: BatchAction } | null>(null);
  const [batchRun, setBatchRun] = useState<BatchRun | null>(null);
  const [batchItems, setBatchItems] = useState<BatchRunItem[]>([]);
  const [rowRunning, setRowRunning] = useState<Record<string, "check" | "fetch" | undefined>>({});

  function sourceParams(limit = 300) {
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (sourceType) params.set("source_type", sourceType);
    if (status) params.set("status", status);
    params.set("limit", String(limit));
    return params;
  }

  async function load() {
    const params = sourceParams();
    const result = await api.listSources(params);
    setSources(result.sources);
    setStats(result.stats);
    setTotal(result.total);
  }

  useEffect(() => {
    load().catch((error) => setMessage(error.message));
  }, [search, sourceType, status]);

  const selectedIds = useMemo(() => Array.from(selected), [selected]);
  const selectedCount = allFilteredSelected ? total : selected.size;
  const allVisibleSelected = sources.length > 0 && sources.every((source) => selected.has(source.source_id));
  const partiallySelected = selected.size > 0 && !allVisibleSelected;
  const canSelectFiltered = allVisibleSelected && total > sources.length && !allFilteredSelected;
  const currentFilter = useMemo<BatchFilter>(() => {
    const filter: BatchFilter = {};
    if (sourceType) filter.source_types = [sourceType as SourceType];
    if (status) filter.statuses = [status as SourceStatus];
    if (search) filter.search = search;
    return filter;
  }, [sourceType, status, search]);

  useEffect(() => {
    if (allFilteredSelected) {
      setSelected(new Set(sources.map((source) => source.source_id)));
    }
  }, [sources, allFilteredSelected]);

  useEffect(() => {
    if (!activeBatch) return;
    const batch = activeBatch;
    let cancelled = false;
    async function poll() {
      try {
        const [run, items] = await Promise.all([api.batchRun(batch.id), api.batchRunItems(batch.id)]);
        if (cancelled) return;
        setBatchRun(run);
        setBatchItems(items);
        if (["succeeded", "partial_success", "failed", "cancelled"].includes(run.status)) {
          setActiveBatch(null);
          await load();
        }
      } catch (error) {
        if (!cancelled) setMessage(error instanceof Error ? error.message : "batch polling failed");
      }
    }
    poll();
    const timer = window.setInterval(poll, 1000);
    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, [activeBatch]);

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

  async function runSingle(source: Source, action: BatchAction) {
    try {
      setRowRunning((current) => ({ ...current, [source.source_id]: action }));
      setMessage(action === "check" ? "检查中" : "抓取中");
      const result = action === "check" ? await api.check(source.source_id) : await api.fetch(source.source_id);
      const ok = Boolean((result as { ok?: boolean }).ok);
      setMessage(ok ? (action === "check" ? "检查完成" : "抓取完成") : (action === "check" ? "检查失败" : "抓取失败"));
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "failed");
    } finally {
      setRowRunning((current) => {
        const next = { ...current };
        delete next[source.source_id];
        return next;
      });
    }
  }

  function batchPayload() {
    return allFilteredSelected ? { filter: currentFilter } : { source_ids: selectedIds };
  }

  async function startBatch(action: BatchAction) {
    if (selectedCount === 0) return;
    const verb = action === "check" ? "批量检查" : "批量抓取";
    if (!window.confirm(`将对 ${selectedCount} 个源执行${verb}`)) return;
    try {
      const created = action === "check" ? await api.batchCheck(batchPayload()) : await api.batchFetch(batchPayload());
      setActiveBatch({ id: created.batch_run_id, action });
      setBatchRun(null);
      setBatchItems([]);
      setMessage(`${verb}已启动`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "batch failed");
    }
  }

  async function cancelBatch() {
    if (!activeBatch) return;
    await api.cancelBatchRun(activeBatch.id);
    setMessage("正在停止：不再启动新的源，当前运行中的源完成后停止。");
  }

  async function selectedIdsForUpdate() {
    if (!allFilteredSelected) return selectedIds;
    const result = await api.listSources(sourceParams(1000));
    return result.sources.map((source) => source.source_id);
  }

  async function applyBatchUpdate(updates: { category?: string; tags?: string[]; rating?: number; status?: SourceStatus }) {
    if (selectedCount === 0) return;
    if (!window.confirm(`将对 ${selectedCount} 个源执行批量编辑`)) return;
    const ids = await selectedIdsForUpdate();
    await api.batchUpdate(ids, updates);
  }

  function formatElapsed(ms?: number | null) {
    if (!ms) return "00:00";
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    return `${String(minutes).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
  }

  function batchMessage() {
    if (!batchRun) return message;
    const verb = batchRun.action === "check" ? "检查" : "抓取";
    if (batchRun.status === "cancelling") return "正在停止：不再启动新的源，当前运行中的源完成后停止。";
    const prefix = ["succeeded", "partial_success", "failed", "cancelled"].includes(batchRun.status)
      ? `批量${verb}完成`
      : `批量${verb}中`;
    return `${prefix}：总数 ${batchRun.total_count}，运行中 ${batchRun.running_count}，成功 ${batchRun.success_count}，失败 ${batchRun.failed_count}，跳过 ${batchRun.skipped_count}，耗时 ${formatElapsed(batchRun.elapsed_ms)}`;
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
        selectedCount={selectedCount}
        isBatchRunning={!!activeBatch}
        onCheck={() => startBatch("check")}
        onFetch={() => startBatch("fetch")}
        onCancel={cancelBatch}
        onApply={(updates) => run(() => applyBatchUpdate(updates), "batch update done")}
      />
      {(message || batchRun) && <div className="notice">{batchMessage()}</div>}
      {(selected.size > 0 || allFilteredSelected) && (
        <div className="selection-hint">
          {allFilteredSelected ? (
            <>
              已选择当前筛选结果中的全部 {total} 个源。
              <button className="link-button" onClick={() => { setSelected(new Set()); setAllFilteredSelected(false); }}>清除选择</button>
            </>
          ) : (
            <>
              已选择当前页 {selected.size} 个源。
              {canSelectFiltered && (
                <button className="link-button" onClick={() => setAllFilteredSelected(true)}>
                  选择当前筛选结果中的全部 {total} 个源
                </button>
              )}
            </>
          )}
        </div>
      )}
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
        allVisibleSelected={allVisibleSelected}
        partiallySelected={partiallySelected}
        runningBySource={{ ...rowRunning, ...Object.fromEntries(batchItems.filter((item) => item.status === "running").map((item) => [item.source_id, activeBatch?.action])) }}
        onSelect={(id, isSelected) => {
          const copy = new Set(selected);
          if (isSelected) copy.add(id); else copy.delete(id);
          setSelected(copy);
          setAllFilteredSelected(false);
        }}
        onSelectVisible={(isSelected) => {
          setSelected(isSelected ? new Set(sources.map((source) => source.source_id)) : new Set());
          setAllFilteredSelected(false);
        }}
        onOpen={(source) => setDetail(source.source_id)}
        onEdit={(source) => setEditing(source)}
        onCheck={(source) => runSingle(source, "check")}
        onFetch={(source) => runSingle(source, "fetch")}
        onStatus={(source, nextStatus: SourceStatus) => run(() => api.updateSource(source.source_id, { status: nextStatus }), "status updated")}
        onDelete={(source) => run(() => api.remove(source.source_id), "disabled")}
      />
    </div>
  );
}
