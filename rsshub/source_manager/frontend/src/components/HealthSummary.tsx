interface Props {
  stats: Record<string, unknown>;
  total: number;
}

export function HealthSummary({ stats, total }: Props) {
  const cells: Array<[string, unknown]> = [
    ["总源数", total],
    ["active", stats.active ?? 0],
    ["broken", stats.broken ?? 0],
    ["最近抓取", stats.latest_success_at ?? "-"],
    ["最近新增", stats.recent_new_entries ?? 0]
  ];
  return (
    <section className="summary-strip" aria-label="health summary">
      {cells.map(([label, value]) => (
        <div className="summary-cell" key={label}>
          <span>{label}</span>
          <strong>{String(value)}</strong>
        </div>
      ))}
    </section>
  );
}
