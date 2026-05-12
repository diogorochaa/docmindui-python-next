from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.dependencies import get_current_user
from src.infrastructure.database.models import User
from src.infrastructure.database.session import get_db
from src.modules.messages.repository import MessageRepository
from src.modules.messages.service import MessageService


def get_message_service(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageService:
    return MessageService(MessageRepository(db, current_user.id))
