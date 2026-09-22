# EcoVision NYC

An AI-powered waste classifier for NYC curbside collection. Point your webcam at an item, and it
tells you whether it's Recycle, Compost, or Trash — including which bin color, prep instructions,
and rough CO2 impact — based on NYC DSNY/311 rules (article KA-02013).

Built at CTP Hacks 2026.

## How it works

1. The **client** (Next.js) captures a photo from your browser's webcam.
2. It's sent to the **server** (FastAPI), which forwards the image to Gemini with a system prompt
   encoding NYC's actual bin-routing rules.
3. Gemini returns a structured classification (item, material, bin color, recyclable/not,
   instructions, estimated weight/CO2), which the client renders on a dashboard and logs to a
   scannable history.

## Tech stack

- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS v4, `react-webcam`, `lucide-react`
- **Backend:** FastAPI, Pillow, Pydantic, `google-genai` (Gemini)

## Getting started

Backend:

```bash
cd server
pip install -r requirements.txt
# copy .env.example to .env and add your GEMINI_API_KEY
uvicorn main:app --reload
```

Frontend (in a second terminal):

```bash
cd client
npm install
npm run dev
```

Open `http://localhost:3000`. See `server/README.md` and `client/README.md` for more detail on each
half.
