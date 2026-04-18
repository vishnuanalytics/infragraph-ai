# InfraGraph AI

An Industrial Asset Knowledge Graph platform with AI-powered Q&A for Oil & Gas operations.

## What This Project Does

Engineers can ask natural language questions like *"Which compressors had pressure failures in the last 6 months?"* and get accurate, explainable answers grounded in real graph data — not hallucinations.

## Tech Stack

| Layer | Technology |
|---|---|
| Knowledge Graph | Neo4j Aura + Cypher |
| Semantic Search | OpenSearch (vector knn) |
| AI / RAG | Llama 3.3 via Groq API |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Backend | FastAPI + Python |
| Frontend | React + TypeScript + Vite |
| Infrastructure | Docker Compose |

## Architecture

User Question
│
▼
React Frontend (TypeScript)
│
▼
FastAPI Backend (Python)
│
├── Neo4j (Knowledge Graph)
│     Plants → Systems → Assets → Sensors
│     Assets → Incidents → FailureModes
│     Assets → MaintenanceEvents
│
├── OpenSearch (Vector Index)
│     Semantic search on incidents + assets
│     384-dim embeddings via sentence-transformers
│
└── Groq LLM (Llama 3.3)
RAG — answers grounded in graph context only

## Knowledge Graph Ontology
(Plant)-[:HAS_SYSTEM]->(System)-[:CONTAINS]->(Asset)
(Asset)-[:HAS_SENSOR]->(Sensor)
(Asset)-[:INVOLVED_IN]->(Incident)-[:CAUSED_BY]->(FailureMode)
(Asset)-[:HAD_MAINTENANCE]->(MaintenanceEvent)

## Features

- Asset registry with status tracking across plants and systems
- Incident log with severity classification and failure mode linkage
- Multi-hop graph traversal — find assets sharing failure modes
- Semantic search on incidents using vector embeddings
- AI Q&A with full explainability — every answer cites graph sources
- Risk dashboard — identifies high risk assets with open critical incidents

## Local Setup

### Prerequisites
- Python 3.10+
- Node 18+
- Docker Desktop
- Neo4j Aura Free account
- Groq API key (free)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Fill in NEO4J_URI, NEO4J_PASSWORD, GROQ_API_KEY in .env
python -m app.graph.seed_data
uvicorn app.main:app --reload --port 8000
```

### OpenSearch (optional — for semantic search)

```bash
docker-compose up -d
python -m app.search.indexer
# Set OPENSEARCH_ENABLED=true in .env
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## API Endpoints
GET  /api/assets/                  All assets with filters
GET  /api/assets/high-risk         Assets with open critical incidents
GET  /api/assets/shared-failures   Assets sharing failure modes (graph traversal)
GET  /api/assets/{id}              Full asset detail with history
GET  /api/incidents/               Incident log with filters
GET  /api/plants/summary           Plant-level aggregation
GET  /api/search/incidents?q=...   Semantic search on incidents
POST /api/ai/ask                   AI Q&A grounded in knowledge graph