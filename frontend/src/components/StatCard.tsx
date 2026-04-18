import type { LucideIcon } from "lucide-react";

interface Props {
  label: string;
  value: string | number;
  icon: LucideIcon;
  color?: string;
  sub?: string;
}

export default function StatCard(
  { label, value, icon: Icon, color = "#38bdf8", sub }: Props
) {
  return (
    <div style={{
      background: "#1e293b", border: "1px solid #334155",
      borderRadius: 12, padding: "20px 24px",
      display: "flex", alignItems: "flex-start",
      justifyContent: "space-between"
    }}>
      <div>
        <div style={{ fontSize: 13, color: "#64748b",
                      marginBottom: 8 }}>{label}</div>
        <div style={{ fontSize: 28, fontWeight: 700,
                      color: "#f1f5f9" }}>{value}</div>
        {sub && <div style={{ fontSize: 12, color: "#475569",
                              marginTop: 4 }}>{sub}</div>}
      </div>
      <div style={{
        background: color + "22", borderRadius: 10,
        padding: 10, color
      }}>
        <Icon size={22} />
      </div>
    </div>
  );
}