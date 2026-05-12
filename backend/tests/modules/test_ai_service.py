from src.modules.ai.service import AiService


class FakeEmbeddings:
    def embed_query(self, query: str) -> list[float]:
        return [0.1, 0.2, float(len(query))]


class FakeVectorStore:
    def __init__(self, chunks: list[str]):
        self.chunks = chunks
        self.last_query = None

    def search(self, query_embedding: list[float], k: int = 3) -> list[str]:
        self.last_query = query_embedding
        return self.chunks[:k]


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    def __init__(self):
        self.last_prompt = ""

    def invoke(self, prompt: str) -> FakeResponse:
        self.last_prompt = prompt
        return FakeResponse("resposta final")


def test_ai_service_uses_context_and_llm():
    llm = FakeLLM()
    embeddings = FakeEmbeddings()
    vector_store = FakeVectorStore(["chunk 1", "chunk 2"])
    service = AiService(llm, embeddings, vector_store)

    result = service.ask("Qual o resumo?")

    assert result == "resposta final"
    assert "chunk 1" in llm.last_prompt
    assert "Qual o resumo?" in llm.last_prompt
    assert vector_store.last_query is not None
