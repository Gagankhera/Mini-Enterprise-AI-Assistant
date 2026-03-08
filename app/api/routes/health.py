"""Health check endpoints."""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app import __version__
from app.api.schemas import HealthResponse
from app.rag.vector_store import VectorStoreService
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
    summary="Basic health check",
    description="Returns basic health status of the service.",
)
async def health_check() -> HealthResponse:
    """Basic health check endpoint."""
    logger.debug("Health check requested")
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=__version__,
    )

