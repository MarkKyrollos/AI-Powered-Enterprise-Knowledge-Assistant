from typing import List, Dict, Optional

import chromadb

from app.config import settings

_client = chromadb.PersistentClient(path=settings.chroma_path)
_collection = _client.get_or_create_collection(name="documents")


def add_chunks(
    owner_id: int,
    document_id: int,
    filename: str,
    chunks: List[Dict],
    embeddings: List[List[float]],
):
    ids = [f"{document_id}-{c['chunk_index']}" for c in chunks]
    metadatas = [
        {
            "owner_id": owner_id,
            "document_id": document_id,
            "filename": filename,
            "page": c["page"],
            "chunk_index": c["chunk_index"],
        }
        for c in chunks
    ]
    documents = [c["text"] for c in chunks]
    _collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)


def query(
    owner_id: int,
    query_embedding: List[float],
    top_k: int = 5,
    document_ids: Optional[List[int]] = None,
) -> List[Dict]:
    where = {"owner_id": owner_id}
    if document_ids:
        where = {"$and": [{"owner_id": owner_id}, {"document_id": {"$in": document_ids}}]}

    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
    )

    hits = []
    if not results.get("ids") or not results["ids"][0]:
        return hits

    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        hits.append(
            {
                "text": doc,
                "document_id": meta["document_id"],
                "filename": meta["filename"],
                "page": meta["page"],
                "chunk_index": meta["chunk_index"],
                "distance": dist,
            }
        )
    return hits


def delete_document(document_id: int):
    _collection.delete(where={"document_id": document_id})
