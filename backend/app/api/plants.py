from fastapi import APIRouter
from app.graph.neo4j_client import neo4j_client
from app.graph import queries

router = APIRouter()

@router.get("/summary")
def get_plant_summary():
    result = neo4j_client.run_query(queries.GET_PLANT_SUMMARY)
    return {"plants": result}

@router.get("/stats")
def get_graph_stats():
    result = neo4j_client.run_query(queries.GET_GRAPH_STATS)
    return {"graph_statistics": result}