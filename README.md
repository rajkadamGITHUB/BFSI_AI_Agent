# BFSI AI Service Agent

A FastAPI demonstration assistant for common banking, payments, credit, insurance, and investing education questions. It combines a curated FAQ, a question catalog, guarded LLM responses, and sample account tools.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` to enable generated answers. The API still starts without them; `/health` reports the provider as unconfigured and chat uses a safe fallback. Then run:

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. API endpoints are `/health`, `/questions`, and `POST /chat` with `{"question_id":"loan_documents","history":[]}`. Chat accepts only catalog question IDs; add supported questions in `data/questions.json` and keep factual source material in `data/banking_faq.txt`.

## Data and safety

The FAQ intentionally avoids institution-specific rates, fees, eligibility promises, and legal coverage claims. Keep those facts in an approved, maintained source before publishing them. The account, card, and transaction tools in `app/tools.py` return hard-coded demonstration data and must be replaced with authenticated, authorized integrations before any real customer use. Do not send credentials, PINs, or one-time codes to the assistant.

The current FAQ retriever is a small deterministic keyword search suited to this demo corpus. For larger knowledge collections, replace it with a managed search/vector index while retaining source metadata, access controls, and freshness checks. Add authentication, rate limiting, audit policy, monitoring, and provider-backed integration checks before production deployment.
