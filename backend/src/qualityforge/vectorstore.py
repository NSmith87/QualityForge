"""Vector store: ChromaDB for MVP. Qdrant / Pinecone / Weaviate later."""

from __future__ import annotations

from typing import Protocol

import chromadb
from chromadb.api.models.Collection import Collection

from qualityforge.settings import Settings


class VectorStore(Protocol):
    def upsert(self, item_id: str, text: str, metadata: dict[str, str]) -> None: ...

    def query(self, text: str, limit: int = 5) -> list[str]: ...


class ChromaVectorStore:
    def __init__(self, settings: Settings) -> None:
        self._client = chromadb.PersistentClient(path=settings.chroma_path)
        self._collection: Collection = self._client.get_or_create_collection(
            settings.chroma_collection
        )

    def upsert(self, item_id: str, text: str, metadata: dict[str, str]) -> None:
        self._collection.upsert(ids=[item_id], documents=[text], metadatas=[metadata])

    def query(self, text: str, limit: int = 5) -> list[str]:
        result = self._collection.query(query_texts=[text], n_results=limit)
        documents = result.get("documents") or []
        return list(documents[0]) if documents else []


def build_vector_store(settings: Settings) -> VectorStore:
    if settings.vector_backend != "chroma":
        raise RuntimeError(
            f"{settings.vector_backend} is planned after MVP. Use VECTOR_BACKEND=chroma."
        )
    return ChromaVectorStore(settings)
