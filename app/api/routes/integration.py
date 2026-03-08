"""External system integration endpoints."""

from fastapi import APIRouter, HTTPException
from typing import List

from app.api.schemas import (
    IntegrationSummaryResponse,
    ErrorResponse,
)

from app.integrations.github_integration import get_github_summary
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/integration", tags=["Integration"])


@router.get(
    "/github-summary",
    response_model=IntegrationSummaryResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Integration error"},
    },
    summary="Get GitHub activity summary",
    description="Retrieve and summarize GitHub repository activity.",
)
async def github_summary() -> IntegrationSummaryResponse:
    """Retrieve GitHub repository summary."""

    logger.info("Fetching GitHub repository summary")

    try:
        summary = get_github_summary()

        logger.info("Successfully generated GitHub summary")

        return IntegrationSummaryResponse(
            source="github",
            summary=summary,
        )

    except Exception as e:
        logger.error(f"Error retrieving GitHub summary: {e}")

        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving GitHub summary: {str(e)}",
        )