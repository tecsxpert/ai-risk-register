# Status Update Report — Tool-01 AI Risk Register
**Project:** AI Risk Register  
**Current Phase:** Week 1 Foundation Complete  
**Date:** 2 May 2026  
**Author:** I (Solo Developer)

---

## 1. Project Overview
I have successfully built the core brain of the **AI Risk Register**. This week focused on creating a high-performance AI service that can understand, categorise, and recommend fixes for corporate risks. The system is designed to be "knowledge-aware" using a technique called RAG (Retrieval Augmented Generation), meaning it doesn't just guess—it looks up facts from my provided knowledge base before answering.

---

## 2. The AI Pipeline: How It Works

I have designed a multi-stage pipeline that ensures every risk entered is cleaned, analysed, and enriched with expert knowledge.

### Phase 1: Security & Cleaning (The Sanitiser)
When you submit a risk, it first passes through my **Sanitisation Layer**:
- **Data Input:** The request enters via a `POST` call (e.g., to `/describe`).
- **HTML Stripping:** I use the `bleach` library to strip any HTML tags. This prevents attackers from injecting malicious scripts.
- **Injection Blocking:** I run the text through a regex engine. If I see patterns like *"Ignore previous instructions"*, I block the request entirely (HTTP 400).
- **Result:** Only "clean" text reaches the AI models.

### Phase 2: Knowledge Ingestion & Storage (RAG)
Before the AI can give expert advice, I "teach" it using your documents:
- **Chunking:** I take a large document and break it into 500-character pieces with a 50-character overlap. This ensures context isn't lost at the edges.
- **Embedding:** Each chunk is converted into a **Vector** (a mathematical signature) using the `all-MiniLM-L6-v2` model.
- **Persistence:** These vectors and text chunks are saved in **ChromaDB**. Unlike a normal database, this allows me to search by "meaning" rather than just keywords.
- **Command to Run:** `python app.py` (which exposes the `/ingest` endpoint).

### Phase 3: Analysis & Generation (The AI Brain)
When a clean risk is ready for analysis:
- **Retrieval:** If using the `/query` endpoint, I find the top-3 most relevant knowledge chunks from ChromaDB.
- **Prompting:** I construct a detailed prompt template and inject your text (and context) into it.
- **Groq Acceleration:** I send this to the **Groq API**. I've chosen the **Llama-3.3-70b-versatile** model for its extreme speed and reasoning capability.
- **Final Output:** The AI returns a structured JSON object. My code parses this and adds a `generated_at` timestamp.

---

## 3. Getting Started: Commands & Setup

I've made the setup process straightforward and reproducible.

### Step 1: Environment Setup
First, I create a clean space for the project's tools.
```powershell
cd ai-service
# I create the virtual environment
python -m venv venv
# I activate it
.\venv\Scripts\activate
# I install all my requirements
pip install -r requirements.txt
```

### Step 2: Running the Brain
To start the Flask service:
```powershell
python app.py
```
**What to expect:** The console will show `* Running on http://127.0.0.1:5000`. This means I am ready to receive risk data.

### Step 3: Verification (The Tests)
I've written scripts to verify every part of the pipeline. Run these in a new terminal:
- `python tests/test_groq.py`: Tests if I can talk to the Groq AI. (Expect: "SUCCESS")
- `python tests/test_chroma.py`: Tests if I can save and find knowledge. (Expect: "[PASS]")
- `python tests/run_security_tests.py`: Tests my security gates. (Expect: 15/15 PASS)

---

## 4. API Endpoints (The Control Panel)

I've exposed these endpoints for the frontend and Java backend to use. All endpoints expect and return **JSON**.

| Endpoint | Purpose | Required Input | Expected Output |
| :--- | :--- | :--- | :--- |
| `POST /describe` | Write professional descriptions | `{"text": "short notes"}` | Full risk profile (title, impact, etc.) |
| `POST /categorise` | Classify risk type | `{"text": "risk desc"}` | `{"category": "SECURITY", ...}` |
| `POST /ingest` | Add knowledge to database | `{"text": "...", "source": "..."}` | `{"status": "success"}` |
| `POST /query` | Ask the database questions | `{"text": "How do we fix X?"}` | Answer + Sources used |

---

## 5. Technical Summary for Professionals
- **Core:** Flask (Python) with Blueprint-based routing.
- **AI Model:** Llama-3.3-70b (via Groq Cloud).
- **Vector DB:** ChromaDB (Persistent Client) using Cosine Similarity.
- **Embeddings:** `all-MiniLM-L6-v2` (Sentence-Transformers).
- **Security:** Global `before_request` hook with recursive JSON traversal and `bleach` sanitisation.
- **Rate Limiting:** `flask-limiter` set to 30 requests per minute.

**Conclusion:** I have built a secure, high-speed AI foundation. The data flow from raw input to sanitised text, retrieved context, and finally structured AI output is fully automated and verified.
