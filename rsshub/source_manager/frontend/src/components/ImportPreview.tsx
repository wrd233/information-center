interface Props {
  preview: any;
}

export function ImportPreview({ preview }: Props) {
  if (!preview) return null;
  return (
    <div className="panel">
      <div className="summary-strip compact">
        {Object.entries(preview.summary || {}).map(([key, value]) => (
          <div className="summary-cell" key={key}><span>{key}</span><strong>{String(value)}</strong></div>
        ))}
      </div>
      <div className="table-wrap small">
        <table>
          <thead><tr><th>#</th><th>action</th><th>名称</th><th>类型</th><th>分类</th><th>重复</th></tr></thead>
          <tbody>
            {(preview.items || []).slice(0, 80).map((item: any) => (
              <tr key={item.index}>
                <td>{item.index}</td>
                <td>{item.action}</td>
                <td>{item.source?.display_name}</td>
                <td>{item.source?.source_type}</td>
                <td>{item.source?.category}</td>
                <td>{(item.duplicate_source_ids || []).join(",") || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

