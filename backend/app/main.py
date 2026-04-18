from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import assets, incidents, plants, api_query, search


app = FastAPI(
    title="InfraGraph AI",
    description="Industrial Asset Knowledge Graph with AI-Powered Q&A",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "project": "InfraGraph AI",
        "description": "Industrial Asset Knowledge Graph",
        "docs": "/docs"
    }

app.include_router(assets.router, prefix="/api/assets", tags=["Assets"])
app.include_router(incidents.router, prefix="/api/incidents", tags=["Incidents"])
app.include_router(plants.router, prefix="/api/plants", tags=["Plants"])
app.include_router(api_query.router, prefix="/api/ai", tags=["AI Q&A"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])




@app.get("/health")
def health():
    return {"status": "ok"}