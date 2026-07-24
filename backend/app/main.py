from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models  # noqa: F401 (ensures models are registered before create_all)
from app.api import auth_routes, document_routes, chat_routes
from app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    description="RAG-powered API that answers questions from uploaded company documents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(document_routes.router)
app.include_router(chat_routes.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
