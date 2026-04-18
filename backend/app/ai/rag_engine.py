import os
from app.graph.neo4j_client import neo4j_client
from app.graph.queries import (
    GET_ASSET_FULL_CONTEXT_FOR_RAG,
    GET_ALL_INCIDENTS,
    GET_HIGH_RISK_ASSETS
)
from app.ai.llm_client import ask_llm

# Read this from .env — defaults to false so backend works without Docker
OPENSEARCH_ENABLED = os.getenv("OPENSEARCH_ENABLED", "false").lower() == "true"

SYSTEM_PROMPT = """
You are an Industrial Asset Intelligence Assistant for an Oil & Gas company.
You have access to a knowledge graph of industrial assets, sensors, incidents,
and maintenance history across offshore and onshore facilities.

CRITICAL RULES:
1. Only answer based on the CONTEXT provided below.
2. If the answer is not in the context, say "I don't have that information in the knowledge graph."
3. Always cite which asset, incident ID, or plant name you are referring to.
4. Be concise and precise — this is safety-critical industrial data.
5. When mentioning severity levels, always flag 'critical' issues prominently.

You are NOT a general AI. You are a domain-specific knowledge system grounded
in structured graph data.
"""


def build_graph_context() -> str:
    """
    Module 2 mode — pulls full graph context directly from Neo4j.
    Used when OPENSEARCH_ENABLED=false in .env
    """
    assets_data    = neo4j_client.run_query(GET_ASSET_FULL_CONTEXT_FOR_RAG)
    risk_data      = neo4j_client.run_query(GET_HIGH_RISK_ASSETS)

    context_parts = []

    context_parts.append("=== ASSET KNOWLEDGE BASE ===")
    for asset in assets_data:
        asset_text = (
            f"\nAsset: {asset['asset_name']} (ID: {asset['asset_id']})\n"
            f"  Type: {asset['asset_type']} | Manufacturer: {asset['manufacturer']} "
            f"| Installed: {asset['install_year']}\n"
            f"  Status: {asset['asset_status']} | Plant: {asset['plant_name']} "
            f"({asset['location']})\n"
            f"  System: {asset['system_name']}\n"
            f"  Sensors: {', '.join(asset['sensors']) if asset['sensors'] else 'None'}"
        )

        if asset['incidents'] and asset['incidents'][0].get('title'):
            asset_text += "\n  Incident History:"
            for inc in asset['incidents']:
                if inc.get('title'):
                    asset_text += (
                        f"\n    - [{inc['severity'].upper()}] {inc['title']} "
                        f"on {inc['date']} | Status: {inc['status']}\n"
                        f"      Failure Mode: {inc.get('failure_mode', 'Unknown')}\n"
                        f"      Description: {inc.get('description', '')}"
                    )

        if asset['maintenance'] and asset['maintenance'][0].get('type'):
            asset_text += "\n  Maintenance History:"
            for maint in asset['maintenance']:
                if maint.get('type'):
                    asset_text += (
                        f"\n    - [{maint['type']}] on {maint['date']} "
                        f"| Cost: ${maint.get('cost_usd', 0):,}\n"
                        f"      Work Done: {maint.get('description', '')}"
                    )

        context_parts.append(asset_text)

    context_parts.append("\n=== CURRENT HIGH RISK ASSETS ===")
    for risk in risk_data:
        context_parts.append(
            f"HIGH RISK: {risk['asset_name']} at {risk['plant_name']} — "
            f"{risk['open_incident_count']} open critical/high incident(s)"
        )

    return "\n".join(context_parts)


def build_targeted_context(user_question: str) -> dict:
    """
    Module 3 mode — uses OpenSearch semantic search.
    Only called when OPENSEARCH_ENABLED=true in .env
    """
    from app.search.search_engine import (
        semantic_search_incidents,
        semantic_search_assets
    )

    relevant_incidents = semantic_search_incidents(user_question, top_k=5)
    relevant_assets    = semantic_search_assets(user_question, top_k=3)
    risk_data          = neo4j_client.run_query(GET_HIGH_RISK_ASSETS)

    context_parts = []

    context_parts.append("=== MOST RELEVANT INCIDENTS (retrieved by semantic search) ===")
    for inc in relevant_incidents:
        context_parts.append(
            f"\nIncident: {inc.get('title')} (ID: {inc.get('incident_id')})\n"
            f"  Asset: {inc.get('asset_name')} ({inc.get('asset_type')}) "
            f"at {inc.get('plant_name')}\n"
            f"  Severity: {inc.get('severity')} | Status: {inc.get('status')} "
            f"| Date: {inc.get('date')}\n"
            f"  Failure Mode: {inc.get('failure_mode', 'Unknown')}\n"
            f"  Description: {inc.get('description')}\n"
            f"  Relevance Score: {inc.get('_score', 0):.4f}"
        )

    context_parts.append("\n=== MOST RELEVANT ASSETS ===")
    for asset in relevant_assets:
        context_parts.append(
            f"\nAsset: {asset.get('asset_name')} (ID: {asset.get('asset_id')})\n"
            f"  Type: {asset.get('asset_type')} | Status: {asset.get('status')}\n"
            f"  Plant: {asset.get('plant_name')} | System: {asset.get('system_name')}\n"
            f"  Manufacturer: {asset.get('manufacturer')} "
            f"| Installed: {asset.get('install_year')}"
        )

    context_parts.append("\n=== CURRENT HIGH RISK ASSETS ===")
    for risk in risk_data:
        context_parts.append(
            f"RISK: {risk['asset_name']} at {risk['plant_name']} — "
            f"{risk['open_incident_count']} open critical/high incident(s)"
        )

    return {
        "context_text":              "\n".join(context_parts),
        "retrieved_incident_count":  len(relevant_incidents),
        "retrieved_asset_count":     len(relevant_assets)
    }


def answer_question(user_question: str) -> dict:
    if OPENSEARCH_ENABLED:
        retrieval_result = build_targeted_context(user_question)
        context          = retrieval_result["context_text"]
        retrieval_stats  = {
            "incidents_retrieved": retrieval_result["retrieved_incident_count"],
            "assets_retrieved":    retrieval_result["retrieved_asset_count"],
            "retrieval_method":    "semantic vector search (cosine similarity)"
        }
        grounded_in = "Neo4j Knowledge Graph + OpenSearch Vector Index"
    else:
        context         = build_graph_context()
        retrieval_stats = {
            "incidents_retrieved": "all",
            "assets_retrieved":    "all",
            "retrieval_method":    "full graph context from Neo4j"
        }
        grounded_in = "Neo4j Knowledge Graph"

    full_system_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"=== KNOWLEDGE GRAPH CONTEXT ===\n"
        f"{context}\n"
        f"=== END OF CONTEXT ===\n\n"
        f"Answer the following question using ONLY the context above:"
    )

    answer = ask_llm(
        system_prompt=full_system_prompt,
        user_message=user_question
    )

    return {
        "question":            user_question,
        "answer":              answer,
        "retrieval_stats":     retrieval_stats,
        "grounded_in":         grounded_in,
        "explainability_note": (
            "Answer generated from structured graph data only. "
            "No external knowledge used. All facts traceable to graph entities."
        )
    }