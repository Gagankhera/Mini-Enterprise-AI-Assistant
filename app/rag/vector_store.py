"""Vector store module for FAISS operations."""

from functools import lru_cache
from typing import List, Tuple, Any
from uuid import uuid4
import os

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from app.rag.embeddings import get_embeddings
from app.logger import get_logger

logger = get_logger(__name__)


INDEX_PATH = "faiss_index"


@lru_cache
def get_embeddings_model():
    """Return cached embeddings model."""
    return get_embeddings()


class VectorStoreService:
    """Service class for FAISS vector store operations."""

    def __init__(self) -> None:
        self.embeddings = get_embeddings_model()
        self.vector_store: FAISS | None = None

        # Auto load index if exists
        if os.path.exists(INDEX_PATH):
            try:
                self.load(INDEX_PATH)
            except Exception as e:
                logger.warning(f"Failed loading FAISS index: {e}")

        logger.info("VectorStoreService initialized")

    # ---------------------------------------------------
    # Document Ingestion
    # ---------------------------------------------------

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to vector store."""

        if not documents:
            logger.warning("No documents received for ingestion")
            return []

        ids = [str(uuid4()) for _ in documents]

        if self.vector_store is None:
            logger.info("Initializing FAISS index")

            self.vector_store = FAISS.from_documents(
                documents,
                self.embeddings,
                ids=ids
            )
        else:
            logger.info(f"Adding {len(documents)} documents to existing index")
            self.vector_store.add_documents(documents, ids=ids)

        logger.info(f"{len(documents)} documents added to FAISS")

        return ids

    # ---------------------------------------------------
    # Search
    # ---------------------------------------------------

    def search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search."""

        if self.vector_store is None:
            logger.warning("Search attempted on empty vector store")
            return []

        return self.vector_store.similarity_search(query, k=k)

    def search_with_scores(self, query: str, k: int = 4) -> List[Tuple[Document, float]]:
        """Search with similarity scores."""

        if self.vector_store is None:
            logger.warning("Search attempted on empty vector store")
            return []

        return self.vector_store.similarity_search_with_score(query, k=k)

    # ---------------------------------------------------
    # Retriever
    # ---------------------------------------------------

    def get_retriever(self, k: int = 4) -> Any:
        """Return retriever object."""

        if self.vector_store is None:
            raise RuntimeError(
                "Vector store not initialized. Please ingest documents first."
            )

        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )

    # ---------------------------------------------------
    # Persistence
    # ---------------------------------------------------

    def save(self, path: str = INDEX_PATH) -> None:
        """Persist FAISS index."""

        if self.vector_store is None:
            logger.warning("Nothing to save. Vector store empty.")
            return

        self.vector_store.save_local(path)
        logger.info(f"FAISS index saved at {path}")

    def load(self, path: str = INDEX_PATH) -> None:
        """Load FAISS index."""

        if not os.path.exists(path):
            logger.warning("FAISS index path does not exist")
            return

        self.vector_store = FAISS.load_local(
            path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        logger.info(f"FAISS index loaded from {path}")

    # ---------------------------------------------------
    # Metadata
    # ---------------------------------------------------

    def get_collection_info(self) -> dict:
        """Return basic index statistics."""

        if self.vector_store is None:
            return {
                "points_count": 0,
                "status": "empty"
            }

        return {
            "points_count": len(self.vector_store.index_to_docstore_id),
            "status": "active"
        }

    def health_check(self) -> bool:
        """Health check for vector store."""

        return self.vector_store is not None

@lru_cache
def get_vector_store() -> VectorStoreService:
    """Return shared VectorStoreService instance."""
    return VectorStoreService()