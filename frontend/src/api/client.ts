import axios from "axios";
import type {
  Asset, Incident, PlantSummary,
  AIResponse, SearchResult, GraphStats
} from "../types";

const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: BASE });

// Assets
export const fetchAssets = (params?: {
  status?: string;
  asset_type?: string;
}) => api.get<{ count: number; assets: Asset[] }>("/api/assets/", { params });

export const fetchAssetById = (id: string) =>
  api.get<Asset>(`/api/assets/${id}`);

export const fetchHighRiskAssets = () =>
  api.get<{ count: number; high_risk_assets: any[] }>("/api/assets/high-risk");

export const fetchSharedFailures = () =>
  api.get("/api/assets/shared-failures");

// Incidents
export const fetchIncidents = (params?: {
  severity?: string;
  start_date?: string;
  end_date?: string;
}) => api.get<{ count: number; incidents: Incident[] }>
  ("/api/incidents/", { params });

// Plants
export const fetchPlantSummary = () =>
  api.get<{ plants: PlantSummary[] }>("/api/plants/summary");

export const fetchGraphStats = () =>
  api.get<GraphStats>("/api/plants/stats");

// Search
export const searchIncidents = (
  q: string,
  mode: "semantic" | "keyword" = "semantic",
  severity?: string
) =>
  api.get<SearchResult>("/api/search/incidents", {
    params: { q, mode, severity }
  });

// AI
export const askAI = (question: string) =>
  api.post<AIResponse>("/api/ai/ask", { question });

export const fetchSampleQuestions = () =>
  api.get<{ questions: string[] }>("/api/ai/sample-questions");