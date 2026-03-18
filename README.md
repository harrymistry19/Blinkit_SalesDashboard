# Invoice AI Assistant (Domain-Specific AI Agent)

Production-ready full-stack invoice extraction system built with FastAPI, React, Tailwind CSS, Groq, and SQLite.

## What it does

- Accepts **invoice-only** uploads: PDF, JPG, PNG.
- Uses a **modular OCR layer** that can be replaced with Tesseract later.
- Sends OCR text to **Groq** with a strict invoice-only prompt.
- Returns **strict structured JSON** with `null` for fields not found.
- Persists processing history in **SQLite**.
- Performs validation checks for missing invoice number and total mismatch.
- Displays a clean frontend UI with downloadable JSON reports.

## Architecture

```text
frontend (React + Tailwind + Vite)
   │
   ├── /upload  -> backend stores invoice file
   ├── /process -> OCR placeholder -> Groq -> normalization -> validation -> SQLite
   └── /history -> fetches prior processed invoices

backend (FastAPI + SQLAlchemy + SQLite)
```

## Backend structure

```text
backend/
  main.py
  routes/
    upload.py
    process.py
    history.py
  services/
    ai_processor.py
    ocr_service.py
    invoice_parser.py
  models/
    database.py
    history.py
    schemas.py
  utils/
    config.py
    constants.py
```

## Frontend structure

```text
frontend/
  src/
    components/
    pages/
    services/
```

## Groq system prompt used

```text
You are an expert invoice parser. You ONLY extract data from invoices. Do NOT answer anything outside invoice context. Return STRICT JSON only. Do NOT add explanations. Do NOT hallucinate. If value not found → return null.
```

## Sample Groq request body

```json
{
  "model": "llama-3.3-70b-versatile",
  "temperature": 0,
  "response_format": { "type": "json_object" },
  "messages": [
    {
      "role": "system",
      "content": "You are an expert invoice parser. You ONLY extract data from invoices. Do NOT answer anything outside invoice context. Return STRICT JSON only. Do NOT add explanations. Do NOT hallucinate. If value not found → return null."
    },
    {
      "role": "user",
      "content": "Extract invoice data only and respond with strict JSON.\n\nOCR TEXT:\n<invoice text here>"
    }
  ]
}
```

## Run locally

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # optional if you create one manually
uvicorn main:app --reload
```

Create `backend/.env` manually if needed:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Optional frontend env:

```env
VITE_API_URL=http://127.0.0.1:8000
```

## Notes on invoice variability

Different invoice templates can have very different layouts and text formatting. This app addresses that by:

- keeping OCR modular so extraction quality can improve independently,
- using a domain-specific Groq prompt restricted to invoice JSON extraction,
- normalizing outputs into a strict schema,
- flagging missing or inconsistent values instead of guessing.

## Important limitation

The included OCR service is a placeholder for modularity. To make extraction production-grade for real scanned invoices, replace `backend/services/ocr_service.py` with Tesseract, PaddleOCR, AWS Textract, Azure Document Intelligence, or a similar OCR engine.
