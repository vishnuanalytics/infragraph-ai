import { NavLink, Outlet } from "react-router-dom";
import {
  LayoutDashboard, Server, AlertTriangle,
  MessageSquare, Network
} from "lucide-react";

const nav = [
  { to: "/",         label: "Dashboard",  icon: LayoutDashboard },
  { to: "/assets",   label: "Assets",     icon: Server },
  { to: "/incidents",label: "Incidents",  icon: AlertTriangle },
  { to: "/ai",       label: "AI Q&A",     icon: MessageSquare },
];

export default function Layout() {
  return (
    <div style={{ display: "flex", minHeight: "100vh",
                  background: "#0f172a", color: "#e2e8f0" }}>

      {/* Sidebar */}
      <aside style={{
        width: 220, background: "#1e293b",
        padding: "24px 16px", display: "flex",
        flexDirection: "column", gap: 8,
        borderRight: "1px solid #334155"
      }}>
        {/* Logo */}
        <div style={{ display: "flex", alignItems: "center",
                      gap: 10, marginBottom: 32 }}>
          <Network size={26} color="#38bdf8" />
          <div>
            <div style={{ fontWeight: 700, fontSize: 15,
                          color: "#f1f5f9" }}>InfraGraph</div>
            <div style={{ fontSize: 11, color: "#64748b" }}>AI Platform</div>
          </div>
        </div>

        {nav.map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} end={to === "/"}
            style={({ isActive }) => ({
              display: "flex", alignItems: "center", gap: 10,
              padding: "10px 12px", borderRadius: 8,
              textDecoration: "none", fontSize: 14, fontWeight: 500,
              background: isActive ? "#0f172a" : "transparent",
              color: isActive ? "#38bdf8" : "#94a3b8",
              borderLeft: isActive ? "3px solid #38bdf8"
                                   : "3px solid transparent",
              transition: "all 0.15s"
            })}>
            <Icon size={17} />
            {label}
          </NavLink>
        ))}

        <div style={{ marginTop: "auto", fontSize: 11,
                      color: "#475569", paddingTop: 16,
                      borderTop: "1px solid #334155" }}>
          <div>Neo4j + OpenSearch</div>
          <div>Llama 3 via Groq</div>
        </div>
      </aside>

      {/* Main */}
      <main style={{ flex: 1, padding: 32, overflowY: "auto" }}>
        <Outlet />
      </main>
    </div>
  );
}