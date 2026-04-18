from app.search.opensearch_client import (
    opensearch_client,
    INCIDENT_INDEX,
    ASSET_INDEX
)
from app.ai.embedder import embed_text

def semantic_search_incidents(
    query: str,
    top_k: int = 5,
    severity_filter: str = None,
    status_filter: str = None
) -> list[dict]:
    """
    Hybrid search: semantic vector similarity + optional keyword filters.
    This is what you call 'search schema tuning' in the JD.
    """
    query_vector = embed_text(query)

    # Build filter clause if filters provided
    filters = []
    if severity_filter:
        filters.append({"term": {"severity": severity_filter}})
    if status_filter:
        filters.append({"term": {"status": status_filter}})

    if filters:
        # Filtered semantic search — vector search within filtered subset
        search_body = {
            "size": top_k,
            "query": {
                "bool": {
                    "must": [
                        {
                            "knn": {
                                "embedding": {
                                    "vector": query_vector,
                                    "k": top_k
                                }
                            }
                        }
                    ],
                    "filter": filters
                }
            },
            "_source": {
                "excludes": ["embedding"]  # Don't return raw vectors to client
            }
        }
    else:
        # Pure semantic search
        search_body = {
            "size": top_k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_vector,
                        "k": top_k
                    }
                }
            },
            "_source": {
                "excludes": ["embedding"]
            }
        }

    response = opensearch_client.search(
        index=INCIDENT_INDEX,
        body=search_body
    )

    results = []
    for hit in response["hits"]["hits"]:
        result = hit["_source"]
        result["_score"] = hit["_score"]   # Similarity score
        result["_id"] = hit["_id"]
        results.append(result)

    return results


def semantic_search_assets(query: str, top_k: int = 5) -> list[dict]:
    query_vector = embed_text(query)

    search_body = {
        "size": top_k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_vector,
                    "k": top_k
                }
            }
        },
        "_source": {
            "excludes": ["embedding"]
        }
    }

    response = opensearch_client.search(
        index=ASSET_INDEX,
        body=search_body
    )

    results = []
    for hit in response["hits"]["hits"]:
        result = hit["_source"]
        result["_score"] = hit["_score"]
        results.append(result)

    return results


def keyword_search_incidents(query: str, top_k: int = 5) -> list[dict]:
    """
    BM25 keyword search — complement to semantic search.
    In production you combine both scores (hybrid search).
    """
    search_body = {
        "size": top_k,
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "title^3",          # Boost title matches 3x
                    "description^2",    # Boost description 2x
                    "failure_mode",
                    "asset_name",
                    "searchable_text"
                ],
                "type": "best_fields",
                "fuzziness": "AUTO"     # Handles typos automatically
            }
        },
        "_source": {
            "excludes": ["embedding"]
        }
    }

    response = opensearch_client.search(
        index=INCIDENT_INDEX,
        body=search_body
    )

    return [
        {**hit["_source"], "_score": hit["_score"]}
        for hit in response["hits"]["hits"]
    ]