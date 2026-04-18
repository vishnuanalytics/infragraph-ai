from fastapi import APIRouter, HTTPException, Query
from app.graph.neo4j_client import neo4j_client
from app.graph import queries
from typing import Optional

router = APIRouter()

@router.get("/")
def get_all_assets(
    status: Optional[str] = Query(None, description="Filter by status: operational, degraded, under_maintenance"),
    asset_type: Optional[str] = Query(None, description="Filter by type: Compressor, HeatExchanger, Pipeline, Column")
):
    if status:
        result = neo4j_client.run_query(
            queries.GET_ASSETS_BY_STATUS,
            {"status": status}
        )
    elif asset_type:
        result = neo4j_client.run_query(
            queries.GET_ASSETS_BY_TYPE,
            {"asset_type": asset_type}
        )
    else:
        result = neo4j_client.run_query(queries.GET_ALL_ASSETS)

    return {"count": len(result), "assets": result}

@router.get("/high-risk")
def get_high_risk_assets():
    result = neo4j_client.run_query(queries.GET_HIGH_RISK_ASSETS)
    return {"count": len(result), "high_risk_assets": result}

@router.get("/shared-failures")
def get_assets_with_shared_failure_modes():
    result = neo4j_client.run_query(queries.GET_ASSETS_WITH_SAME_FAILURE_MODE)
    return {
        "description": "Assets that share the same failure mode — useful for predictive maintenance",
        "count": len(result),
        "relationships": result
    }

@router.get("/{asset_id}")
def get_asset_by_id(asset_id: str):
    result = neo4j_client.run_query(
        queries.GET_ASSET_BY_ID,
        {"asset_id": asset_id}
    )
    if not result:
        raise HTTPException(status_code=404, detail=f"Asset {asset_id} not found")
    return result[0]