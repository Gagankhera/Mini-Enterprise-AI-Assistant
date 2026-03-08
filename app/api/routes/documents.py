"""Document management endpoints."""

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.api.schemas import (
    DocumentUploadResponse,
    ErrorResponse,
)

from app.rag.document_processor import DocumentProcessor
from app.rag.vector_store import get_vector_store
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/documents", tags=["Documents"])

# Shared FAISS vector store instance
vector_store = get_vector_store()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file type"},
        500: {"model": ErrorResponse, "description": "Processing error"},
    },
    summary="Upload and ingest a document",
    description="Upload a document (PDF, TXT, or CSV) to be processed and added to the vector store.",
)
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload"),
) -> DocumentUploadResponse:
    """Upload and process a document."""

    logger.info(f"Received document upload: {file.filename}")

    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    try:
        # Process document
        processor = DocumentProcessor()
        chunks = processor.process_upload(file.file, file.filename)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No content could be extracted from the document",
            )

        # Add to FAISS vector store
        document_ids = vector_store.add_documents(chunks)

        # Save FAISS index locally (optional but recommended)
        vector_store.save()

        logger.info(
            f"Successfully processed {file.filename}: "
            f"{len(chunks)} chunks, {len(document_ids)} documents"
        )

        return DocumentUploadResponse(
            message="Document uploaded and processed successfully",
            filename=file.filename,
            chunks_created=len(chunks),
            document_ids=document_ids,
        )

    except ValueError as e:
        logger.warning(f"Invalid file upload: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}",
        )
