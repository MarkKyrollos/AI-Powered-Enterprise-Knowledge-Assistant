from typing import List, Optional

from openai import OpenAI
from sqlalchemy.orm import Session

from app.config import settings
from app.rag.extract import extract_text_blocks
from app.rag.chunker import chunk_document
from app.rag.embeddings import embed_texts, embed_query
from app.vector_db import chroma_client
from app import models

_client_kwargs = {"base_url": settings.openai_base_url}
if settings.openai_api_key:
    _client_kwargs["api_key"] = settings.openai_api_key

_client = OpenAI(**_client_kwargs)

SYSTEM_PROMPT = (
    "You are an enterprise knowledge assistant. Answer the user's question using ONLY "
    "the provided document excerpts. If the answer is not contained in the excerpts, "
    "say you don't have enough information in the uploaded documents. Always be concise "
    "and factual. Do not make up information that isn't in the excerpts."
)


def ingest_document(db: Session, document: models.Document, owner_id: int):
    """Extract, chunk, embed, and store a document's content. Updates document status."""
    try:
        blocks = extract_text_blocks(document.filepath, document.file_type)
        chunks = chunk_document(blocks)

        if not chunks:
            document.status = "failed"
            document.num_chunks = 0
            db.commit()
            return

        texts = [c["text"] for c in chunks]
        embeddings = embed_texts(texts)

        chroma_client.add_chunks(
            owner_id=owner_id,
            document_id=document.id,
            filename=document.filename,
            chunks=chunks,
            embeddings=embeddings,
        )

        document.num_chunks = len(chunks)
        document.status = "ready"
        db.commit()
    except Exception:
        document.status = "failed"
        db.commit()
        raise


def answer_question(
    owner_id: int, question: str, document_ids: Optional[List[int]] = None, top_k: int = 5
):
    query_embedding = embed_query(question)
    hits = chroma_client.query(
        owner_id=owner_id, query_embedding=query_embedding, top_k=top_k, document_ids=document_ids
    )

    if not hits:
        return {
            "answer": "No documents uploaded yet. Please upload documents first before asking questions. Go to the Documents page to upload files.",
            "citations": [],
        }

    context_blocks = []
    for h in hits:
        context_blocks.append(
            f"[Source: {h['filename']}, Page {h['page']}]\n{h['text']}"
        )
    context = "\n\n---\n\n".join(context_blocks)

    user_prompt = (
        f"Document excerpts:\n\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the excerpts above, and mention which document/page "
        "each key fact comes from."
    )

    completion = _client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    answer = completion.choices[0].message.content

    citations = [
        {
            "document_id": h["document_id"],
            "filename": h["filename"],
            "chunk_index": h["chunk_index"],
            "snippet": h["text"][:300],
        }
        for h in hits
    ]

    return {"answer": answer, "citations": citations}
