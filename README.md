# CortexFlow AI — Autonomous Knowledge & Decision Engine

CortexFlow AI is a production-quality full-stack AI application that acts as an intelligent company assistant. It combines AI Engineering, Machine Learning, Generative AI, RAG, and Full-Stack Development into a single unified platform.

## Features

- **Document Ingestion**: Upload PDFs and Images. Extracts text using PyPDF2 and Tesseract OCR.
- **RAG Engine**: Semantic search using `pgvector` and OpenAI Embeddings.
- **Machine Learning**: Document classification models trained with `scikit-learn` and tracked via `MLflow`.
- **SQL Agent**: Natural Language to SQL translation for querying structured business data securely.
- **AI Orchestrator**: An LLM-based intent router that delegates user queries to RAG, ML, SQL, or a Complex DAG Workflow combining multiple engines.
- **Background Workers**: Celery & Redis for asynchronous document chunking and embedding.
- **Frontend Dashboard**: A stunning Next.js interface with dark mode, animations, and a ChatGPT-style interface.

## Architecture

* **Frontend**: Next.js 14 (App Router), Tailwind CSS, React
* **Backend**: FastAPI, SQLAlchemy, Celery
* **Database**: PostgreSQL with `pgvector` extension
* **Cache/Broker**: Redis
* **ML Ops**: MLflow
* **LLM / AI**: LangChain, OpenAI (`gpt-4-turbo-preview`, `text-embedding-ada-002`)

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API Key

### 1. Start Infrastructure (Docker)
```bash
docker-compose up -d
```
This starts PostgreSQL (with pgvector), Redis, and the MLflow Tracking Server.

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the FastAPI Server
uvicorn app.main:app --reload --port 8000
```

### 3. Start Celery Worker
In a new terminal window:
```bash
cd backend
source venv/bin/activate
celery -A app.worker.celery_app worker --loglevel=info
```

### 4. Train ML Model
In a new terminal window:
```bash
cd ml
source ../backend/venv/bin/activate
python train_classifier.py
```

### 5. Frontend Setup
In a new terminal window:
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to access the CortexFlow AI platform.

## API Documentation
Once the backend is running, visit `http://localhost:8000/docs` for the interactive Swagger API documentation.

Core Endpoints:
- `POST /api/orchestrator/query` - Unified intent router
- `POST /api/documents/upload` - Upload and process docs
- `POST /api/sql/query` - SQL Agent standalone
- `POST /api/ml/predict` - ML Inference standalone
