from celery.exceptions import CeleryError
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.core.config import settings
from src.core.dependencies import get_pdf_text_extractor, get_vector_store
from src.modules.documents.deps import get_document_indexing_service
from src.modules.documents.service import DocumentIndexingService
from src.shared.exceptions import InvalidDocumentError

router = APIRouter(prefix="/upload")


@router.post("/")
async def upload(
    file: UploadFile = File(...),
    extractor=Depends(get_pdf_text_extractor),
    indexing: DocumentIndexingService = Depends(get_document_indexing_service),
):
    content = await file.read()
    text = extractor.extract(content)

    if settings.CELERY_INDEX_DOCUMENTS:
        from src.workers.document_tasks import index_document_text_task

        async_result = index_document_text_task.delay(text)
        try:
            payload = async_result.get(timeout=settings.CELERY_INDEX_TASK_TIMEOUT_SECONDS)
        except TimeoutError as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Tempo esgotado ao indexar o documento. Tente novamente.",
            ) from exc
        except InvalidDocumentError:
            raise
        except CeleryError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Falha ao processar o documento na fila. Tente novamente em instantes.",
            ) from exc

        get_vector_store.cache_clear()
        return {"status": "document indexed", "chunks_indexed": payload["chunks_indexed"]}

    chunks_indexed = indexing.index_text(text)

    return {"status": "document indexed", "chunks_indexed": chunks_indexed}
