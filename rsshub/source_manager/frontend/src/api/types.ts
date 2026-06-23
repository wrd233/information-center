export type SourceType = "rsshub" | "wechat" | "native";
export type SourceStatus = "active" | "paused" | "broken" | "disabled";

export interface Source {
  source_id: string;
  source_type: SourceType;
  display_name: string;
  status: SourceStatus;
  category: string;
  tags: string[];
  rating: number;
  notes?: string | null;
  adapter_id?: string | null;
  route_path?: string | null;
  feed_url?: string | null;
  original_feed_url?: string | null;
  resolved_feed_url?: string | null;
  wechat_identity: Record<string, unknown>;
  last_checked_at?: string | null;
  last_check_status?: string | null;
  last_success_at?: string | null;
  last_failure_at?: string | null;
  consecutive_failures: number;
  last_error?: string | null;
  total_entries_seen: number;
  last_fetch_new_count: number;
  last_fetch_existing_count: number;
  last_fetch_scanned_count: number;
}

export interface SourceList {
  ok: boolean;
  sources: Source[];
  total: number;
  stats: Record<string, unknown>;
}

export interface Entry {
  entry_id: string;
  title?: string | null;
  url?: string | null;
  published_at?: string | null;
  last_seen_at?: string | null;
  seen_count: number;
  summary_excerpt?: string | null;
}

export interface FetchRun {
  fetch_run_id: string;
  status: string;
  started_at?: string | null;
  finished_at?: string | null;
  scanned_count: number;
  new_count: number;
  existing_count: number;
  stopped_reason?: string | null;
  error_message?: string | null;
}

export interface SourceDetail {
  ok: boolean;
  source: Source;
  recent_entries: Entry[];
  recent_fetch_runs: FetchRun[];
}

export interface SettingsPayload {
  ok: boolean;
  database_path: string;
  config_path: string;
  server: Record<string, unknown>;
  adapters: Record<string, Record<string, unknown>>;
  export_profiles: Record<string, Record<string, unknown>>;
  categories: string[];
  health: Record<string, unknown>;
  fetch: Record<string, unknown>;
  batch_fetch: Record<string, unknown>;
  docs_url: string;
}

