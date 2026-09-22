flowchart TD

subgraph group_frontend["Web application"]
  node_app["Route application<br/>[App.jsx]"]
  node_auth_context["Authentication state<br/>[AuthContext.jsx]"]
  node_login["Sign in<br/>[Login.jsx]"]
  node_register["Registration<br/>[Register.jsx]"]
  node_chat_ui["Chat interface<br/>[Chat.jsx]"]
  node_documents_ui["Documents interface<br/>[Documents.jsx]"]
  node_profile_ui["Profile interface<br/>[Profile.jsx]"]
  node_api_client["API client<br/>[api.js]"]
end

subgraph group_api["API and identity"]
  node_main["FastAPI application<br/>[main.py]"]
  node_auth_routes["Authentication routes<br/>[auth_routes.py]"]
  node_document_routes["Document routes<br/>[document_routes.py]"]
  node_chat_routes["Chat routes<br/>[chat_routes.py]"]
  node_auth["Password and tokens<br/>[auth.py]"]
end

subgraph group_rag["Knowledge processing"]
  node_pipeline["RAG orchestration<br/>[pipeline.py]"]
  node_extract["Text extraction<br/>[extract.py]"]
  node_chunker["Chunking<br/>[chunker.py]"]
  node_embeddings["Embedding client<br/>[embeddings.py]"]
  node_chroma_client["Vector index client<br/>[chroma_client.py]"]
end

subgraph group_state["Persistent state"]
  node_files[("Uploaded files")]
  node_sql_db[("Relational database")]
  node_models["User and chat models<br/>[models.py]"]
  node_chroma[("ChromaDB index")]
end

node_employee(("Employee"))
node_model_service{{"OpenAI-compatible model service"}}

node_employee -->|"uses"| node_app
node_app -->|"routes"| node_login
node_app -->|"routes"| node_register
node_app -->|"routes"| node_chat_ui
node_app -->|"routes"| node_documents_ui
node_app -->|"routes"| node_profile_ui
node_login -->|"signs in"| node_auth_context
node_register -->|"registers"| node_auth_context
node_auth_context -->|"requests"| node_api_client
node_chat_ui -->|"requests"| node_api_client
node_documents_ui -->|"requests"| node_api_client
node_profile_ui -->|"requests"| node_api_client
node_api_client -->|"calls API"| node_main
node_main -->|"mounts"| node_auth_routes
node_main -->|"mounts"| node_document_routes
node_main -->|"mounts"| node_chat_routes
node_auth_routes -->|"uses"| node_auth
node_auth_routes -->|"reads/writes"| node_sql_db
node_document_routes -->|"writes/deletes"| node_files
node_document_routes -->|"reads/writes"| node_sql_db
node_document_routes -->|"ingests"| node_pipeline
node_document_routes -->|"deletes index"| node_chroma_client
node_pipeline -->|"extracts text"| node_extract
node_pipeline -->|"chunks text"| node_chunker
node_pipeline -->|"embeds chunks"| node_embeddings
node_pipeline -->|"stores/searches"| node_chroma_client
node_pipeline -->|"updates status"| node_sql_db
node_pipeline -->|"requests embeddings and answers"| node_model_service
node_embeddings -->|"requests embeddings"| node_model_service
node_chroma_client -->|"reads/writes"| node_chroma
node_chat_routes -->|"gets answer"| node_pipeline
node_chat_routes -->|"stores/reads history"| node_sql_db
node_chat_routes -->|"authenticates"| node_auth

click node_app "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/frontend/src/App.jsx"
click node_auth_context "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/frontend/src/contexts/AuthContext.jsx"
click node_login "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/frontend/src/pages/Login.jsx"
click node_register "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/frontend/src/pages/Register.jsx"
click node_chat_ui "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/frontend/src/pages/Chat.jsx"
click node_documents_ui "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/frontend/src/pages/Documents.jsx"
click node_profile_ui "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/frontend/src/pages/Profile.jsx"
click node_api_client "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/frontend/src/services/api.js"
click node_main "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/main.py"
click node_auth_routes "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/api/auth_routes.py"
click node_document_routes "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/api/document_routes.py"
click node_chat_routes "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/api/chat_routes.py"
click node_auth "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/auth.py"
click node_pipeline "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/rag/pipeline.py"
click node_extract "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/rag/extract.py"
click node_chunker "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/rag/chunker.py"
click node_embeddings "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/rag/embeddings.py"
click node_chroma_client "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/vector_db/chroma_client.py"
click node_models "https://github.com/markkyrollos/ai-powered-enterprise-knowledge-assistant/blob/main/backend/app/models.py"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_app,node_auth_context,node_login,node_register,node_chat_ui,node_documents_ui,node_profile_ui,node_api_client toneBlue
class node_main,node_auth_routes,node_document_routes,node_chat_routes,node_auth toneAmber
class node_pipeline,node_extract,node_chunker,node_embeddings,node_chroma_client toneMint
class node_files,node_sql_db,node_models,node_chroma toneRose
class node_employee,node_model_service toneIndigo
# Enterprise Knowledge Assistant (RAG)

An AI chatbot assistant that lets employees upload company documents (PDF, DOCX, Markdown, TXT)
and ask natural-language questions. Answers are grounded only in the uploaded content and
every answer cites the source document and chunk it came from.

> Example: _"How many vacation days do interns get?"_ → _"According to the Employee
> Handbook, interns receive 15 annual leave days... (Source: Employee_Handbook.pdf)"_

## Architecture

```
                    React Frontend (Vite + Tailwind)
                                 │
                          FastAPI Backend
             ┌───────────────────┼───────────────────┐
             │                   │                    │
        PostgreSQL           ChromaDB             Ollama
     (users, docs,        (chunk embeddings)    (embeddings + chat)
      chat history)
             │
      Uploaded files (local volume / S3-ready)
```

**RAG pipeline (on upload):**
`PDF/DOCX/MD → extract text → chunk (sliding window, overlap) → embed (Ollama) → store in ChromaDB + Postgres metadata`

**RAG pipeline (on question):**
`Question → embed → vector search (top-k, scoped to user) → build prompt with retrieved chunks → mistral answer → return answer + citations`

## Tech stack

| Layer      | Choice                                        |
| ---------- | --------------------------------------------- |
| Frontend   | React, Vite, Tailwind CSS, React Router       |
| Backend    | FastAPI, SQLAlchemy                           |
| Database   | PostgreSQL                                    |
| Vector DB  | ChromaDB                                      |
| Embeddings | Ollama `mistral`                              |
| LLM        | Ollama                                        |
| Auth       | JWT (python-jose) + bcrypt password hashing   |

## Project structure

```
enterprise-knowledge-assistant/
├── backend/
│   ├── app/
│   │   ├── api/            # auth, documents, chat routes
│   │   ├── rag/             # extraction, chunking, embeddings, pipeline
│   │   ├── vector_db/        # ChromaDB client wrapper
│   │   ├── main.py            # FastAPI app entrypoint
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic request/response schemas
│   │   ├── auth.py            # JWT + password hashing
│   │   ├── config.py          # settings from environment
│   │   └── database.py        # DB engine/session
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/            # Login, Register, Chat, Documents, Profile
│   │   ├── components/        # Layout, ProtectedRoute
│   │   ├── contexts/          # AuthContext
│   │   └── services/          # api.js (axios client)
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── README.md
```

## Getting started

### Option A — Docker Compose

Requires Docker and an Ollama API key.

```bash
git clone <your-repo-url>
cd enterprise-knowledge-assistant

# Configure backend secrets
cp backend/.env.example backend/.env
# then edit backend/.env and set OPENAI_API_KEY

docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API docs (Swagger): http://localhost:8000/docs

### Option B — Run locally without Docker

**Backend** (uses SQLite automatically):

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and set OPENAI_API_KEY

uvicorn app.main:app --reload --port 8000 # OR: python -m uvicorn app.main:app --reload --port 8000
```

**Frontend** (in a separate terminal):

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Visit http://localhost:5173, register an account, upload a document, and start asking
questions.

## API reference

| Method | Endpoint                | Description                               |
| ------ | ----------------------- | ----------------------------------------- |
| POST   | `/api/auth/register`    | Create an account                         |
| POST   | `/api/auth/login`       | Get a JWT access token                    |
| GET    | `/api/auth/me`          | Current user info                         |
| POST   | `/api/documents/upload` | Upload & process a document               |
| GET    | `/api/documents`        | List your documents                       |
| DELETE | `/api/documents/{id}`   | Delete a document                         |
| POST   | `/api/chat`             | Ask a question, get an answer + citations |
| GET    | `/api/chat/history`     | Full chat history                         |
| DELETE | `/api/chat/history`     | Clear chat history                        |

Full interactive docs are auto-generated by FastAPI at `/docs` once the backend is running.

## Notes

- The vector store is scoped per-user (`owner_id` filter on every query), so one user's
  documents are never visible to another
- Passwords are hashed with bcrypt; tokens are short-lived JWTs
- Swap `DATABASE_URL` in `backend/.env` to point at any Postgres instance (local, RDS,
  Supabase)
