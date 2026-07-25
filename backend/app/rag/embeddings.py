from typing import List

from openai import OpenAI

from app.config import settings

_client = OpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url
)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a batch of texts using the configured OpenAI embedding model."""
    if not texts:
        return []
    response = _client.embeddings.create(model=settings.embedding_model, input=texts)
    return [item.embedding for item in response.data]


def embed_query(text: str) -> List[float]:
    return embed_texts([text])[0]
