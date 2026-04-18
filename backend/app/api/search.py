from fastapi import APIRouter, Query
from app.search.search_engine import (
    semantic_search_incidents,
    semantic_search_assets,
    keyword_search_incidents
)
from app.search.index_manager import get_index_stats
from app.search.indexer import run_full_indexing
from typing import Optional

router = APIRouter()

@router.get("/incidents")
def search_incidents(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(5, description="Number of results"),
    severity: Optional[str] = Query(None, description="Filter: critical, high, medium"),
    status: Optional[str] = Query(None, description="Filter: open, resolved, in_progress"),
    mode: str = Query("semantic", description="Search mode: semantic or keyword")
):
    if mode == "keyword":
        results = keyword_search_incidents(q, top_k)
    else:
        results = semantic_search_incidents(q, top_k, severity, status)

    return {
        "query": q,
        "mode": mode,
        "count": len(results),
        "results": results
    }

@router.get("/assets")
def search_assets(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(5, description="Number of results")
):
    results = semantic_search_assets(q, top_k)
    return {
        "query": q,
        "count": len(results),
        "results": results
    }

@router.get("/stats")
def search_index_stats():
    return get_index_stats()

@router.post("/reindex")
def reindex_all():
    run_full_indexing(recreate=True)
    return {"status": "reindexing complete", "stats": get_index_stats()}