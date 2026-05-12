from fastapi import APIRouter, Depends

from src.modules.ai.deps import get_ai_service
from src.modules.ai.schemas import AIRequest
from src.modules.ai.service import AiService

router = APIRouter(prefix="/ai")


@router.post("")
def ask(data: AIRequest, service: AiService = Depends(get_ai_service)):
    return {"response": service.ask(data.question)}
