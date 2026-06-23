import { Activity, Download, RefreshCw, Save } from "lucide-react";
import { useState } from "react";
import type { SourceStatus } from "../api/types";

interface Props {
  selectedCount: number;
  onCheck: () => void;
  onFetch: () => void;
  onApply: (updates: { category?: string; tags?: string[]; rating?: number; status?: SourceStatus }) => void;
}

export function BatchToolbar({ selectedCount, onCheck, onFetch, onApply }: Props) {
  const disabled = selectedCount === 0;
  const [status, setStatus] = useState("");
  const [category, setCategory] = useState("");
  const [tags, setTags] = useState("");
  const [rating, setRating] = useState("");
  function apply() {
    const updates: { category?: string; tags?: string[]; rating?: number; status?: SourceStatus } = {};
    if (status) updates.status = status as SourceStatus;
    if (category) updates.category = category;
    if (tags) updates.tags = tags.split(",").map((item) => item.trim()).filter(Boolean);
    if (rating) updates.rating = Number(rating);
    onApply(updates);
  }
  return (
    <div className="toolbar batchbar">
      <span className="selection-count">{selectedCount} selected</span>
      <button disabled={disabled} onClick={onCheck} title="Batch check">
        <Activity size={16} aria-hidden="true" />Check
      </button>
      <button disabled={disabled} onClick={onFetch} title="Batch fetch">
        <RefreshCw size={16} aria-hidden="true" />Fetch
      </button>
      <select aria-label="Batch status" value={status} disabled={disabled} onChange={(event) => setStatus(event.target.value)}>
        <option value="">status</option>
        <option value="active">active</option>
        <option value="paused">paused</option>
        <option value="broken">broken</option>
        <option value="disabled">disabled</option>
      </select>
      <input aria-label="Batch category" placeholder="category" disabled={disabled} value={category} onChange={(event) => setCategory(event.target.value)} />
      <input aria-label="Batch tags" placeholder="tags" disabled={disabled} value={tags} onChange={(event) => setTags(event.target.value)} />
      <input aria-label="Batch rating" type="number" min="0" max="100" placeholder="rating" disabled={disabled} value={rating} onChange={(event) => setRating(event.target.value)} />
      <button disabled={disabled} onClick={apply} title="Apply">
        <Save size={16} aria-hidden="true" />Apply
      </button>
      <a className="icon-link" href="/api/v1/exports/csv?mode=clean" title="Clean CSV">
        <Download size={16} aria-hidden="true" />CSV
      </a>
    </div>
  );
}
