"""
Extracts plain text (with page numbers where applicable) from uploaded files.
Returns a list of {"page": int, "text": str} blocks so citations can reference pages.
"""
import os
from typing import List, Dict

from pypdf import PdfReader
import docx


def extract_pdf(filepath: str) -> List[Dict]:
    reader = PdfReader(filepath)
    blocks = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            blocks.append({"page": i, "text": text})
    return blocks


def extract_docx(filepath: str) -> List[Dict]:
    document = docx.Document(filepath)
    full_text = "\n".join(p.text for p in document.paragraphs if p.text.strip())
    # DOCX has no reliable page concept without rendering; treat as a single "page".
    return [{"page": 1, "text": full_text}] if full_text.strip() else []


def extract_markdown_or_text(filepath: str) -> List[Dict]:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return [{"page": 1, "text": text}] if text.strip() else []


def extract_text_blocks(filepath: str, file_type: str) -> List[Dict]:
    file_type = file_type.lower()
    if file_type == "pdf":
        return extract_pdf(filepath)
    elif file_type == "docx":
        return extract_docx(filepath)
    elif file_type in ("md", "markdown", "txt"):
        return extract_markdown_or_text(filepath)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def get_file_type(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower().lstrip(".")
    return ext
