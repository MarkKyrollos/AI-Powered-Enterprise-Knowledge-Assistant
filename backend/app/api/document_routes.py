import os
import shutil
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db
from app.config import settings
from app.rag.extract import get_file_type
from app.rag.pipeline import ingest_document
from app.vector_db import chroma_client

router = APIRouter(prefix="/api/documents", tags=["documents"])

ALLOWED_TYPES = {"pdf", "docx", "md", "markdown", "txt"}


@router.post("/upload", response_model=schemas.DocumentOut, status_code=201)
def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    file_type = get_file_type(file.filename)
    if file_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '.{file_type}'. Allowed: {', '.join(sorted(ALLOWED_TYPES))}",
        )

    os.makedirs(settings.upload_dir, exist_ok=True)
    safe_name = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(settings.upload_dir, safe_name)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = models.Document(
        owner_id=current_user.id,
        filename=file.filename,
        filepath=filepath,
        file_type=file_type,
        status="processing",
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # Process synchronously so the client gets accurate status immediately.
    # (For very large files you could move this to background_tasks.add_task instead.)
    ingest_document(db, document, current_user.id)
    db.refresh(document)

    return document


@router.get("", response_model=list[schemas.DocumentOut])
def list_documents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return (
        db.query(models.Document)
        .filter(models.Document.owner_id == current_user.id)
        .order_by(models.Document.created_at.desc())
        .all()
    )


@router.delete("/{document_id}", status_code=204)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    document = (
        db.query(models.Document)
        .filter(models.Document.id == document_id, models.Document.owner_id == current_user.id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    chroma_client.delete_document(document_id)

    if os.path.exists(document.filepath):
        os.remove(document.filepath)

    db.delete(document)
    db.commit()
    return None
