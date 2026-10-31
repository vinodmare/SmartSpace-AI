from __future__ import annotations

import argparse
import json

from sklearn.metrics.pairwise import cosine_similarity

from model_loader import load_fraud_model, load_price_model, load_recommendation_model, price_input_to_frame


def predict_price(payload: dict) -> dict:
    model = load_price_model()
    frame = price_input_to_frame(payload)
    prediction = float(model.predict(frame)[0])
    return {"predicted_price_inr": round(prediction, 2)}


def detect_fraud(payload: dict) -> dict:
    model = load_fraud_model()
    frame = price_input_to_frame(payload)
    prediction = int(model.predict(frame)[0])
    probability = float(model.predict_proba(frame)[0][1]) if hasattr(model, "predict_proba") else float(prediction)
    return {
        "is_fraud": bool(prediction),
        "fraud_probability": round(probability, 4),
        "risk_level": "high" if probability >= 0.7 else "medium" if probability >= 0.35 else "low",
    }


def recommend(payload: dict, top_k: int = 5) -> dict:
    model = load_recommendation_model()
    query = " ".join(
        str(payload.get(key, ""))
        for key in ["city", "locality", "property_type", "amenities", "description", "budget_inr"]
    )
    query_vec = model["vectorizer"].transform([query])
    scores = cosine_similarity(query_vec, model["matrix"]).flatten()
    top_idx = scores.argsort()[-top_k:][::-1]
    items = model["items"].iloc[top_idx].copy()
    items["score"] = scores[top_idx]
    return {"recommendations": items.to_dict(orient="records")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["price", "fraud", "recommend"], required=True)
    parser.add_argument("--json", required=True, help="JSON payload")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
    payload = json.loads(args.json)
    if args.task == "price":
        result = predict_price(payload)
    elif args.task == "fraud":
        result = detect_fraud(payload)
    else:
        result = recommend(payload, args.top_k)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

