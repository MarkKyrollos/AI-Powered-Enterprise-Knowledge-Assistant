import datetime
from typing import Optional, List, Any

from pydantic import BaseModel, EmailStr


# ---------- Auth ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Documents ----------
class DocumentOut(BaseModel):
    id: int
    filename: str
    file_type: str
    num_chunks: int
    status: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# ---------- Chat ----------
class ChatRequest(BaseModel):
    question: str
    document_ids: Optional[List[int]] = None  # optionally scope to specific docs


class Citation(BaseModel):
    document_id: int
    filename: str
    chunk_index: int
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]


class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    citations: Optional[Any] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True
