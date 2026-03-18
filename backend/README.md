# Backend

FastAPI service for the Invoice AI Assistant. It is intentionally restricted to invoice PDF/JPG/PNG processing only.

## Environment

Create `backend/.env` with:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

## Run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
