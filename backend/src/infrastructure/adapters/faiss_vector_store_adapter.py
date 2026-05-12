from pathlib import Path

from src.infrastructure.gateways.faiss_store import VectorStore


class FaissVectorStoreAdapter:
    def __init__(self, persist_dir: Path | None = None) -> None:
        self._persist_dir = persist_dir
        self._store = VectorStore()
        self._loaded_mtime: float = 0.0
        if persist_dir is not None:
            self._maybe_reload()

    def _maybe_reload(self) -> None:
        if self._persist_dir is None:
            return
        index_path = self._persist_dir / "index.faiss"
        if not index_path.exists():
            return
        mtime = index_path.stat().st_mtime
        if mtime <= self._loaded_mtime:
            return
        loaded = VectorStore.load(self._persist_dir)
        if loaded is not None:
            self._store = loaded
            self._loaded_mtime = mtime

    def add(self, texts: list[str], embeddings: list[list[float]]) -> None:
        self._maybe_reload()
        self._store.add(texts, embeddings)
        if self._persist_dir is not None:
            self._store.save(self._persist_dir)
            idx = self._persist_dir / "index.faiss"
            if idx.exists():
                self._loaded_mtime = idx.stat().st_mtime

    def search(self, query_embedding: list[float], k: int = 3) -> list[str]:
        self._maybe_reload()
        return self._store.search(query_embedding, k)
