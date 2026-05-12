"""Tarefas Celery relacionadas a documentos e indexação."""

from celery import shared_task

from src.application.use_cases.ingest_document import (
    IngestDocumentCommand,
    ingest_document_text,
)
from src.core.config import settings
from src.infrastructure.adapters.faiss_vector_store_adapter import FaissVectorStoreAdapter
from src.infrastructure.adapters.openai_embeddings_adapter import OpenAIEmbeddingsAdapter


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
    result = ingest_document_text(IngestDocumentCommand(text=text), embeddings, vector_store)
    return {"chunks_indexed": result.chunks_indexed}
