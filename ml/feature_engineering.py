from __future__ import annotations

import math
import re
from typing import Any

import numpy as np
import pandas as pd


def parse_indian_money(value: Any) -> float | np.nan:
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    if not text:
        return np.nan
    lower = text.lower().replace("₹", "").replace("rs.", "").replace("rs", "").strip()
    multiplier = 1.0
    if "cr" in lower or "crore" in lower:
        multiplier = 10_000_000.0
    elif "lac" in lower or "lakh" in lower:
        multiplier = 100_000.0
    match = re.search(r"[-+]?\d*\.?\d+", lower)
    return float(match.group()) * multiplier if match else np.nan


def parse_area_sqft(value: Any) -> float | np.nan:
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).lower().replace(",", "").strip()
    numbers = [float(x) for x in re.findall(r"\d+\.?\d*", text)]
    if not numbers:
        return np.nan
    if len(numbers) >= 2 and any(token in text for token in ["-", "to"]):
        return float(np.mean(numbers[:2]))
    return numbers[0]


def extract_bhk(value: Any) -> float | np.nan:
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"\d+", str(value))
    return float(match.group()) if match else np.nan


def clean_text(value: Any) -> str:
    if pd.isna(value):
        return "unknown"
    text = re.sub(r"\s+", " ", str(value).strip().lower())
    return text or "unknown"


def add_common_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "area" in out.columns:
        out["log_area"] = np.log1p(out["area"].clip(lower=0))
    if {"price", "area"}.issubset(out.columns):
        out["price_per_sqft"] = out["price"] / out["area"].replace(0, np.nan)
    if {"rent", "area"}.issubset(out.columns):
        out["rent_per_sqft"] = out["rent"] / out["area"].replace(0, np.nan)
    if "amenities" in out.columns:
        out["amenity_count"] = out["amenities"].fillna("").astype(str).str.count(",") + 1
    if "description" in out.columns:
        out["description_length"] = out["description"].fillna("").astype(str).str.len()
    if "review_scores_rating" in out.columns:
        out["rating_bucket"] = pd.cut(
            pd.to_numeric(out["review_scores_rating"], errors="coerce"),
            bins=[0, 60, 80, 90, 100],
            labels=["low", "medium", "high", "excellent"],
        ).astype(str)
    return out


def create_fraud_labels(df: pd.DataFrame) -> pd.Series:
    numeric = df.select_dtypes(include=[np.number]).copy()
    if numeric.empty:
        return pd.Series(np.zeros(len(df), dtype=int), index=df.index)
    risk = pd.Series(0.0, index=df.index)
    for col in numeric.columns:
        values = numeric[col].replace([np.inf, -np.inf], np.nan)
        z = (values - values.mean()) / (values.std() or 1)
        risk += z.abs().fillna(0)
    threshold = risk.quantile(0.95)
    return (risk >= threshold).astype(int)

