"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import Any,List
from pydantic import BaseModel, Field

# ============== Health Schemas ==============


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp",
    )
    version: str = Field(..., description="Application version")


# ============== Document Schemas ==============


class DocumentUploadResponse(BaseModel):
    """Response after document upload."""

    message: str = Field(..., description="Status message")
    filename: str = Field(..., description="Uploaded filename")
    chunks_created: int = Field(..., description="Number of chunks created")
    document_ids: list[str] = Field(..., description="List of document IDs")


class DocumentInfo(BaseModel):
    """Document information."""

    source: str = Field(..., description="Document source/filename")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Document metadata",
    )


# ============== Query Schemas ==============


class QueryRequest(BaseModel):
    """Request for RAG query."""

    question: str = Field(
        ...,
        description="Question to ask",
        min_length=1,
        max_length=1000,
    )
    include_sources: bool = Field(
        default=True,
        description="Include source documents in response",
    )
  

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What are the key security risks?",
                    "include_sources": True,
                
                }
            ]
        }
    }


class SourceDocument(BaseModel):
    """Source document information."""

    content: str = Field(..., description="Document content excerpt")
    metadata: dict[str, Any] = Field(..., description="Document metadata")



class QueryResponse(BaseModel):
    """Response for RAG query."""

    question: str = Field(..., description="Original question")
    answer: str = Field(..., description="Generated answer")
    sources: list[SourceDocument] | None = Field(
        None,
        description="Source documents used",
    )
    processing_time_ms: float = Field(
        ...,
        description="Query processing time in milliseconds",
    )

class IntegrationSummaryResponse(BaseModel):
    source: str
    summary: str


class AgentAnalysisRequest(BaseModel):
    source: str = Field(
        ...,
        example="incident_logs",
        description="Name of log source file without extension"
    )


class AgentAnalysisResponse(BaseModel):
    summary: str
    severity: str
    recommendations: List[str]

# ============== Error Schemas ==============


class ErrorResponse(BaseModel):
    """Error response."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: str | None = Field(None, description="Detailed error information")


class ValidationErrorResponse(BaseModel):
    """Validation error response."""

    error: str = Field(default="Validation Error", description="Error type")
    message: str = Field(..., description="Error message")
    errors: list[dict] = Field(..., description="Validation errors")



