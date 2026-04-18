const colors: Record<string, string> = {
  critical: "#ef4444",
  high:     "#f97316",
  medium:   "#eab308",
  low:      "#22c55e",
};

export default function SeverityBadge({ severity }: { severity: string }) {
  const color = colors[severity] || "#64748b";
  return (
    <span style={{
      background: color + "22", color, border: `1px solid ${color}44`,
      padding: "2px 10px", borderRadius: 99, fontSize: 12, fontWeight: 600,
      textTransform: "uppercase", letterSpacing: "0.05em"
    }}>
      {severity}
    </span>
  );
}