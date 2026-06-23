import { Activity, Edit3, Eye, Pause, Play, RefreshCw, Trash2 } from "lucide-react";
import type { Source } from "../api/types";

interface Props {
  sources: Source[];
  selected: Set<string>;
  onSelect: (id: string, selected: boolean) => void;
  onOpen: (source: Source) => void;
  onEdit: (source: Source) => void;
  onCheck: (source: Source) => void;
  onFetch: (source: Source) => void;
  onStatus: (source: Source, status: Source["status"]) => void;
  onDelete: (source: Source) => void;
}

export function SourceTable({ sources, selected, onSelect, onOpen, onEdit, onCheck, onFetch, onStatus, onDelete }: Props) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th><span className="visually-hidden">select</span></th>
            <th>名称</th>
            <th>类型</th>
            <th>分类</th>
            <th>状态</th>
            <th>rating</th>
            <th>最近检查</th>
            <th>最近成功</th>
            <th>连续失败</th>
            <th>最近新增</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {sources.map((source) => (
            <tr key={source.source_id}>
              <td>
                <input
                  type="checkbox"
                  aria-label={`select ${source.display_name}`}
                  checked={selected.has(source.source_id)}
                  onChange={(event) => onSelect(source.source_id, event.target.checked)}
                />
              </td>
              <td>
                <button className="link-button" onClick={() => onOpen(source)}>{source.display_name}</button>
                <small>{source.resolved_feed_url || source.feed_url || source.route_path}</small>
              </td>
              <td>{source.source_type}</td>
              <td>{source.category}</td>
              <td><span className={`status ${source.status}`}>{source.status}</span></td>
              <td>{source.rating}</td>
              <td>{source.last_checked_at || "-"}</td>
              <td>{source.last_success_at || "-"}</td>
              <td>{source.consecutive_failures}</td>
              <td>{source.last_fetch_new_count}</td>
              <td>
                <div className="row-actions">
                  <button aria-label="view" title="View" onClick={() => onOpen(source)}><Eye size={15} /></button>
                  <button aria-label="edit" title="Edit" onClick={() => onEdit(source)}><Edit3 size={15} /></button>
                  <button aria-label="check" title="Check" onClick={() => onCheck(source)}><Activity size={15} /></button>
                  <button aria-label="fetch" title="Fetch" onClick={() => onFetch(source)}><RefreshCw size={15} /></button>
                  <button aria-label="toggle pause" title="Pause or resume" onClick={() => onStatus(source, source.status === "active" ? "paused" : "active")}>
                    {source.status === "active" ? <Pause size={15} /> : <Play size={15} />}
                  </button>
                  <button aria-label="disable" title="Disable" onClick={() => onDelete(source)}><Trash2 size={15} /></button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

