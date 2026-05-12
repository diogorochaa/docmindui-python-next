"""Tarefas Celery relacionadas a documentos e indexação."""

from celery import shared_task

from src.core.config import settings
from src.infrastructure.adapters.faiss_vector_store_adapter import FaissVectorStoreAdapter
from src.infrastructure.adapters.openai_embeddings_adapter import OpenAIEmbeddingsAdapter
from src.modules.documents.repository import VectorDocumentRepository
from src.modules.documents.service import DocumentIndexingService


@shared_task(
    name="documents.index_text",
    autoretry_for=(OSError, ConnectionError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def index_document_text_task(text: str) -> dict[str, int]:
    """Extrai embeddings e grava no vector store (persistido quando configurado)."""
    persist_dir = settings.effective_vector_store_dir()
    embeddings = OpenAIEmbeddingsAdapter()
    vector_store = FaissVectorStoreAdapter(persist_dir=persist_dir)
    repository = VectorDocumentRepository(embeddings, vector_store)
    service = DocumentIndexingService(repository)
    chunks_indexed = service.index_text(text)
    return {"chunks_indexed": chunks_indexed}
