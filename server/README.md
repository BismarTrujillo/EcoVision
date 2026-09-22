# EcoVision NYC — Server

FastAPI backend that classifies items against NYC DSNY/311 curbside recycling rules
(article KA-02013). Accepts an uploaded image and sends it to Gemini for structured
classification.

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your Gemini API key:

```bash
cp .env.example .env
```

```
GEMINI_API_KEY=your-api-key-here
FRONTEND_ORIGIN=http://localhost:3000
```

If `GEMINI_API_KEY` is already set in your shell (e.g. via `setx` or `$env:`), that
takes precedence over `.env`.

## Run

From inside `server/`:

```bash
uvicorn main:app --reload
```

or:

```bash
python main.py
```

Both serve on `http://localhost:8000`.

## Test

```bash
curl http://localhost:8000/health
curl -F "file=@some_image.jpg" http://localhost:8000/classify
```

Syntax-check without running (no API key needed):

```bash
python -m py_compile *.py
```

There is no test suite or linter configured.

## Architecture

- `config.py` — loads `.env`, fails fast if `GEMINI_API_KEY` is missing, exposes `FRONTEND_ORIGIN`.
- `schemas.py` — `NYCWasteClassification`, the structured output schema Gemini is forced to
  return and the exact JSON shape returned by `POST /classify`.
- `nyc_rules.py` — the DSNY/311 bin-routing rules given to Gemini as a system instruction. This
  is the business logic; changes to sorting rules go here.
- `classifier.py` — sends an image to Gemini, validates the response, stamps `captured_at` from
  the local clock, and writes the result to `classified_item.json` as a debug artifact.
- `main.py` — the FastAPI app: CORS, `GET /health`, and `POST /classify` (multipart image
  upload → 400 on invalid image, 502 on classification failure).
