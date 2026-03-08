"""Agent-based operational intelligence endpoints."""

from fastapi import APIRouter, HTTPException
from typing import List

from app.api.schemas import (
    AgentAnalysisRequest,
    AgentAnalysisResponse,
    ErrorResponse,
)

from app.agents.security_agent import analyze_logs
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post(
    "/analyze",
    response_model=AgentAnalysisResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Analysis error"},
    },
    summary="Analyze operational logs",
    description="Analyze operational or incident logs and generate insights.",
)
async def analyze_logs_endpoint(
    request: AgentAnalysisRequest,
) -> AgentAnalysisResponse:
    """Analyze logs and return insights."""

    logger.info(f"Received agent analysis request for source: {request.source}")

    try:

        file_path = f"data/{request.source}.txt"

        with open(file_path) as f:
            logs = f.read()

        result = analyze_logs(logs)

        logger.info("Successfully completed log analysis")

        return AgentAnalysisResponse(
            summary=result["summary"],
            severity=result["severity"],
            recommendations=result["recommendations"],
        )

    except FileNotFoundError:
        logger.warning(f"Log source not found: {request.source}")

        raise HTTPException(
            status_code=400,
            detail=f"Source '{request.source}' not found",
        )

    except Exception as e:
        logger.error(f"Error analyzing logs: {e}")

        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing logs: {str(e)}",
        )