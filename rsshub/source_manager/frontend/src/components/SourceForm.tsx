import { Save, X } from "lucide-react";
import { useState } from "react";
import type { Source, SourceType } from "../api/types";
import type { SourcePayload } from "../api/client";

interface Props {
  source?: Source | null;
  initialType?: SourceType;
  onSubmit: (payload: SourcePayload) => void;
  onCancel: () => void;
}

export function SourceForm({ source, initialType = "native", onSubmit, onCancel }: Props) {
  const [sourceType, setSourceType] = useState<SourceType>(source?.source_type || initialType);
  const [displayName, setDisplayName] = useState(source?.display_name || "");
  const [category, setCategory] = useState(source?.category || "未分类");
  const [tags, setTags] = useState((source?.tags || []).join(","));
  const [rating, setRating] = useState(source?.rating || 50);
  const [status, setStatus] = useState(source?.status || "paused");
  const [routePath, setRoutePath] = useState(source?.route_path || "");
  const [feedUrl, setFeedUrl] = useState(source?.feed_url || "");
  const [originalFeedUrl, setOriginalFeedUrl] = useState(source?.original_feed_url || "");
  const [notes, setNotes] = useState(source?.notes || "");
  const [wechatJson, setWechatJson] = useState(JSON.stringify(source?.wechat_identity || {}, null, 2));

  function submit(event: React.FormEvent) {
    event.preventDefault();
    let wechat_identity: Record<string, unknown> = {};
    try {
      wechat_identity = wechatJson.trim() ? JSON.parse(wechatJson) : {};
    } catch {
      wechat_identity = {};
    }
    onSubmit({
      source_type: sourceType,
      display_name: displayName,
      category,
      tags: tags.split(",").map((item) => item.trim()).filter(Boolean),
      rating,
      status,
      route_path: routePath || undefined,
      feed_url: feedUrl || undefined,
      original_feed_url: originalFeedUrl || undefined,
      notes,
      wechat_identity
    });
  }

  return (
    <form className="panel form-grid" onSubmit={submit}>
      <label>类型
        <select value={sourceType} onChange={(event) => setSourceType(event.target.value as SourceType)} disabled={Boolean(source)}>
          <option value="rsshub">rsshub</option>
          <option value="wechat">wechat</option>
          <option value="native">native</option>
        </select>
      </label>
      <label>名称<input required value={displayName} onChange={(event) => setDisplayName(event.target.value)} /></label>
      <label>分类<input value={category} onChange={(event) => setCategory(event.target.value)} /></label>
      <label>tags<input value={tags} onChange={(event) => setTags(event.target.value)} /></label>
      <label>rating<input type="number" min="0" max="100" value={rating} onChange={(event) => setRating(Number(event.target.value))} /></label>
      <label>状态
        <select value={status} onChange={(event) => setStatus(event.target.value as Source["status"])}>
          <option value="active">active</option>
          <option value="paused">paused</option>
          <option value="broken">broken</option>
          <option value="disabled">disabled</option>
        </select>
      </label>
      {sourceType === "rsshub" && <label className="wide">route_path<input required value={routePath} onChange={(event) => setRoutePath(event.target.value)} /></label>}
      {sourceType !== "rsshub" && <label className="wide">feed_url<input required value={feedUrl} onChange={(event) => setFeedUrl(event.target.value)} /></label>}
      <label className="wide">original_feed_url<input value={originalFeedUrl} onChange={(event) => setOriginalFeedUrl(event.target.value)} /></label>
      {sourceType === "wechat" && <label className="wide">wechat_identity<textarea value={wechatJson} onChange={(event) => setWechatJson(event.target.value)} /></label>}
      <label className="wide">notes<textarea value={notes} onChange={(event) => setNotes(event.target.value)} /></label>
      <div className="form-actions wide">
        <button type="submit"><Save size={16} aria-hidden="true" />Save</button>
        <button type="button" onClick={onCancel}><X size={16} aria-hidden="true" />Cancel</button>
      </div>
    </form>
  );
}

