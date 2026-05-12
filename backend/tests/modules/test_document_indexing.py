from src.modules.documents.repository import VectorDocumentRepository
from src.modules.documents.service import DocumentIndexingService
from src.shared.exceptions import InvalidDocumentError


class FakeEmbeddings:
    def embed_documents(self, chunks: list[str]) -> list[list[float]]:
        return [[float(len(chunk))] for chunk in chunks]


class FakeVectorStore:
    def __init__(self):
        self.added_texts = []
        self.added_embeddings = []

    def add(self, texts: list[str], embeddings: list[list[float]]) -> None:
        self.added_texts = texts
        self.added_embeddings = embeddings


def test_document_indexing_indexes_chunks():
    embeddings = FakeEmbeddings()
    vector_store = FakeVectorStore()
    service = DocumentIndexingService(VectorDocumentRepository(embeddings, vector_store))

    chunks_indexed = service.index_text("conteúdo relevante")

    assert vector_store.added_texts
    assert len(vector_store.added_texts) == len(vector_store.added_embeddings)
    assert chunks_indexed == len(vector_store.added_texts)


def test_document_indexing_rejects_empty_content():
    embeddings = FakeEmbeddings()
    vector_store = FakeVectorStore()
    service = DocumentIndexingService(VectorDocumentRepository(embeddings, vector_store))

    try:
        service.index_text("")
    except InvalidDocumentError as exc:
        assert "sem conteúdo" in str(exc)
    else:
        raise AssertionError("InvalidDocumentError era esperado para documento vazio.")
