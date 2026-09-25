from typing import List, Dict


def chunk_text(  #chunk_text does the splitting of the text
    text: str, chunk_size: int = 1000, chunk_overlap: int = 150
) -> List[str]:
    """Simple sliding-window character chunker with overlap."""
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == length:
            break
        start = end - chunk_overlap
    return chunks


# chunk_document organizes the splitting for an entire document, and returns a list of chunks with page numbers and chunk indices.
def chunk_document(blocks: List[Dict], chunk_size: int = 1000, chunk_overlap: int = 150) -> List[Dict]:
    """
    Takes page-level blocks [{"page": n, "text": "..."}] and returns
    chunk-level records [{"page": n, "chunk_index": i, "text": "..."}]
    """
    chunks = []
    idx = 0
    for block in blocks:
        for c in chunk_text(block["text"], chunk_size, chunk_overlap):
            chunks.append({"page": block["page"], "chunk_index": idx, "text": c})
            idx += 1
    return chunks
