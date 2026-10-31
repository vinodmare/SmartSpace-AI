from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline

from preprocessing import DEFAULT_DATASETS, build_preprocessor, load_price_training_frame, save_eda_report

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models_streamlit"
REPORT_DIR = BASE_DIR / "reports_streamlit"
MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

TARGET = "target_price"


def candidate_models() -> dict[str, Any]:
    return {
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(
            n_estimators=250,
            max_depth=18,
            min_samples_split=4,
            random_state=42,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=250,
            learning_rate=0.06,
            max_depth=4,
            random_state=42,
        ),
    }


def metrics(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


def build_pipeline(df: pd.DataFrame, estimator: Any) -> Pipeline:
    preprocessor, _, _ = build_preprocessor(df, target=TARGET)
    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", estimator),
        ]
    )


def train_and_select_best(paths: list[str] | None = None) -> dict[str, Any]:
    paths = paths or DEFAULT_DATASETS
    save_eda_report(paths, REPORT_DIR / "eda_summary.json")

    df = load_price_training_frame(paths)
    x = df.drop(columns=[TARGET])
    y = df[TARGET].astype(float)

    x_train_val, x_test, y_train_val, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    x_train, x_valid, y_train, y_valid = train_test_split(
        x_train_val, y_train_val, test_size=0.2, random_state=42
    )

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    model_results: dict[str, Any] = {}
    trained: dict[str, Pipeline] = {}

    for name, estimator in candidate_models().items():
        pipeline = build_pipeline(df, estimator)
        cv_scores = cross_validate(
            pipeline,
            x_train_val,
            y_train_val,
            scoring={
                "mae": "neg_mean_absolute_error",
                "rmse": "neg_root_mean_squared_error",
                "r2": "r2",
            },
            cv=cv,
            n_jobs=-1,
            return_train_score=True,
        )
        pipeline.fit(x_train, y_train)
        valid_pred = pipeline.predict(x_valid)
        test_pred = pipeline.predict(x_test)

        model_results[name] = {
            "cv_mae": float(-cv_scores["test_mae"].mean()),
            "cv_rmse": float(-cv_scores["test_rmse"].mean()),
            "cv_r2": float(cv_scores["test_r2"].mean()),
            "train_cv_rmse": float(-cv_scores["train_rmse"].mean()),
            "validation": metrics(y_valid, valid_pred),
            "test": metrics(y_test, test_pred),
            "overfit_gap_rmse": float(
                (-cv_scores["test_rmse"].mean()) - (-cv_scores["train_rmse"].mean())
            ),
        }
        trained[name] = pipeline

    best_name = min(model_results, key=lambda n: model_results[n]["validation"]["rmse"])
    best_model = trained[best_name]

    joblib.dump(best_model, MODEL_DIR / "model.pkl")
    joblib.dump(best_model.named_steps["preprocess"], MODEL_DIR / "preprocessing_pipeline.pkl")
    joblib.dump(
        {
            "best_model_name": best_name,
            "model_results": model_results,
            "features": list(x.columns),
            "target": TARGET,
        },
        MODEL_DIR / "training_metadata.pkl",
    )

    df.head(5000).to_csv(REPORT_DIR / "cleaned_training_sample.csv", index=False)
    explain_model(best_model, x_valid, y_valid, best_name)

    report = {
        "dataset_rows_after_cleaning": int(len(df)),
        "dataset_columns_after_cleaning": list(df.columns),
        "best_model": best_name,
        "selection_reason": "Lowest validation RMSE after 5-fold cross-validation and holdout validation.",
        "models": model_results,
        "artifacts": {
            "model": str(MODEL_DIR / "model.pkl"),
            "preprocessing_pipeline": str(MODEL_DIR / "preprocessing_pipeline.pkl"),
            "metadata": str(MODEL_DIR / "training_metadata.pkl"),
            "explainability_plot": str(REPORT_DIR / "explainable_ai_permutation_importance.png"),
        },
    }
    (REPORT_DIR / "training_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def explain_model(model: Pipeline, x_valid: pd.DataFrame, y_valid: pd.Series, model_name: str) -> None:
    sample_size = min(600, len(x_valid))
    x_sample = x_valid.sample(sample_size, random_state=42) if len(x_valid) > sample_size else x_valid
    y_sample = y_valid.loc[x_sample.index]

    importance = permutation_importance(
        model,
        x_sample,
        y_sample,
        scoring="neg_root_mean_squared_error",
        n_repeats=5,
        random_state=42,
        n_jobs=-1,
    )
    order = np.argsort(importance.importances_mean)[-15:]

    plt.figure(figsize=(10, 7))
    plt.barh(np.array(x_sample.columns)[order], importance.importances_mean[order])
    plt.title(f"Explainable AI: permutation importance for {model_name}")
    plt.xlabel("Increase in prediction error when feature is shuffled")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "explainable_ai_permutation_importance.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    print(json.dumps(train_and_select_best(), indent=2))
