import pickle
from pathlib import Path
from typing import IO, Any

import faiss
import numpy as np

try:
    import fcntl

    _HAS_FCNTL = True
except ImportError:
    _HAS_FCNTL = False


def _flock_lock(file_obj: IO[Any], exclusive: bool) -> None:
    if not _HAS_FCNTL:
        return
    fd = file_obj.fileno()
    fcntl.flock(fd, fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)


def _flock_unlock(file_obj: IO[Any]) -> None:
    if not _HAS_FCNTL:
        return
    fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)


class VectorStore:
    """Armazenamento vetorial em memória com persistência opcional em disco."""

    EMBEDDING_DIM = 1536

    def __init__(self) -> None:
        self.index = faiss.IndexFlatL2(self.EMBEDDING_DIM)
        self.documents: list[str] = []

    def add(self, texts: list[str], embeddings: list[list[float]]) -> None:
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.documents.extend(texts)

    def search(self, query_embedding: list[float], k: int = 3) -> list[str]:
        if not self.documents:
            return []

        query_vector = np.array([query_embedding]).astype("float32")
        _, indices = self.index.search(query_vector, min(k, len(self.documents)))
        return [self.documents[i] for i in indices[0] if i != -1]

    @classmethod
    def load(cls, directory: Path) -> "VectorStore | None":
        index_path = directory / "index.faiss"
        docs_path = directory / "documents.pkl"
        if not index_path.exists() or not docs_path.exists():
            return None
        with open(directory / ".lock", "a+b") as lock_file:
            _flock_lock(lock_file, exclusive=False)
            try:
                store = cls.__new__(cls)
                store.index = faiss.read_index(str(index_path))
                with open(docs_path, "rb") as doc_file:
                    store.documents = pickle.load(doc_file)
                return store
            finally:
                _flock_unlock(lock_file)

    def save(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        index_path = directory / "index.faiss"
        docs_path = directory / "documents.pkl"
        tmp_docs = directory / "documents.pkl.tmp"
        lock_path = directory / ".lock"
        with open(lock_path, "a+b") as lock_file:
            _flock_lock(lock_file, exclusive=True)
            try:
                faiss.write_index(self.index, str(index_path))
                with open(tmp_docs, "wb") as doc_file:
                    pickle.dump(self.documents, doc_file, protocol=pickle.HIGHEST_PROTOCOL)
                tmp_docs.replace(docs_path)
            finally:
                _flock_unlock(lock_file)
