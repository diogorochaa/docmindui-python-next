from uuid import UUID

from src.modules.messages.repository import MessageRepository
from src.shared.message import Message


class MessageService:
    def __init__(self, repository: MessageRepository) -> None:
        self._repository = repository

    def create_message(self, conversation_id: UUID, role: str, content: str) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at="",
        )
        self._repository.add(message)
        return self._repository.list()[-1]

    def list_messages(self) -> list[Message]:
        return self._repository.list()

    def clear_messages(self) -> None:
        self._repository.clear()
