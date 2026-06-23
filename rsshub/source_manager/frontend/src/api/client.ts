import type {
  BatchPayload,
  BatchRun,
  BatchRunCreate,
  BatchRunItem,
  SettingsPayload,
  Source,
  SourceDetail,
  SourceList,
  SourceStatus,
  SourceType
} from "./types";

const API = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, {
    headers: { "content-type": "application/json", ...(init?.headers || {}) },
    ...init
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  return response.json() as Promise<T>;
}

export interface SourcePayload {
  source_type: SourceType;
  display_name: string;
  status?: SourceStatus;
  category?: string;
  tags?: string[];
  rating?: number;
  notes?: string;
  adapter_id?: string;
  route_path?: string;
  feed_url?: string;
  original_feed_url?: string;
  wechat_identity?: Record<string, unknown>;
  allow_duplicate?: boolean;
}

export const api = {
  listSources(params: URLSearchParams) {
    return request<SourceList>(`/sources?${params.toString()}`);
  },
  createSource(payload: SourcePayload) {
    return request<Source>("/sources", { method: "POST", body: JSON.stringify(payload) });
  },
  updateSource(id: string, payload: Partial<SourcePayload>) {
    return request<Source>(`/sources/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  detail(id: string) {
    return request<SourceDetail>(`/sources/${id}`);
  },
  remove(id: string) {
    return request<Source>(`/sources/${id}`, { method: "DELETE" });
  },
  check(id: string) {
    return request(`/sources/${id}/check`, { method: "POST", body: "{}" });
  },
  fetch(id: string) {
    return request(`/sources/${id}/fetch`, { method: "POST", body: JSON.stringify({ include_raw: false }) });
  },
  batchCheck(payload: BatchPayload) {
    return request<BatchRunCreate>("/sources/check-batch", { method: "POST", body: JSON.stringify(payload) });
  },
  batchFetch(payload: BatchPayload) {
    return request<BatchRunCreate>("/sources/fetch-batch", { method: "POST", body: JSON.stringify(payload) });
  },
  batchRun(id: string) {
    return request<BatchRun>(`/batch-runs/${id}`);
  },
  batchRunItems(id: string) {
    return request<BatchRunItem[]>(`/batch-runs/${id}/items`);
  },
  cancelBatchRun(id: string) {
    return request<BatchRun>(`/batch-runs/${id}/cancel`, { method: "POST", body: "{}" });
  },
  batchUpdate(sourceIds: string[], payload: Partial<Pick<Source, "category" | "tags" | "rating" | "status">>) {
    return request<Source[]>("/sources/batch", { method: "PATCH", body: JSON.stringify({ source_ids: sourceIds, ...payload }) });
  },
  importPreview(kind: "csv" | "opml", content: string, filename?: string) {
    return request(`/imports/${kind}/preview`, { method: "POST", body: JSON.stringify({ content, filename }) });
  },
  importCommit(kind: "csv" | "opml", content: string, strategy: string, filename?: string) {
    return request(`/imports/${kind}/commit`, { method: "POST", body: JSON.stringify({ content, strategy, filename }) });
  },
  importHistory() {
    return request<{ ok: boolean; import_runs: Record<string, unknown>[] }>("/imports/history");
  },
  settings() {
    return request<SettingsPayload>("/settings");
  }
};

export function downloadUrl(path: string) {
  window.location.href = `${API}${path}`;
}
