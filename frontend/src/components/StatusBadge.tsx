const colors: Record<string, string> = {
  operational:       "#22c55e",
  degraded:          "#f97316",
  under_maintenance: "#eab308",
  open:              "#ef4444",
  resolved:          "#22c55e",
  in_progress:       "#38bdf8",
};

export default function StatusBadge({ status }: { status: string }) {
  const color = colors[status] || "#64748b";
  return (
    <span style={{
      background: color + "22", color, border: `1px solid ${color}44`,
      padding: "2px 10px", borderRadius: 99, fontSize: 12, fontWeight: 600
    }}>
      {status.replace("_", " ")}
    </span>
  );
}