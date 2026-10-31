from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import (
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from feature_engineering import create_fraud_labels
from preprocessing import DEFAULT_DATASETS, load_price_training_frame

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def evaluate_price() -> dict:
    df = load_price_training_frame(DEFAULT_DATASETS)
    y = df["target_price"].astype(float)
    x = df.drop(columns=["target_price"])
    _, x_test, _, y_test = train_test_split(x, y, test_size=0.15, random_state=42)
    model = joblib.load(MODEL_DIR / "price_prediction_model.pkl")
    pred = model.predict(x_test)
    return {
        "mae": float(mean_absolute_error(y_test, pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
        "r2": float(r2_score(y_test, pred)),
        "test_rows": int(len(x_test)),
    }


def evaluate_fraud() -> dict:
    df = load_price_training_frame(DEFAULT_DATASETS).drop(columns=["target_price"], errors="ignore")
    y = create_fraud_labels(df)
    x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.15, stratify=y, random_state=42)
    model = joblib.load(MODEL_DIR / "fraud_detection_model.pkl")
    pred = model.predict(x_test)
    proba = model.predict_proba(x_test)[:, 1] if hasattr(model, "predict_proba") else pred
    return {
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, proba)) if len(set(y_test)) > 1 else 0.0,
        "test_rows": int(len(x_test)),
        "train_rows": int(len(x_train)),
    }


def evaluate_recommendation() -> dict:
    model = joblib.load(MODEL_DIR / "recommendation_model.pkl")
    matrix = model["matrix"]
    return {
        "items": int(matrix.shape[0]),
        "tfidf_features": int(matrix.shape[1]),
        "architecture": model["type"],
    }


def main() -> None:
    result = {
        "price_prediction": evaluate_price(),
        "fraud_detection": evaluate_fraud(),
        "recommendation": evaluate_recommendation(),
    }
    (REPORT_DIR / "evaluation_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
