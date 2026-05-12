class VectorDocumentRepository:
    def __init__(self, embeddings, vector_store) -> None:
        self._embeddings = embeddings
        self._vector_store = vector_store

    def persist_chunks(self, chunks: list[str]) -> None:
        vectors = self._embeddings.embed_documents(chunks)
        self._vector_store.add(chunks, vectors)
