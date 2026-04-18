import { useEffect, useState } from "react";
import { fetchIncidents, searchIncidents } from "../api/client";
import SeverityBadge from "../components/SeverityBadge";
import StatusBadge from "../components/StatusBadge";
import type { Incident } from "../types";

export default function Incidents() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [severity, setSeverity]   = useState("");
  const [searchQ, setSearchQ]     = useState("");
  const [searchMode, setMode]     = useState<"semantic"|"keyword">("semantic");
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    if (searchQ.trim().length > 2) {
      setLoading(true);
      searchIncidents(searchQ, searchMode,
                      severity || undefined).then(r => {
        setIncidents(r.data.results);
        setLoading(false);
      });
    } else {
      setLoading(true);
      fetchIncidents({ severity: severity || undefined }).then(r => {
        setIncidents(r.data.incidents);
        setLoading(false);
      });
    }
  }, [severity, searchQ, searchMode]);

  const inputStyle = {
    background: "#1e293b", color: "#e2e8f0",
    border: "1px solid #334155", borderRadius: 8,
    padding: "9px 14px", fontSize: 13, outline: "none"
  };

  const selectStyle = { ...inputStyle, cursor: "pointer" };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>

      <div>
        <h1 style={{ fontSize: 22, fontWeight: 700,
                     color: "#f1f5f9", margin: 0 }}>Incident Log</h1>
        <p style={{ color: "#64748b", marginTop: 4, fontSize: 14 }}>
          {incidents.length} incidents — semantic & keyword search enabled
        </p>
      </div>

      {/* Search bar */}
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        <input
          value={searchQ}
          onChange={e => setSearchQ(e.target.value)}
          placeholder="Search incidents semantically..."
          style={{ ...inputStyle, flex: 1, minWidth: 240 }}
        />
        <select value={searchMode}
                onChange={e => setMode(e.target.value as any)}
                style={selectStyle}>
          <option value="semantic">Semantic Search</option>
          <option value="keyword">Keyword Search</option>
        </select>
        <select value={severity}
                onChange={e => setSeverity(e.target.value)}
                style={selectStyle}>
          {["","critical","high","medium","low"].map(s => (
            <option key={s} value={s}>{s || "All Severities"}</option>
          ))}
        </select>
      </div>

      {/* Table */}
      {loading ? (
        <div style={{ color: "#64748b" }}>Loading incidents...</div>
      ) : (
        <div style={{ background: "#1e293b", border: "1px solid #334155",
                      borderRadius: 12, overflow: "hidden" }}>
          <table style={{ width: "100%", borderCollapse: "collapse",
                          fontSize: 13 }}>
            <thead>
              <tr style={{ background: "#0f172a" }}>
                {["Date","Title","Asset","Plant",
                  "Failure Mode","Severity","Status"].map(h => (
                  <th key={h} style={{
                    padding: "12px 16px", textAlign: "left",
                    color: "#475569", fontWeight: 600,
                    borderBottom: "1px solid #334155"
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {incidents.map(inc => (
                <tr key={inc.id}
                    style={{ borderBottom: "1px solid #1e293b" }}
                    onMouseEnter={e =>
                      (e.currentTarget.style.background = "#0f172a")}
                    onMouseLeave={e =>
                      (e.currentTarget.style.background = "transparent")}
                >
                  <td style={{ padding: "12px 16px",
                                color: "#475569" }}>{inc.date}</td>
                  <td style={{ padding: "12px 16px",
                                color: "#f1f5f9",
                                fontWeight: 500 }}>{inc.title}</td>
                  <td style={{ padding: "12px 16px",
                                color: "#94a3b8" }}>{inc.asset_name}</td>
                  <td style={{ padding: "12px 16px",
                                color: "#94a3b8" }}>{inc.plant_name}</td>
                  <td style={{ padding: "12px 16px",
                                color: "#64748b" }}>{inc.failure_mode}</td>
                  <td style={{ padding: "12px 16px" }}>
                    <SeverityBadge severity={inc.severity} />
                  </td>
                  <td style={{ padding: "12px 16px" }}>
                    <StatusBadge status={inc.status} />
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