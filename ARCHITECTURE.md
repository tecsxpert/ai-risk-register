# System Architecture — AI Risk Register

I have designed this system as a high-performance, resilient AI-powered risk management platform. The architecture is split between a robust Spring Boot backend and a specialized Flask AI microservice.

## 1. High-Level Overview

My system follows a decoupled microservices pattern:
- **Java Backend (Spring Boot)**: Manages the core business logic, user authentication (JWT), and the main risk database (MySQL).
- **AI Microservice (Flask)**: A specialized intelligence layer that handles NLP tasks, RAG (Retrieval-Augmented Generation), and report generation using Groq Llama 3 models.
- **Communication**: All inter-service communication happens via RESTful APIs using standard JSON payloads.

## 2. Component Breakdown

### A. Java Backend (The Core)
*   **Controllers**: I've exposed a REST API for the frontend to manage risks and documents.
*   **Service Layer**: I handle complex workflows, such as triggering background AI enrichment when a risk is saved.
*   **Security**: I've implemented Spring Security with JWT. Every request to the backend must carry a valid token.
*   **AI Service Client**: I built a centralized component (`AiServiceClient.java`) that communicates with the Flask service, featuring a 10-second timeout to prevent blocking.

### B. AI Microservice (The Intelligence)
*   **Model Layer**: I'm using `llama-3.3-70b-versatile` via Groq Cloud. This provides high-speed, high-quality reasoning without requiring local GPUs.
*   **Vector Store (RAG)**: I use **ChromaDB** to store and search through document embeddings, allowing the AI to "know" specific risk policies and standards.
*   **Caching Layer**: I've integrated **Redis** to store AI responses. If I receive the same input twice, I serve the result from the cache in <10ms.
*   **Rate Limiting**: I use `flask-limiter` to protect my service from being overwhelmed and to manage my Groq API quota.

### C. Data Flow
1. **Risk Creation**: When I save a risk in the Java backend, a background task (`@Async`) sends the raw text to the AI `/describe` endpoint.
2. **AI Enrichment**: The AI service sanitizes the input, checks the Redis cache, and if needed, calls Groq to generate a professional description.
3. **RAG Querying**: When I ask a question via `/query`, the AI service embeds the question, finds relevant context in ChromaDB, and passes both to Groq to generate a grounded answer.
4. **Batch Processing**: For large datasets, I use the `/batch-process` endpoint which handles multiple items with a 100ms inter-item delay to respect rate limits.

## 3. Resilience & Security
*   **Sanitization**: Every input to the AI service is sanitized via a global middleware to block prompt injection and HTML.
*   **Fallback Logic**: If the Groq API is down or times out, my service returns a structured fallback response so the UI never breaks.
*   **Thread Safety**: My Flask service runs with `threaded=True` and my job queue uses `threading.Lock` to handle concurrent user requests safely.

## 4. Technology Stack
- **Languages**: Java 17+, Python 3.11+
- **Frameworks**: Spring Boot 3.x, Flask 3.x
- **Databases**: MySQL (Metadata), ChromaDB (Vectors), Redis (Cache)
- **AI Models**: Llama 3.3 (Reasoning), SentenceTransformers (Embeddings)
