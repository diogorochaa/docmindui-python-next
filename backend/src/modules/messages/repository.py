from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.infrastructure.database.models import ChatMessage
from src.shared.exceptions import ServiceUnavailableError
from src.shared.message import Message


class MessageRepository:
    """Persistência de mensagens por usuário via SQLAlchemy ORM."""

    def __init__(self, db: Session, user_id: UUID) -> None:
        self._db = db
        self._user_id = user_id

    def add(self, message: Message) -> None:
        row = ChatMessage(
            user_id=self._user_id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
        )
        try:
            self._db.add(row)
            self._db.flush()
        except SQLAlchemyError as exc:
            raise ServiceUnavailableError("PostgreSQL indisponível no momento.") from exc

    def list(self) -> list[Message]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == self._user_id)
            .order_by(ChatMessage.created_at.asc(), ChatMessage.id.asc())
        )
        try:
            rows = self._db.execute(stmt).scalars().all()
        except SQLAlchemyError as exc:
            raise ServiceUnavailableError("PostgreSQL indisponível no momento.") from exc

        return [
            Message(
                conversation_id=r.conversation_id,
                role=r.role,
                content=r.content,
                created_at=r.created_at.isoformat() if r.created_at else "",
            )
            for r in rows
        ]

    def clear(self) -> None:
        try:
            self._db.execute(delete(ChatMessage).where(ChatMessage.user_id == self._user_id))
        except SQLAlchemyError as exc:
            raise ServiceUnavailableError("PostgreSQL indisponível no momento.") from exc
