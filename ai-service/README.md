# AI Service — Tool-01 Risk Register

I am the core AI microservice that powers the risk description, categorisation, and analysis features. I use the Groq LLaMA 3.3-70b model for intelligent text generation and ChromaDB for retrieval-augmented generation (RAG).

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+**
- **Redis Server** (for caching)
- **Groq API Key** (starts with `gsk_`)

### Setup
1. **Clone and Navigate**:
   ```bash
   cd ai-service
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   Copy `.env.example` to `.env` and fill in your `GROQ_API_KEY`.
   ```bash
   cp .env.example .env
   ```

### Running the Service
**Development Mode**:
```bash
python app.py
```
**Production Mode (Gunicorn)**:
```bash
gunicorn --workers=4 --bind=0.0.0.0:5000 --timeout=120 "app:create_app()"
```

## ⚙️ Configuration
The service is configured via environment variables in the `.env` file:
- `GROQ_API_KEY`: Your secret key for Groq Cloud.
- `REDIS_URL`: The connection string for your Redis instance (default: `redis://localhost:6379`).

Central application settings (like the model name) are managed in `services/config.py`.

## 🛣️ API Reference

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/describe` | Generates a structured risk description from a brief note. |
| `POST` | `/categorise` | Classifies a risk into one of 8 standard categories. |
| `POST` | `/recommend` | Generates 3 actionable mitigation recommendations. |
| `POST` | `/query` | Answers questions using ingested knowledge base (RAG). |
| `POST` | `/generate-report` | Produces a formal executive risk report. |
| `POST` | `/generate-report/async` | Starts a background report generation job. |
| `GET` | `/generate-report/status/<id>` | Polls the status of an async report job. |
| `POST` | `/generate-report/stream` | Streams a report in real-time (SSE). |
| `POST` | `/analyse-document` | Extracts up to 10 risks from a large text block. |
| `POST` | `/batch-process` | Processes up to 20 risks (describe + categorise) in one go. |
| `POST` | `/ingest` | Adds a text document to the RAG knowledge base. |
| `GET` | `/health` | Returns live service metrics and health status. |

## 🧪 Testing
Run the unit test suite using pytest:
```bash
pytest
```
To run end-to-end security or quality tests, use the standalone scripts in the `tests/` folder.
