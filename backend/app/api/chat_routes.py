from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db
from app.rag.pipeline import answer_question

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=schemas.ChatResponse)
def chat(
    payload: schemas.ChatRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # Save the user's question
    user_msg = models.ChatMessage(
        owner_id=current_user.id, role="user", content=payload.question
    )
    db.add(user_msg)
    db.commit()

    try:
        result = answer_question(
            owner_id=current_user.id,
            question=payload.question,
            document_ids=payload.document_ids,
        )
    except Exception as e:
        error_detail = str(e)
        if "API key" in error_detail or "401" in error_detail:
            detail = "OpenAI API key is not configured. Please configure OPENAI_API_KEY in .env file."
        else:
            detail = f"Error answering question: {error_detail}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

    assistant_msg = models.ChatMessage(
        owner_id=current_user.id,
        role="assistant",
        content=result["answer"],
        citations=result["citations"],
    )
    db.add(assistant_msg)
    db.commit()

    return result


@router.get("/history", response_model=list[schemas.ChatMessageOut])
def history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.owner_id == current_user.id)
        .order_by(models.ChatMessage.created_at.asc())
        .all()
    )


@router.delete("/history", status_code=204)
def clear_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db.query(models.ChatMessage).filter(
        models.ChatMessage.owner_id == current_user.id
    ).delete()
    db.commit()
    return None
