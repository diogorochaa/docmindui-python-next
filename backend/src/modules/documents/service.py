from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.modules.documents.repository import VectorDocumentRepository
from src.shared.exceptions import InvalidDocumentError


class DocumentIndexingService:
    def __init__(self, repository: VectorDocumentRepository) -> None:
        self._repository = repository

    def index_text(self, text: str) -> int:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(text)

        if not chunks:
            raise InvalidDocumentError("Documento sem conteúdo para indexação.")

        self._repository.persist_chunks(chunks)
        return len(chunks)
