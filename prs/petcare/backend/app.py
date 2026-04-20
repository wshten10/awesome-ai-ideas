"""
PetCare AI - Main Application Entry Point
AI驱动全方位宠物健康管理平台
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database.session import init_db
from backend.health_monitor.api import router as health_monitor_router
from backend.knowledge_graph.api import router as knowledge_graph_router
from backend.training_assistant.api import router as training_assistant_router
from backend.health_predictor.api import router as health_predictor_router
from backend.community.api import router as community_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    await init_db()
    yield


app = FastAPI(
    title="PetCare AI",
    description="AI驱动全方位宠物健康管理平台",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_monitor_router, prefix="/api/v1/health-monitor", tags=["Health Monitor"])
app.include_router(knowledge_graph_router, prefix="/api/v1/knowledge-graph", tags=["Knowledge Graph"])
app.include_router(training_assistant_router, prefix="/api/v1/training", tags=["Training Assistant"])
app.include_router(health_predictor_router, prefix="/api/v1/health-predictor", tags=["Health Predictor"])
app.include_router(community_router, prefix="/api/v1/community", tags=["Community"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PetCare AI", "version": "0.1.0"}


@app.get("/")
async def root():
    return {
        "name": "PetCare AI",
        "description": "AI驱动全方位宠物健康管理平台",
        "docs": "/docs",
    }
