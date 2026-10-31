from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

MODEL_DIR = Path(__file__).resolve().parent / "models"


def load_model(filename: str) -> Any:
    path = MODEL_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")
    return joblib.load(path)


def load_price_model() -> Any:
    return load_model("price_prediction_model.pkl")


def load_fraud_model() -> Any:
    return load_model("fraud_detection_model.pkl")


def load_recommendation_model() -> Any:
    return load_model("recommendation_model.pkl")


def price_input_to_frame(payload: dict) -> Any:
    import pandas as pd

    defaults = {
        "source_file": "api",
        "city": "bangalore",
        "locality": "unknown",
        "property_type": "rental_space",
        "furnishing": "unknown",
        "amenities": "",
        "description": "",
        "area": None,
        "beds": None,
        "bathrooms": None,
        "balconies": None,
        "target_type": "monthly_rent",
        "log_area": None,
        "amenity_count": None,
        "description_length": None,
    }
    defaults.update(payload)
    if defaults["log_area"] is None and defaults.get("area") is not None:
        import numpy as np

        defaults["log_area"] = float(np.log1p(max(float(defaults["area"]), 0)))
    if defaults["amenity_count"] is None:
        defaults["amenity_count"] = len(str(defaults.get("amenities", "")).split(",")) if defaults.get("amenities") else 0
    if defaults["description_length"] is None:
        defaults["description_length"] = len(str(defaults.get("description", "")))
    return pd.DataFrame([defaults])
