from dotenv import load_dotenv
load_dotenv(override=True)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, documents, chat, ml, sql, orchestrator, analytics
from app.core.database import engine, Base
from app.models.user import User
from app.models.document import Document
from app.models.chunk import DocumentChunk
from sqlalchemy import text

# Create pgvector extension if it doesn't exist
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()

# Create tables (For dev only. In prod, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CortexFlow AI API",
    description="API for CortexFlow AI Autonomous Knowledge & Decision Engine",
    version="0.1.0",
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(ml.router, prefix="/api/ml", tags=["Machine Learning"])
app.include_router(sql.router, prefix="/api/sql", tags=["SQL Agent"])
app.include_router(orchestrator.router, prefix="/api/orchestrator", tags=["AI Orchestrator"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to CortexFlow AI API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
