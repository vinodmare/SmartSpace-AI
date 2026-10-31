from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif, f_regression
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

from feature_engineering import create_fraud_labels
from preprocessing import DEFAULT_DATASETS, build_preprocessor, load_price_training_frame, save_eda_report

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "reports"
MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


def optional_model(import_path: str, class_name: str) -> type | None:
    try:
        module = __import__(import_path, fromlist=[class_name])
        return getattr(module, class_name)
    except Exception:
        return None


def regression_candidates() -> dict[str, Any]:
    candidates: dict[str, Any] = {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(random_state=42, n_estimators=250, n_jobs=-1),
    }
    xgb = optional_model("xgboost", "XGBRegressor")
    if xgb:
        candidates["xgboost"] = xgb(random_state=42, n_estimators=300, learning_rate=0.08, max_depth=6)
    lgbm = optional_model("lightgbm", "LGBMRegressor")
    if lgbm:
        candidates["lightgbm"] = lgbm(random_state=42, n_estimators=300, learning_rate=0.08, verbose=-1)
    cat = optional_model("catboost", "CatBoostRegressor")
    if cat:
        candidates["catboost"] = cat(random_state=42, iterations=300, learning_rate=0.08, verbose=False)
    return candidates


def classification_candidates() -> dict[str, Any]:
    candidates: dict[str, Any] = {
        "logistic_regression": LogisticRegression(max_iter=1500, class_weight="balanced"),
        "random_forest": RandomForestClassifier(random_state=42, n_estimators=250, class_weight="balanced", n_jobs=-1),
    }
    xgb = optional_model("xgboost", "XGBClassifier")
    if xgb:
        candidates["xgboost"] = xgb(
            random_state=42,
            n_estimators=250,
            learning_rate=0.08,
            max_depth=5,
            eval_metric="logloss",
        )
    return candidates


def regression_metrics(model: Pipeline, x: pd.DataFrame, y: pd.Series) -> dict[str, float]:
    pred = model.predict(x)
    return {
        "mae": float(mean_absolute_error(y, pred)),
        "rmse": float(np.sqrt(mean_squared_error(y, pred))),
        "r2": float(r2_score(y, pred)),
    }


def classification_metrics(model: Pipeline, x: pd.DataFrame, y: pd.Series) -> dict[str, float]:
    pred = model.predict(x)
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(x)[:, 1]
    else:
        proba = pred
    return {
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y, proba)) if len(set(y)) > 1 else 0.0,
    }


def tune_random_forest_regressor(base_pipeline: Pipeline, x_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    params = {
        "model__n_estimators": [150, 250, 350],
        "model__max_depth": [None, 8, 14, 22],
        "model__min_samples_split": [2, 5, 10],
    }
    search = RandomizedSearchCV(
        base_pipeline,
        params,
        n_iter=6,
        cv=3,
        scoring="neg_mean_absolute_error",
        random_state=42,
        n_jobs=-1,
    )
    search.fit(x_train, y_train)
    return search.best_estimator_


def train_price_model(df: pd.DataFrame) -> dict:
    y = df["target_price"].astype(float)
    x = df.drop(columns=["target_price"])
    x_train_full, x_test, y_train_full, y_test = train_test_split(x, y, test_size=0.15, random_state=42)
    x_train, x_val, y_train, y_val = train_test_split(x_train_full, y_train_full, test_size=0.1765, random_state=42)

    metrics: dict[str, dict] = {}
    best_name = ""
    best_pipeline: Pipeline | None = None
    best_mae = float("inf")

    for name, model in regression_candidates().items():
        preprocessor, _, _ = build_preprocessor(x_train.assign(target_price=y_train))
        pipeline = Pipeline(
            steps=[
                ("preprocess", preprocessor),
                ("feature_selection", SelectPercentile(score_func=f_regression, percentile=60)),
                ("model", model),
            ]
        )
        if name == "random_forest":
            pipeline = tune_random_forest_regressor(pipeline, x_train, y_train)
        else:
            pipeline.fit(x_train, y_train)

        cv = cross_val_score(pipeline, x_train_full, y_train_full, scoring="neg_mean_absolute_error", cv=3, n_jobs=-1)
        val_metrics = regression_metrics(pipeline, x_val, y_val)
        test_metrics = regression_metrics(pipeline, x_test, y_test)
        metrics[name] = {
            "validation": val_metrics,
            "test": test_metrics,
            "cv_mae_mean": float(-cv.mean()),
            "cv_mae_std": float(cv.std()),
        }
        if val_metrics["mae"] < best_mae:
            best_mae = val_metrics["mae"]
            best_name = name
            best_pipeline = pipeline

    if best_pipeline is None:
        raise RuntimeError("No price model could be trained.")

    joblib.dump(best_pipeline, MODEL_DIR / "price_prediction_model.pkl")
    joblib.dump(best_pipeline.named_steps["preprocess"], MODEL_DIR / "preprocessing_pipeline.pkl")
    save_feature_importance(best_pipeline, REPORT_DIR / "price_feature_importance.png")
    return {"best_model": best_name, "metrics": metrics}


def train_fraud_model(df: pd.DataFrame) -> dict:
    fraud_df = df.drop(columns=["target_price"], errors="ignore").copy()
    fraud_df["is_fraud"] = create_fraud_labels(fraud_df)
    y = fraud_df["is_fraud"].astype(int)
    x = fraud_df.drop(columns=["is_fraud"])
    x_train_full, x_test, y_train_full, y_test = train_test_split(x, y, test_size=0.15, stratify=y, random_state=42)
    x_train, x_val, y_train, y_val = train_test_split(x_train_full, y_train_full, test_size=0.1765, stratify=y_train_full, random_state=42)

    metrics: dict[str, dict] = {}
    best_name = ""
    best_pipeline: Pipeline | None = None
    best_f1 = -1.0

    for name, model in classification_candidates().items():
        preprocessor, _, _ = build_preprocessor(x_train.assign(target_price=0), target="target_price")
        pipeline = Pipeline(
            steps=[
                ("preprocess", preprocessor),
                ("feature_selection", SelectPercentile(score_func=f_classif, percentile=60)),
                ("model", model),
            ]
        )
        pipeline.fit(x_train, y_train)
        cv = cross_val_score(pipeline, x_train_full, y_train_full, scoring="f1", cv=3, n_jobs=-1)
        val_metrics = classification_metrics(pipeline, x_val, y_val)
        test_metrics = classification_metrics(pipeline, x_test, y_test)
        metrics[name] = {
            "validation": val_metrics,
            "test": test_metrics,
            "cv_f1_mean": float(cv.mean()),
            "cv_f1_std": float(cv.std()),
        }
        if val_metrics["f1"] > best_f1:
            best_f1 = val_metrics["f1"]
            best_name = name
            best_pipeline = pipeline

    if best_pipeline is None:
        raise RuntimeError("No fraud model could be trained.")

    joblib.dump(best_pipeline, MODEL_DIR / "fraud_detection_model.pkl")
    return {"best_model": best_name, "metrics": metrics, "label_strategy": "top_5_percent_anomaly_risk"}


def train_recommendation_model(df: pd.DataFrame) -> dict:
    rec = df.copy()
    rec["space_id"] = np.arange(len(rec)).astype(str)
    text_cols = ["city", "locality", "property_type", "furnishing", "amenities", "description", "target_type"]
    rec["recommendation_text"] = rec[text_cols].fillna("").astype(str).agg(" ".join, axis=1)
    vectorizer = TfidfVectorizer(max_features=12000, ngram_range=(1, 2), min_df=2)
    matrix = vectorizer.fit_transform(rec["recommendation_text"])
    payload = {
        "type": "content_based",
        "vectorizer": vectorizer,
        "matrix": matrix,
        "items": rec[
            ["space_id", "city", "locality", "property_type", "target_price", "area", "beds", "bathrooms", "recommendation_text"]
        ].reset_index(drop=True),
        "future_collaborative_filtering": {
            "required_events": ["view", "click", "favorite", "booking_start", "booking_complete"],
            "planned_model": "implicit matrix factorization or neural collaborative filtering",
        },
    }
    joblib.dump(payload, MODEL_DIR / "recommendation_model.pkl")

    sample_scores = cosine_similarity(matrix[:1], matrix).flatten()
    return {"items": int(len(rec)), "features": int(matrix.shape[1]), "sample_top_score": float(sample_scores.max())}


def save_feature_importance(model: Pipeline, path: Path) -> None:
    estimator = model.named_steps["model"]
    if not hasattr(estimator, "feature_importances_"):
        return
    importances = np.asarray(estimator.feature_importances_)
    top = np.argsort(importances)[-25:]
    plt.figure(figsize=(10, 7))
    plt.barh(range(len(top)), importances[top])
    plt.yticks(range(len(top)), [f"feature_{i}" for i in top])
    plt.title("Price Model Feature Importance")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def main() -> None:
    save_eda_report(DEFAULT_DATASETS, REPORT_DIR / "eda_summary.json")
    df = load_price_training_frame(DEFAULT_DATASETS)
    df.to_csv(REPORT_DIR / "clean_training_frame_sample.csv", index=False)

    metrics = {
        "rows_after_cleaning": int(len(df)),
        "columns_after_feature_engineering": list(df.columns),
        "price_prediction": train_price_model(df),
        "fraud_detection": train_fraud_model(df),
        "recommendation": train_recommendation_model(df),
    }
    (REPORT_DIR / "model_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2)[:12000])


if __name__ == "__main__":
    main()
