from fastapi import APIRouter, Query
from app.graph.neo4j_client import neo4j_client
from app.graph import queries
from typing import Optional

router = APIRouter()

@router.get("/")
def get_all_incidents(
    severity: Optional[str] = Query(None, description="Filter: critical, high, medium, low"),
    start_date: Optional[str] = Query(None, description="Format: YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Format: YYYY-MM-DD")
):
    if severity:
        result = neo4j_client.run_query(
            queries.GET_INCIDENTS_BY_SEVERITY,
            {"severity": severity}
        )
    elif start_date and end_date:
        result = neo4j_client.run_query(
            queries.GET_INCIDENTS_BY_DATE_RANGE,
            {"start_date": start_date, "end_date": end_date}
        )
    else:
        result = neo4j_client.run_query(queries.GET_ALL_INCIDENTS)

    return {"count": len(result), "incidents": result}