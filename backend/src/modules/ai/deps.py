from fastapi import Depends

from src.core.dependencies import (
    get_embeddings_adapter,
    get_llm,
    get_vector_store,
)
from src.modules.ai.service import AiService


def get_ai_service(
    llm=Depends(get_llm),
    embeddings=Depends(get_embeddings_adapter),
    vector_store=Depends(get_vector_store),
) -> AiService:
    return AiService(llm=llm, embeddings=embeddings, vector_store=vector_store)
