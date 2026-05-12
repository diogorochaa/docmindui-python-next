from dataclasses import replace

from fastapi.testclient import TestClient

from src.core.dependencies import (
    get_embeddings_adapter,
    get_llm,
    get_message_history,
    get_pdf_text_extractor,
    get_vector_store,
)
from src.domain.exceptions import InvalidDocumentError
from src.domain.message import Message
from src.main import app


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    def invoke(self, prompt: str) -> FakeResponse:
        return FakeResponse(f"ok: {prompt[:20]}")


class FakeEmbeddings:
    def embed_documents(self, chunks: list[str]) -> list[list[float]]:
        return [[float(len(chunk))] for chunk in chunks]

    def embed_query(self, query: str) -> list[float]:
        return [0.1, float(len(query))]


class FakeVectorStore:
    def __init__(self):
        self.texts = []

    def add(self, texts: list[str], embeddings: list[list[float]]) -> None:
        _ = embeddings
        self.texts.extend(texts)

    def search(self, query_embedding: list[float], k: int = 3) -> list[str]:
        _ = query_embedding
        return self.texts[:k] or ["contexto fake"]


class FakePdfExtractor:
    def extract(self, file_bytes: bytes) -> str:
        _ = file_bytes
        return "conteúdo pdf fake"


class BrokenPdfExtractor:
    def extract(self, file_bytes: bytes) -> str:
        _ = file_bytes
        raise InvalidDocumentError("PDF inválido ou corrompido.")


class FakeMessageHistory:
    def __init__(self) -> None:
        self.items: list[Message] = []

    def add(self, message: Message) -> None:
        self.items.append(replace(message, created_at="2026-01-01T00:00:00+00:00"))

    def list(self) -> list[Message]:
        return self.items

    def clear(self) -> None:
        self.items = []


def test_health_route_returns_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ai_route_returns_response_with_overrides():
    app.dependency_overrides[get_llm] = lambda: FakeLLM()
    app.dependency_overrides[get_embeddings_adapter] = lambda: FakeEmbeddings()
    app.dependency_overrides[get_vector_store] = lambda: FakeVectorStore()
    client = TestClient(app)

    response = client.post("/ai/", json={"question": "Pergunta teste"})

    assert response.status_code == 200
    assert "response" in response.json()
    app.dependency_overrides.clear()


def test_upload_route_indexes_document_with_overrides():
    app.dependency_overrides[get_pdf_text_extractor] = lambda: FakePdfExtractor()
    app.dependency_overrides[get_embeddings_adapter] = lambda: FakeEmbeddings()
    app.dependency_overrides[get_vector_store] = lambda: FakeVectorStore()
    client = TestClient(app)

    response = client.post(
        "/upload/",
        files={"file": ("doc.pdf", b"fake-bytes", "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "document indexed"
    assert response.json()["chunks_indexed"] >= 1
    app.dependency_overrides.clear()


def test_upload_route_returns_400_for_invalid_document():
    app.dependency_overrides[get_pdf_text_extractor] = lambda: BrokenPdfExtractor()
    app.dependency_overrides[get_embeddings_adapter] = lambda: FakeEmbeddings()
    app.dependency_overrides[get_vector_store] = lambda: FakeVectorStore()
    client = TestClient(app)

    response = client.post(
        "/upload/",
        files={"file": ("broken.pdf", b"broken", "application/pdf")},
    )

    assert response.status_code == 400
    assert "detail" in response.json()
    app.dependency_overrides.clear()


def test_auth_register_login_and_duplicate_email():
    client = TestClient(app)

    reg = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "senha1234"},
    )
    assert reg.status_code == 201
    assert reg.json()["email"] == "user@example.com"
    assert "id" in reg.json()

    dup = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "outrasenha12"},
    )
    assert dup.status_code == 409

    bad_login = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "errada"},
    )
    assert bad_login.status_code == 401

    ok = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "senha1234"},
    )
    assert ok.status_code == 200
    body = ok.json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body


def test_messages_routes_create_list_and_clear():
    fake_history = FakeMessageHistory()
    app.dependency_overrides[get_message_history] = lambda: fake_history
    client = TestClient(app)

    conv_id = "550e8400-e29b-41d4-a716-446655440000"
    create = client.post(
        "/messages/",
        json={
            "conversation_id": conv_id,
            "role": "user",
            "content": "oi",
        },
    )
    assert create.status_code == 201
    assert create.json()["content"] == "oi"
    assert create.json()["conversation_id"] == conv_id

    read = client.get("/messages/")
    assert read.status_code == 200
    assert len(read.json()) == 1

    clear = client.delete("/messages/")
    assert clear.status_code == 204
    app.dependency_overrides.clear()
