import { useEffect, useState } from "react";
import {
  Server, AlertTriangle, Wrench,
  Activity, Building2, TrendingUp
} from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  PieChart, Pie, Cell, ResponsiveContainer
} from "recharts";
import StatCard from "../components/StatCard";
import SeverityBadge from "../components/SeverityBadge";
import {
  fetchPlantSummary, fetchIncidents,
  fetchHighRiskAssets, fetchGraphStats
} from "../api/client";
import type { PlantSummary, Incident } from "../types";

const PIE_COLORS = ["#ef4444","#f97316","#eab308","#22c55e"];

export default function Dashboard() {
  const [plants, setPlants]     = useState<PlantSummary[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [riskAssets, setRisk]   = useState<any[]>([]);
  const [stats, setStats]       = useState<any[]>([]);
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    Promise.all([
      fetchPlantSummary(),
      fetchIncidents(),
      fetchHighRiskAssets(),
      fetchGraphStats()
    ]).then(([p, i, r, s]) => {
      setPlants(p.data.plants);
      setIncidents(i.data.incidents);
      setRisk(r.data.high_risk_assets);
      setStats(s.data.graph_statistics);
      setLoading(false);
    });
  }, []);

  if (loading) return (
    <div style={{ color: "#64748b", paddingTop: 80, textAlign: "center" }}>
      Loading knowledge graph...
    </div>
  );

  const totalAssets  = plants.reduce((s, p) => s + p.total_assets, 0);
  const totalInc     = plants.reduce((s, p) => s + p.total_incidents, 0);
  const totalCost    = plants.reduce(
    (s, p) => s + (p.total_maintenance_cost_usd || 0), 0
  );

  // Severity distribution for pie chart
  const sevCounts = ["critical","high","medium","low"].map(sev => ({
    name: sev,
    value: incidents.filter(i => i.severity === sev).length
  })).filter(x => x.value > 0);

  // Incidents per plant for bar chart
  const plantBar = plants.map(p => ({
    name: p.plant_name.split(" ").slice(-1)[0],
    incidents: p.total_incidents,
    assets: p.total_assets
  }));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 28 }}>

      {/* Header */}
      <div>
        <h1 style={{ fontSize: 22, fontWeight: 700, color: "#f1f5f9",
                     margin: 0 }}>Operations Overview</h1>
        <p style={{ color: "#64748b", marginTop: 4, fontSize: 14 }}>
          Industrial Asset Knowledge Graph — Real-time Intelligence
        </p>
      </div>

      {/* Stat cards */}
      <div style={{ display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(200px,1fr))",
                    gap: 16 }}>
        <StatCard label="Total Assets"    value={totalAssets}
                  icon={Server}           color="#38bdf8" />
        <StatCard label="Total Incidents" value={totalInc}
                  icon={AlertTriangle}    color="#f97316" />
        <StatCard label="High Risk Assets" value={riskAssets.length}
                  icon={Activity}         color="#ef4444" />
        <StatCard label="Maintenance Cost"
                  value={`$${(totalCost/1000).toFixed(0)}k`}
                  icon={Wrench}           color="#a78bfa" />
        <StatCard label="Plants Monitored" value={plants.length}
                  icon={Building2}        color="#34d399" />
        <StatCard label="Graph Nodes"
                  value={stats.reduce((s,x) => s + x.count, 0)}
                  icon={TrendingUp}       color="#fbbf24"
                  sub="across all entity types" />
      </div>

      {/* Charts row */}
      <div style={{ display: "grid",
                    gridTemplateColumns: "1fr 1fr", gap: 20 }}>

        {/* Bar chart */}
        <div style={{ background: "#1e293b", border: "1px solid #334155",
                      borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, color: "#94a3b8",
                        marginBottom: 16 }}>Incidents by Plant</div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={plantBar}>
              <XAxis dataKey="name" tick={{ fill: "#64748b", fontSize: 12 }}
                     axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#64748b", fontSize: 12 }}
                     axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ background: "#0f172a",
                                border: "1px solid #334155",
                                borderRadius: 8, color: "#e2e8f0" }}
              />
              <Bar dataKey="incidents" fill="#f97316"
                   radius={[4,4,0,0]} name="Incidents" />
              <Bar dataKey="assets"    fill="#38bdf8"
                   radius={[4,4,0,0]} name="Assets" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Pie chart */}
        <div style={{ background: "#1e293b", border: "1px solid #334155",
                      borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, color: "#94a3b8",
                        marginBottom: 16 }}>Incident Severity Distribution</div>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={sevCounts} dataKey="value" nameKey="name"
                   cx="50%" cy="50%" outerRadius={80} label={
                     ({ name, value }) => `${name}: ${value}`
                   }>
                {sevCounts.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ background: "#0f172a",
                                border: "1px solid #334155",
                                borderRadius: 8, color: "#e2e8f0" }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Graph entity counts */}
      <div style={{ background: "#1e293b", border: "1px solid #334155",
                    borderRadius: 12, padding: 20 }}>
        <div style={{ fontSize: 14, fontWeight: 600, color: "#94a3b8",
                      marginBottom: 16 }}>Knowledge Graph Node Inventory</div>
        <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
          {stats.map(s => (
            <div key={s.label} style={{ textAlign: "center" }}>
              <div style={{ fontSize: 22, fontWeight: 700,
                            color: "#38bdf8" }}>{s.count}</div>
              <div style={{ fontSize: 12, color: "#64748b" }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* High risk table */}
      {riskAssets.length > 0 && (
        <div style={{ background: "#1e293b", border: "1px solid #ef444433",
                      borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 14, fontWeight: 600, color: "#ef4444",
                        marginBottom: 16 }}>
            ⚠ High Risk Assets — Immediate Attention Required
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse",
                          fontSize: 13 }}>
            <thead>
              <tr style={{ color: "#64748b", textAlign: "left" }}>
                {["Asset","Type","Plant","Open Incidents"].map(h => (
                  <th key={h} style={{ padding: "6px 12px",
                                       borderBottom: "1px solid #334155" }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {riskAssets.map(a => (
                <tr key={a.asset_id}
                    style={{ borderBottom: "1px solid #1e293b" }}>
                  <td style={{ padding: "10px 12px",
                                color: "#f1f5f9" }}>{a.asset_name}</td>
                  <td style={{ padding: "10px 12px",
                                color: "#94a3b8" }}>{a.asset_type}</td>
                  <td style={{ padding: "10px 12px",
                                color: "#94a3b8" }}>{a.plant_name}</td>
                  <td style={{ padding: "10px 12px" }}>
                    <span style={{ color: "#ef4444", fontWeight: 700 }}>
                      {a.open_incident_count}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}