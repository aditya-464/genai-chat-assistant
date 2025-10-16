# GenAI Chat Assistant (minimal)

## Requirements
- Python 3.10+
- Node 18+ / npm
- OpenAI API key

## Setup Backend
1. cd backend
2. python -m venv venv
3. source venv/bin/activate   (Windows: venv\Scripts\activate)
4. pip install -r requirements.txt
5. export OPENAI_API_KEY="sk-..."   (Windows: set OPENAI_API_KEY=...)
6. python app.py
   - Backend runs at http://0.0.0.0:7860

## Setup Frontend
1. cd frontend
2. npm install
3. npm run start
   - Frontend runs at http://localhost:5173 (vite default)

## Usage
- Open frontend, upload a PDF or TXT via the Upload control.
- Ask questions in the chat: the assistant will use RAG (search + LLM) to answer.

## Notes & Improvements
- This is a minimal demo. For production:
  - Persist vectorstore in cloud or DB.
  - Add authentication, rate-limiting, concurrency handling.
  - Use background tasks for indexing big docs.
  - Use local LLMs for sensitive data (e.g., Llama 3 via Ollama).
