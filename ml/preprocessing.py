from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler

from feature_engineering import add_common_features, clean_text, extract_bhk, parse_area_sqft, parse_indian_money


DEFAULT_DATASETS = [
    r"C:\Users\vinod\Downloads\RS_Session_260_AU_1168_A_to_C.csv",
    r"C:\Users\vinod\Downloads\Table_7_10.csv",
    r"C:\Users\vinod\Downloads\export.geojson",
    r"C:\Users\vinod\Downloads\house_prices_bangalore.csv",
    r"C:\Users\vinod\Downloads\Fleet_Nov_2021.csv",
    r"C:\Users\vinod\Downloads\Fleet_Jan_2022_0.csv",
    r"C:\Users\vinod\Downloads\Fleet_Dec_2021_0.csv",
    r"C:\Users\vinod\Downloads\bengaluru_house_prices (1).csv",
    r"C:\Users\vinod\Downloads\5c2f62fe-5afa-4119-a499-fec9d604d5bd.csv",
    r"C:\Users\vinod\Downloads\Airbnb_Data.csv.zip",
    r"C:\Users\vinod\Downloads\bengaluru_house_prices.csv",
    r"C:\Users\vinod\Downloads\data.csv",
    r"C:\Users\vinod\Downloads\Indian_Real_Estate_Clean_Data.csv.zip",
    r"C:\Users\vinod\Downloads\Real Estate Data V21.csv.zip",
]


def read_dataset(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() == ".geojson":
        df = pd.read_json(path)
        df["source_file"] = path.name
        return df
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            member = next(name for name in archive.namelist() if name.lower().endswith(".csv"))
            with archive.open(member) as handle:
                df = pd.read_csv(handle, low_memory=False)
                df["source_file"] = path.name
                df["source_member"] = member
                return df
    df = pd.read_csv(path, low_memory=False)
    df["source_file"] = path.name
    return df


def analyze_datasets(paths: Iterable[str | Path]) -> dict:
    reports = {}
    for path in paths:
        try:
            df = read_dataset(path)
            reports[Path(path).name] = {
                "rows": int(len(df)),
                "columns": list(map(str, df.columns)),
                "missing": df.isna().sum().sort_values(ascending=False).head(25).astype(int).to_dict(),
                "duplicates": int(df.duplicated().sum()),
                "numeric_columns": list(map(str, df.select_dtypes(include=[np.number]).columns)),
                "categorical_columns": list(map(str, df.select_dtypes(exclude=[np.number]).columns)),
            }
        except Exception as exc:
            reports[Path(path).name] = {"error": repr(exc)}
    return reports


def normalize_price_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cols = {c.lower().strip(): c for c in df.columns}
    out = pd.DataFrame(index=df.index)
    out["source_file"] = df.get("source_file", "unknown")
    out["city"] = df.get(cols.get("city", ""), "Bangalore").map(clean_text) if cols.get("city") else "bangalore"
    out["locality"] = (
        df.get(cols.get("locality", ""), df.get(cols.get("location", ""), "unknown")).map(clean_text)
        if cols.get("locality") or cols.get("location")
        else "unknown"
    )
    out["property_type"] = (
        df.get(cols.get("property_type", ""), df.get(cols.get("area_type", ""), "rental_space")).map(clean_text)
        if cols.get("property_type") or cols.get("area_type")
        else "rental_space"
    )
    out["furnishing"] = df.get(cols.get("furnishing", ""), "unknown").map(clean_text) if cols.get("furnishing") else "unknown"
    out["amenities"] = df.get(cols.get("amenities", ""), "").astype(str) if cols.get("amenities") else ""
    out["description"] = df.get(cols.get("description", ""), "").astype(str) if cols.get("description") else ""

    area_col = cols.get("area") or cols.get("total_area(sqft)") or cols.get("total_area") or cols.get("total_sqft")
    out["area"] = df[area_col].map(parse_area_sqft) if area_col else np.nan

    bhk_col = cols.get("bhk") or cols.get("beds") or cols.get("bedrooms") or cols.get("size")
    out["beds"] = df[bhk_col].map(extract_bhk) if bhk_col else np.nan

    bath_col = cols.get("bath") or cols.get("bathrooms") or cols.get("baths")
    out["bathrooms"] = pd.to_numeric(df[bath_col], errors="coerce") if bath_col else np.nan

    balcony_col = cols.get("balcony") or cols.get("balconies")
    if balcony_col:
        out["balconies"] = df[balcony_col].replace({"Yes": 1, "No": 0, "yes": 1, "no": 0}).map(parse_area_sqft)
    else:
        out["balconies"] = np.nan

    if cols.get("rent"):
        out["target_price"] = pd.to_numeric(df[cols["rent"]], errors="coerce")
        out["target_type"] = "monthly_rent"
    elif cols.get("price"):
        out["target_price"] = df[cols["price"]].map(parse_indian_money)
        out["target_type"] = "sale_price"
    elif cols.get("log_price"):
        out["target_price"] = np.exp(pd.to_numeric(df[cols["log_price"]], errors="coerce")) * 83
        out["target_type"] = "nightly_airbnb_price_inr"
    else:
        out["target_price"] = np.nan
        out["target_type"] = "unknown"

    out = add_common_features(out)
    return out


def load_price_training_frame(paths: Iterable[str | Path]) -> pd.DataFrame:
    frames = []
    for path in paths:
        try:
            normalized = normalize_price_dataset(read_dataset(path))
            if normalized["target_price"].notna().sum() >= 50:
                frames.append(normalized)
        except Exception:
            continue
    if not frames:
        raise RuntimeError("No usable price datasets found.")
    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates()
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["target_price"])
    df = df[df["target_price"] > 0]
    for col in ["target_price", "area"]:
        if col in df.columns:
            q1, q3 = df[col].quantile([0.01, 0.99])
            df = df[df[col].between(q1, q3) | df[col].isna()]
    return df.reset_index(drop=True)


def build_preprocessor(df: pd.DataFrame, target: str = "target_price") -> tuple[ColumnTransformer, list[str], list[str]]:
    feature_df = df.drop(columns=[target], errors="ignore")
    high_cardinality = [c for c in feature_df.columns if feature_df[c].nunique(dropna=True) > 500]
    feature_df = feature_df.drop(columns=high_cardinality, errors="ignore")
    numeric = list(feature_df.select_dtypes(include=[np.number]).columns)
    categorical = [c for c in feature_df.columns if c not in numeric]
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", min_frequency=5)),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric),
            ("cat", categorical_pipeline, categorical),
        ],
        remainder="drop",
    )
    return preprocessor, numeric, categorical


def save_eda_report(paths: Iterable[str | Path], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(analyze_datasets(paths), indent=2), encoding="utf-8")
