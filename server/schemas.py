"""Pydantic schema for waste classification results.

This is also the exact JSON shape returned by POST /classify.
"""

from pydantic import BaseModel


class NYCWasteClassification(BaseModel):
    item_name: str
    material_type: str
    nyc_stream_category: str
    bin_color: str
    is_recyclable: bool
    preparation_instructions: list[str]
    nyc_rule_notes: str
    estimated_weight_grams: float
    estimated_co2_grams: float
    captured_at: str
