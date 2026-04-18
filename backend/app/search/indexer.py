from app.graph.neo4j_client import neo4j_client
from app.graph.queries import GET_ALL_INCIDENTS, GET_ASSET_FULL_CONTEXT_FOR_RAG
from app.ai.embedder import embed_batch
from app.search.opensearch_client import (
    opensearch_client,
    INCIDENT_INDEX,
    ASSET_INDEX
)
from app.search.index_manager import create_all_indexes

def build_incident_searchable_text(incident: dict) -> str:
    """
    Combine all relevant fields into one string for embedding.
    The quality of this text directly affects search quality.
    This is a deliberate design decision you explain to the interviewer.
    """
    parts = [
        f"Incident: {incident.get('title', '')}",
        f"Asset: {incident.get('asset_name', '')} (type: {incident.get('asset_type', '')})",
        f"Plant: {incident.get('plant_name', '')}",
        f"Severity: {incident.get('severity', '')}",
        f"Failure mode: {incident.get('failure_mode', '')}",
        f"Status: {incident.get('status', '')}",
        f"Description: {incident.get('description', '')}",
        f"Date: {incident.get('date', '')}"
    ]
    return " | ".join(parts)

def build_asset_searchable_text(asset: dict) -> str:
    sensors_text = ", ".join(asset.get("sensors", [])) if asset.get("sensors") else "none"

    incident_texts = []
    for inc in asset.get("incidents", []):
        if inc.get("title"):
            incident_texts.append(
                f"{inc['title']} ({inc['severity']}) caused by {inc.get('failure_mode', 'unknown')}"
            )

    parts = [
        f"Asset: {asset.get('asset_name', '')} type {asset.get('asset_type', '')}",
        f"Manufacturer: {asset.get('manufacturer', '')}",
        f"Plant: {asset.get('plant_name', '')} location {asset.get('location', '')}",
        f"System: {asset.get('system_name', '')}",
        f"Status: {asset.get('asset_status', '')}",
        f"Installed: {asset.get('install_year', '')}",
        f"Sensors: {sensors_text}",
        f"Incidents: {'; '.join(incident_texts) if incident_texts else 'none'}"
    ]
    return " | ".join(parts)

def index_incidents():
    print("Fetching incidents from Neo4j...")
    incidents = neo4j_client.run_query(GET_ALL_INCIDENTS)
    print(f"Found {len(incidents)} incidents to index.")

    # Build searchable texts for all incidents
    texts = [build_incident_searchable_text(i) for i in incidents]

    # Embed all in one batch call — efficient
    print("Generating embeddings...")
    embeddings = embed_batch(texts)

    # Bulk index into OpenSearch
    print("Indexing into OpenSearch...")
    bulk_body = []
    for incident, text, embedding in zip(incidents, texts, embeddings):
        # Action line
        bulk_body.append({
            "index": {
                "_index": INCIDENT_INDEX,
                "_id": incident["id"]
            }
        })
        # Document line
        bulk_body.append({
            "incident_id":     incident.get("id"),
            "asset_id":        incident.get("asset_id"),
            "asset_name":      incident.get("asset_name"),
            "asset_type":      incident.get("asset_type"),
            "plant_name":      incident.get("plant_name"),
            "severity":        incident.get("severity"),
            "status":          incident.get("status"),
            "failure_mode":    incident.get("failure_mode"),
            "date":            incident.get("date"),
            "title":           incident.get("title"),
            "description":     incident.get("description"),
            "searchable_text": text,
            "embedding":       embedding
        })

    response = opensearch_client.bulk(body=bulk_body)
    errors = [i for i in response["items"] if "error" in i.get("index", {})]
    print(f"Indexed {len(incidents) - len(errors)} incidents. Errors: {len(errors)}")

def index_assets():
    print("Fetching assets from Neo4j...")
    assets = neo4j_client.run_query(GET_ASSET_FULL_CONTEXT_FOR_RAG)
    print(f"Found {len(assets)} assets to index.")

    texts = [build_asset_searchable_text(a) for a in assets]

    print("Generating embeddings...")
    embeddings = embed_batch(texts)

    print("Indexing into OpenSearch...")
    bulk_body = []
    for asset, text, embedding in zip(assets, texts, embeddings):
        bulk_body.append({
            "index": {
                "_index": ASSET_INDEX,
                "_id": asset["asset_id"]
            }
        })
        bulk_body.append({
            "asset_id":        asset.get("asset_id"),
            "asset_name":      asset.get("asset_name"),
            "asset_type":      asset.get("asset_type"),
            "manufacturer":    asset.get("manufacturer"),
            "plant_name":      asset.get("plant_name"),
            "system_name":     asset.get("system_name"),
            "status":          asset.get("asset_status"),
            "install_year":    asset.get("install_year"),
            "searchable_text": text,
            "embedding":       embedding
        })

    response = opensearch_client.bulk(body=bulk_body)
    errors = [i for i in response["items"] if "error" in i.get("index", {})]
    print(f"Indexed {len(assets) - len(errors)} assets. Errors: {len(errors)}")

def run_full_indexing(recreate: bool = False):
    print("=== InfraGraph OpenSearch Indexing Pipeline ===")
    create_all_indexes(recreate=recreate)
    index_incidents()
    index_assets()
    print("=== Indexing complete ===")

if __name__ == "__main__":
    run_full_indexing(recreate=True)