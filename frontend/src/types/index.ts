export interface Asset {
  id: string;
  name: string;
  type: string;
  manufacturer: string;
  install_year: number;
  status: "operational" | "degraded" | "under_maintenance";
  system_name: string;
  plant_name: string;
  sensors?: Sensor[];
  incidents?: Incident[];
  maintenance_history?: MaintenanceEvent[];
}

export interface Incident {
  id: string;
  title: string;
  date: string;
  severity: "critical" | "high" | "medium" | "low";
  status: "open" | "resolved" | "in_progress";
  description: string;
  asset_id?: string;
  asset_name?: string;
  asset_type?: string;
  failure_mode?: string;
  plant_name?: string;
}

export interface Sensor {
  id: string;
  name: string;
  type: string;
  unit: string;
}

export interface MaintenanceEvent {
  id: string;
  type: string;
  date: string;
  description: string;
  cost_usd: number;
  technician?: string;
}

export interface PlantSummary {
  plant_id: string;
  plant_name: string;
  location: string;
  plant_type: string;
  total_systems: number;
  total_assets: number;
  total_incidents: number;
  total_maintenance_events: number;
  total_maintenance_cost_usd: number;
}

export interface AIResponse {
  question: string;
  answer: string;
  retrieval_stats: {
    incidents_retrieved: number;
    assets_retrieved: number;
    retrieval_method: string;
  };
  grounded_in: string;
  explainability_note: string;
}

export interface SearchResult {
  query: string;
  mode: string;
  count: number;
  results: Incident[];
}

export interface GraphStats {
  graph_statistics: { label: string; count: number }[];
}