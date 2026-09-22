# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

EcoVision NYC is a full-stack app that classifies items against NYC DSNY/311 curbside recycling
rules (article KA-02013): a browser captures a photo (webcam), sends it to the backend, which sends
it to Gemini for structured classification, and the frontend renders the result (bin color, recycle/
compost/trash category, prep instructions, rough weight/CO2 estimates).

- `server/` — FastAPI backend. See `server/README.md` for setup/run/architecture.
- `client/` — Next.js frontend. See `client/README.md` for setup/run.

## Running both halves

Backend (from `server/`):

```bash
pip install -r requirements.txt
# copy .env.example to .env and fill in GEMINI_API_KEY, or set it in your shell
uvicorn main:app --reload
```

Frontend (from `client/`, in a second terminal):

```bash
npm install
npm run dev
```

Frontend runs on `http://localhost:3000` and calls the backend at `http://127.0.0.1:8000` by default
(override with `NEXT_PUBLIC_API_BASE_URL`).

## Architecture

### Backend (`server/`)

- `config.py` — loads `.env`, fails fast if `GEMINI_API_KEY` is missing, exposes `FRONTEND_ORIGIN`
  (used for CORS).
- `schemas.py` — `NYCWasteClassification`, the structured output schema Gemini is forced to return.
  This is also the exact JSON shape returned by `POST /classify`.
- `nyc_rules.py` — `SYSTEM_INSTRUCTION`, encoding the actual NYC bin-routing rules (blue/green/brown/
  black/special disposal categories and their edge cases, e.g. plastic film and styrofoam are trash
  despite being plastic). This prompt *is* the business logic — changes to sorting rules go here.
- `classifier.py` — `classify_image()` sends a PIL image to `gemini-3.5-flash-lite` with the schema +
  system instruction, stamps `captured_at` from the local clock (not Gemini), and writes the result to
  `classified_item.json` as a local debug artifact. Lets exceptions propagate — `main.py` turns
  API/network/validation failures into HTTP error responses.
- `main.py` — the FastAPI app: CORS (origin from `FRONTEND_ORIGIN`), `GET /health`, and
  `POST /classify` (multipart image upload via `UploadFile` → decodes with Pillow → 400 on invalid
  image, 502 on classification failure).

There is no test suite or linter configured for the backend.

### Frontend (`client/`)

Next.js (App Router) + React 19 + Tailwind v4. `app/page.tsx` holds the scan/dashboard state and
calls `POST /classify` with the captured frame. Components live in `app/components/`:
`Scanner` (webcam capture), `ScanResultCard` (latest classification), `DashboardStats` (stats, chart,
recent-history preview with a "View All" button), `HistoryModal` (full scan history), `Header`.
Shared types are in `app/types/index.ts` — `VisionAPIResponse` mirrors the backend's
`NYCWasteClassification` schema exactly; keep the two in sync if the schema changes.
