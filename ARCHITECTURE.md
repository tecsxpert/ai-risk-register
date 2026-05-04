# Engineering Blueprint: Building the AI Risk Register from Scratch

This document is a comprehensive, step-by-step reconstruction guide for the AI Risk Register. I have written this for anyone—from a senior architect to a newcomer—to understand exactly **why** every file exists, **what** every line does, and **how** to rebuild this system from the ground up.

---

## Part 1: Project Philosophy & Foundation

The goal of this system is to take messy, unstructured human text and turn it into high-quality, structured risk data. To do this, I chose a **Microservice Architecture**.

### Why Microservices?
- **Isolation**: If the AI model is slow, it doesn't slow down the user's ability to login to the Java app.
- **Language Choice**: I used **Python** for the AI service because it has the best libraries for LLMs (Groq, ChromaDB), and **Java** for the backend because of its enterprise reliability (Spring Boot).

---

## Part 2: Phase-by-Phase Reconstruction

### Phase 1: The Environment & Configuration
Every project needs a place to store its secrets and dependencies.

#### 1. `requirements.txt`
*   **Why**: This file lists every Python library I need.
*   **Key Lines**:
    - `flask`: The web framework. I chose it because it's lightweight.
    - `groq`: The client library for our Llama 3 model.
    - `chromadb`: Our vector database for RAG.
    - `redis`: For caching responses to save money and time.

#### 2. `.env`
*   **Why**: I never hardcode API keys. This file stays on my local machine (and is in `.gitignore`) to keep the `GROQ_API_KEY` secret.

---

### Phase 2: The Intelligence Engine (`services/groq_client.py`)
This is the heart of the system. It talks to the Groq Cloud.

*   **`client = Groq(api_key=os.getenv('GROQ_API_KEY'))`**: I initialize the connection here. If the key is missing, the service will fail immediately.
*   **`def call_groq(...)`**: I built this function to be flexible.
    - **Prompt Loading**: It reads text files from the `prompts/` folder. This keeps my code clean—I don't have long text strings inside my Python files.
    - **Retry Logic**: I added a `for attempt in range(max_retries)` loop. AI APIs can sometimes glitch; this ensures we try again 3 times before giving up.
    - **JSON Cleaning**: LLMs often wrap their answers in "markdown blocks" (like \`\`\`json). I wrote code to strip these out so I can parse the raw JSON data reliably.

---

### Phase 3: The Knowledge Base (`services/chroma_client.py`)
This is how the AI "reads" my policy documents.

*   **`model = SentenceTransformer('all-MiniLM-L6-v2')`**: This model turns text into numbers (vectors).
*   **ChromaDB**: I chose ChromaDB because it's "AI-native." It stores these numbers and lets me ask, "Which document segment is most similar to this user question?"
*   **`def get_context(query)`**: This takes a user's question, turns it into a vector, and finds the top 3 relevant paragraphs from our documents.

---

### Phase 4: Performance Layer (`services/ai_cache.py`)
AI calls are expensive and slow (~1 second). I want them to be free and fast.

*   **SHA256 Hashing**: I take the user's input and turn it into a unique 64-character ID.
*   **Redis**: I store the AI's answer in Redis using that ID. If the next user asks the exact same thing, I find the ID in Redis and return the answer in **5 milliseconds** instead of 1000ms.

---

### Phase 5: The Web Interface (`app.py` & Blueprints)
I use **Flask Blueprints** to organize my routes. Instead of one giant file, every feature has its own file in the `routes/` folder.

*   **`limiter = Limiter(...)`**: I added this to prevent "Brute Force" or "Denial of Service" attacks. It restricts users to 30 requests per minute.
*   **`@app.before_request`**: This is my security guard. Every single request passes through here first to be **sanitized** (stripping out malicious code or "Prompt Injection" attempts).

---

### Phase 6: Scaling for Production

#### 1. Batch Processing (`routes/batch_process.py`)
*   **The 100ms Delay**: I added `time.sleep(0.1)` between items. This is a "politely aggressive" way to process many items without hitting the Groq API rate limits.

#### 2. Async Job Queue (`services/job_queue.py`)
*   **Why**: Some reports take 30 seconds to generate. I don't want the user's browser to "hang."
*   **How**: When a user starts a report, I give them a `job_id` and run the AI in a **background thread**. The user's browser then "polls" (checks back) every few seconds to see if it's done.

---

### Phase 7: The Java Connection (`AiServiceClient.java`)
This is how the Java backend talks to the Python AI.

*   **`RestTemplate`**: The standard Java way to make HTTP calls.
*   **Timeouts**: I set a `setConnectTimeout(5000)` and `setReadTimeout(10000)`. This ensures that even if the AI service crashes, the Java backend stays responsive.

---

## Part 3: How to Rebuild it (Step-by-Step)

### 1. Set up the Python Service
```powershell
# Create the folder and virtual environment
mkdir ai-service; cd ai-service
python -m venv venv
.\venv\Scripts\activate

# Install the "Brain"
pip install flask groq chromadb redis sentence-transformers bleach flask-talisman flask-limiter
```

### 2. Configure the Secrets
Create a `.env` file and add your key:
`GROQ_API_KEY=your_key_here`

### 3. Seed the Knowledge Base
I've provided a script to ingest your initial documents so the RAG system has something to read.

### 4. Verify the Build
I use these specific commands to ensure every layer is working:

1.  **Check Connectivity**: `Invoke-RestMethod -Uri http://localhost:5000/health` (Should return "healthy").
2.  **Test Reasoning**: `Invoke-RestMethod -Uri http://localhost:5000/describe -Method Post -Body '{"text": "Data leak"}'` (Should return a structured JSON risk).
3.  **Test Knowledge**: `Invoke-RestMethod -Uri http://localhost:5000/query -Method Post -Body '{"text": "What is our password policy?"}'` (Should return an answer based on your documents).

---

## Glossary of Terms (For the "Noob" Guide)

*   **Microservice**: A small, independent piece of software that does one job well.
*   **LLM (Large Language Model)**: The "Brain" (Llama 3). It understands language.
*   **Endpoint**: A specific URL (like `/describe`) that a program can "call" to get a result.
*   **Vector**: A list of numbers that represent the "meaning" of a sentence.
*   **Blueprint**: A way to organize a Flask app into smaller, manageable sections.
*   **Sanitization**: Cleaning up user input so it can't "hack" or "trick" the system.
*   **SSE (Streaming)**: Sending data piece-by-piece as it's being thought of, like a typewriter.
