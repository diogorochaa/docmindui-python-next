from fastapi import Depends

from src.core.dependencies import (
    get_embeddings_adapter,
    get_vector_store,
)
from src.modules.documents.repository import VectorDocumentRepository
from src.modules.documents.service import DocumentIndexingService


def get_vector_document_repository(
    embeddings=Depends(get_embeddings_adapter),
    vector_store=Depends(get_vector_store),
) -> VectorDocumentRepository:
    return VectorDocumentRepository(embeddings, vector_store)


def get_document_indexing_service(
    repository: VectorDocumentRepository = Depends(get_vector_document_repository),
) -> DocumentIndexingService:
    return DocumentIndexingService(repository)
