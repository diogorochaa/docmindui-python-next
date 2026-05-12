from fastapi import APIRouter, Depends, status

from src.modules.messages.deps import get_message_service
from src.modules.messages.schemas import MessageCreateRequest, MessageResponse
from src.modules.messages.service import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/", response_model=list[MessageResponse])
def get_messages(service: MessageService = Depends(get_message_service)):
    messages = service.list_messages()
    return [
        MessageResponse(
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
        )
        for message in messages
    ]


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def post_message(
    payload: MessageCreateRequest,
    service: MessageService = Depends(get_message_service),
):
    message = service.create_message(
        conversation_id=payload.conversation_id,
        role=payload.role,
        content=payload.content,
    )
    return MessageResponse(
        conversation_id=message.conversation_id,
        role=message.role,
        content=message.content,
        created_at=message.created_at,
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_messages(service: MessageService = Depends(get_message_service)):
    service.clear_messages()
