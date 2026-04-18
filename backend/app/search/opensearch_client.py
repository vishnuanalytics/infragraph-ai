from opensearchpy import OpenSearch
from dotenv import load_dotenv
import os

load_dotenv()

# ============================================================
# INDEX SCHEMAS — this is what you explain as "index mapping
# strategy" to the interviewer. Each field is intentional.
# ============================================================

INCIDENT_INDEX = "infragraph_incidents"
ASSET_INDEX = "infragraph_assets"
MAINTENANCE_INDEX = "infragraph_maintenance"

# Incident index: text fields for search + vector field for semantic search
INCIDENT_INDEX_MAPPING = {
    "settings": {
        "index": {
            "knn": True,                    # Enable k-NN vector search
            "knn.algo_param.ef_search": 100 # Controls recall vs speed
        }
    },
    "mappings": {
        "properties": {
            # Structured fields — for exact/filtered queries
            "incident_id":    {"type": "keyword"},
            "asset_id":       {"type": "keyword"},
            "asset_name":     {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "asset_type":     {"type": "keyword"},
            "plant_name":     {"type": "keyword"},
            "severity":       {"type": "keyword"},
            "status":         {"type": "keyword"},
            "failure_mode":   {"type": "keyword"},
            "date":           {"type": "date", "format": "yyyy-MM-dd"},

            # Full-text searchable description
            "title":          {"type": "text", "analyzer": "english"},
            "description":    {"type": "text", "analyzer": "english"},

            # Combined text for embedding — this is what we vectorize
            "searchable_text": {"type": "text", "analyzer": "english"},

            # Vector field — 384 dims matches all-MiniLM-L6-v2
            "embedding": {
                "type": "knn_vector",
                "dimension": 384,
                "method": {
                    "name": "hnsw",         # Hierarchical Navigable Small World graph
                    "space_type": "cosinesimil",  # Cosine similarity for normalized vectors
                    "engine": "nmslib",
                    "parameters": {
                        "ef_construction": 128,
                        "m": 24
                    }
                }
            }
        }
    }
}

ASSET_INDEX_MAPPING = {
    "settings": {
        "index": {
            "knn": True,
            "knn.algo_param.ef_search": 100
        }
    },
    "mappings": {
        "properties": {
            "asset_id":       {"type": "keyword"},
            "asset_name":     {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "asset_type":     {"type": "keyword"},
            "manufacturer":   {"type": "keyword"},
            "plant_name":     {"type": "keyword"},
            "system_name":    {"type": "keyword"},
            "status":         {"type": "keyword"},
            "install_year":   {"type": "integer"},
            "searchable_text": {"type": "text", "analyzer": "english"},
            "embedding": {
                "type": "knn_vector",
                "dimension": 384,
                "method": {
                    "name": "hnsw",
                    "space_type": "cosinesimil",
                    "engine": "nmslib",
                    "parameters": {
                        "ef_construction": 128,
                        "m": 24
                    }
                }
            }
        }
    }
}

def get_opensearch_client() -> OpenSearch:
    return OpenSearch(
        hosts=[{
            "host": os.getenv("OPENSEARCH_HOST", "localhost"),
            "port": int(os.getenv("OPENSEARCH_PORT", 9200))
        }],
        http_compress=True,
        use_ssl=False,
        verify_certs=False
    )

opensearch_client = get_opensearch_client()