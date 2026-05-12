from functools import lru_cache
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from langchain_openai import ChatOpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.core.config import settings
from src.infrastructure.adapters.faiss_vector_store_adapter import (
    FaissVectorStoreAdapter,
)
from src.infrastructure.adapters.openai_embeddings_adapter import (
    OpenAIEmbeddingsAdapter,
)
from src.infrastructure.adapters.pdf_text_extractor import (
    PdfTextExtractorAdapter,
)
from src.infrastructure.database.models import User
from src.infrastructure.database.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def decode_access_token_subject(token: str) -> UUID:
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
    subject = payload.get("sub")
    if not subject:
        raise ValueError("Token sem subject.")
    return UUID(str(subject))


def get_settings():
    return settings


@lru_cache
def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
    )


@lru_cache
def get_embeddings_adapter():
    return OpenAIEmbeddingsAdapter()


@lru_cache
def get_vector_store():
    return FaissVectorStoreAdapter(persist_dir=settings.effective_vector_store_dir())


@lru_cache
def get_pdf_text_extractor():
    return PdfTextExtractorAdapter()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar o usuário.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id = decode_access_token_subject(token)
    except (JWTError, ValueError):
        raise credentials_error from None

    user = db.get(User, user_id)
    if user is None:
        raise credentials_error
    return user


def get_current_user_with_messages(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar o usuário.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = decode_access_token_subject(token)
    except (JWTError, ValueError):
        raise credentials_error from None

    stmt = select(User).options(selectinload(User.messages)).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise credentials_error
    return user
