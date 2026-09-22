"""FastAPI app exposing POST /classify.

Run from inside server/ with:
    uvicorn main:app --reload
or:
    python main.py
"""

import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from config import FRONTEND_ORIGIN
from classifier import classify_image
from schemas import NYCWasteClassification

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/classify", response_model=NYCWasteClassification)
async def classify(file: UploadFile = File(...)) -> NYCWasteClassification:
    data = await file.read()
    try:
        pil_image = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image: {exc}") from exc

    try:
        return classify_image(pil_image)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Classification failed: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
