import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchAssets } from "../api/client";
import StatusBadge from "../components/StatusBadge";
import type { Asset } from "../types";

const STATUS_OPTIONS = ["","operational","degraded","under_maintenance"];
const TYPE_OPTIONS   = ["","Compressor","HeatExchanger","Pipeline","Column"];

export default function Assets() {
  const [assets, setAssets]   = useState<Asset[]>([]);
  const [status, setStatus]   = useState("");
  const [type, setType]       = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    fetchAssets({
      status: status || undefined,
      asset_type: type || undefined
    }).then(r => {
      setAssets(r.data.assets);
      setLoading(false);
    });
  }, [status, type]);

  const selectStyle = {
    background: "#1e293b", color: "#94a3b8",
    border: "1px solid #334155", borderRadius: 8,
    padding: "8px 14px", fontSize: 13, cursor: "pointer"
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>

      <div style={{ display: "flex", justifyContent: "space-between",
                    alignItems: "flex-end" }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 700,
                       color: "#f1f5f9", margin: 0 }}>Asset Registry</h1>
          <p style={{ color: "#64748b", marginTop: 4, fontSize: 14 }}>
            {assets.length} assets across all plants
          </p>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <select value={status} onChange={e => setStatus(e.target.value)}
                  style={selectStyle}>
            {STATUS_OPTIONS.map(s => (
              <option key={s} value={s}>{s || "All Statuses"}</option>
            ))}
          </select>
          <select value={type} onChange={e => setType(e.target.value)}
                  style={selectStyle}>
            {TYPE_OPTIONS.map(t => (
              <option key={t} value={t}>{t || "All Types"}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div style={{ color: "#64748b" }}>Loading assets...</div>
      ) : (
        <div style={{ display: "grid",
                      gridTemplateColumns: "repeat(auto-fill, minmax(280px,1fr))",
                      gap: 16 }}>
          {assets.map(asset => (
            <div key={asset.id}
              onClick={() => navigate(`/assets/${asset.id}`)}
              style={{
                background: "#1e293b", border: "1px solid #334155",
                borderRadius: 12, padding: 20, cursor: "pointer",
                transition: "border-color 0.15s"
              }}
              onMouseEnter={e =>
                (e.currentTarget.style.borderColor = "#38bdf8")}
              onMouseLeave={e =>
                (e.currentTarget.style.borderColor = "#334155")}
            >
              <div style={{ display: "flex", justifyContent: "space-between",
                            alignItems: "flex-start", marginBottom: 12 }}>
                <div style={{ fontSize: 15, fontWeight: 600,
                              color: "#f1f5f9" }}>{asset.name}</div>
                <StatusBadge status={asset.status} />
              </div>
              <div style={{ display: "flex", flexDirection: "column",
                            gap: 4 }}>
                {[
                  ["Type", asset.type],
                  ["Plant", asset.plant_name],
                  ["System", asset.system_name],
                  ["Manufacturer", asset.manufacturer],
                  ["Installed", asset.install_year?.toString()]
                ].map(([label, val]) => (
                  <div key={label} style={{ display: "flex", gap: 8,
                                            fontSize: 13 }}>
                    <span style={{ color: "#475569", minWidth: 90 }}>
                      {label}
                    </span>
                    <span style={{ color: "#94a3b8" }}>{val}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}