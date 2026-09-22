"""Sends an image to Gemini and returns a validated NYC waste classification."""

from datetime import datetime

from google import genai
from google.genai import types
from PIL import Image

from nyc_rules import SYSTEM_INSTRUCTION
from schemas import NYCWasteClassification

client = genai.Client()


def classify_image(pil_image: Image.Image) -> NYCWasteClassification:
    """Send a PIL image to Gemini and return a validated classification.

    Raises on API/network/validation failure - the caller (the /classify
    endpoint) is responsible for turning that into an HTTP error response.
    """
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[pil_image],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=NYCWasteClassification,
            # This is pure structured extraction, not reasoning - minimize
            # the model's internal thinking pass to cut round-trip latency.
            # thinking_budget=0 is rejected by some Gemini models (400), so
            # use the lowest supported thinking_level instead.
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )

    result = response.parsed
    if result is None:
        result = NYCWasteClassification.model_validate_json(response.text)

    # captured_at comes from the local clock, not Gemini's guess.
    result = result.model_copy(update={"captured_at": datetime.now().isoformat()})

    payload = result.model_dump_json(indent=2)
    print("\n" + payload + "\n")

    with open("classified_item.json", "w", encoding="utf-8") as f:
        f.write(payload)

    return result
