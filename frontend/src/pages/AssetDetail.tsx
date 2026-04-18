import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchAssetById } from "../api/client";
import SeverityBadge from "../components/SeverityBadge";
import StatusBadge from "../components/StatusBadge";
import type { Asset } from "../types";

export default function AssetDetail() {
  const { id }        = useParams<{ id: string }>();
  const navigate      = useNavigate();
  const [asset, setAsset] = useState<Asset | null>(null);

  useEffect(() => {
    if (id) fetchAssetById(id).then(r => setAsset(r.data));
  }, [id]);

  if (!asset) return (
    <div style={{ color: "#64748b" }}>Loading asset...</div>
  );

  const sectionStyle = {
    background: "#1e293b", border: "1px solid #334155",
    borderRadius: 12, padding: 20
  };

  const labelStyle = { color: "#475569", fontSize: 13, minWidth: 140 };
  const valueStyle = { color: "#94a3b8", fontSize: 13 };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>

      {/* Back */}
      <button onClick={() => navigate("/assets")}
        style={{ background: "none", border: "none", color: "#38bdf8",
                 cursor: "pointer", fontSize: 13, textAlign: "left",
                 padding: 0, width: "fit-content" }}>
        ← Back to Assets
      </button>

      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between",
                    alignItems: "center" }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 700,
                       color: "#f1f5f9", margin: 0 }}>{asset.name}</h1>
          <div style={{ color: "#64748b", fontSize: 14,
                        marginTop: 4 }}>{asset.id}</div>
        </div>
        <StatusBadge status={asset.status} />
      </div>

      {/* Core info */}
      <div style={sectionStyle}>
        <div style={{ fontSize: 13, fontWeight: 600, color: "#64748b",
                      marginBottom: 14, textTransform: "uppercase",
                      letterSpacing: "0.08em" }}>Asset Information</div>
        <div style={{ display: "grid",
                      gridTemplateColumns: "1fr 1fr", gap: "10px 24px" }}>
          {[
            ["Type", asset.type],
            ["Manufacturer", asset.manufacturer],
            ["Installed", asset.install_year?.toString()],
            ["Plant", asset.plant_name],
            ["System", asset.system_name],
          ].map(([l, v]) => (
            <div key={l} style={{ display: "flex", gap: 12 }}>
              <span style={labelStyle}>{l}</span>
              <span style={valueStyle}>{v}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Sensors */}
      {asset.sensors && asset.sensors.length > 0 && (
        <div style={sectionStyle}>
          <div style={{ fontSize: 13, fontWeight: 600, color: "#64748b",
                        marginBottom: 14, textTransform: "uppercase",
                        letterSpacing: "0.08em" }}>
            Sensors ({asset.sensors.length})
          </div>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            {asset.sensors.map(s => (
              <div key={s.id} style={{
                background: "#0f172a", border: "1px solid #334155",
                borderRadius: 8, padding: "8px 14px"
              }}>
                <div style={{ fontSize: 13, color: "#38bdf8",
                              fontWeight: 600 }}>{s.name}</div>
                <div style={{ fontSize: 11, color: "#475569",
                              marginTop: 2 }}>
                  {s.type} · {s.unit}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Incidents */}
      {asset.incidents && asset.incidents.length > 0 && (
        <div style={sectionStyle}>
          <div style={{ fontSize: 13, fontWeight: 600, color: "#64748b",
                        marginBottom: 14, textTransform: "uppercase",
                        letterSpacing: "0.08em" }}>
            Incident History ({asset.incidents.length})
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {asset.incidents
              .filter(i => i.title)
              .map(inc => (
              <div key={inc.id} style={{
                background: "#0f172a", borderRadius: 8, padding: 14,
                border: "1px solid #334155"
              }}>
                <div style={{ display: "flex",
                              justifyContent: "space-between",
                              alignItems: "center", marginBottom: 6 }}>
                  <div style={{ fontSize: 14, fontWeight: 600,
                                color: "#f1f5f9" }}>{inc.title}</div>
                  <div style={{ display: "flex", gap: 8 }}>
                    <SeverityBadge severity={inc.severity} />
                    <StatusBadge status={inc.status} />
                  </div>
                </div>
                <div style={{ fontSize: 12, color: "#475569" }}>
                  {inc.date}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Maintenance */}
      {asset.maintenance_history &&
       asset.maintenance_history.length > 0 && (
        <div style={sectionStyle}>
          <div style={{ fontSize: 13, fontWeight: 600, color: "#64748b",
                        marginBottom: 14, textTransform: "uppercase",
                        letterSpacing: "0.08em" }}>
            Maintenance History
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {asset.maintenance_history
              .filter(m => m.type)
              .map((m, i) => (
              <div key={i} style={{
                background: "#0f172a", borderRadius: 8, padding: 14,
                border: "1px solid #334155"
              }}>
                <div style={{ display: "flex",
                              justifyContent: "space-between",
                              marginBottom: 6 }}>
                  <span style={{ color: "#a78bfa", fontWeight: 600,
                                 fontSize: 13 }}>{m.type}</span>
                  <span style={{ color: "#64748b", fontSize: 12 }}>
                    {m.date}
                  </span>
                </div>
                <div style={{ fontSize: 13, color: "#94a3b8" }}>
                  {m.description}
                </div>
                {m.cost_usd > 0 && (
                  <div style={{ fontSize: 12, color: "#475569",
                                marginTop: 6 }}>
                    Cost: ${m.cost_usd?.toLocaleString()}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}