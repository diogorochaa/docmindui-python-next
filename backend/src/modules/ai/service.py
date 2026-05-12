class AiService:
    def __init__(self, llm, embeddings, vector_store) -> None:
        self._llm = llm
        self._embeddings = embeddings
        self._vector_store = vector_store

    def ask(self, question: str) -> str:
        query_embedding = self._embeddings.embed_query(question)
        context_chunks = self._vector_store.search(query_embedding)
        context = "\n\n".join(context_chunks)

        prompt = f"""
    Responda com base no contexto abaixo:

    {context}

    Pergunta: {question}
    """

        response = self._llm.invoke(prompt)
        return response.content
