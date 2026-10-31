# SmartSpace AI ML Pipeline

This module trains ML models without changing the existing frontend.

## Models

- Rental Price Prediction
- Fraud Detection
- Content-Based Recommendation

## Jupyter Notebook + Streamlit Workflow

This is the recommended no-API workflow.

```powershell
cd ml
python -m pip install -r requirements.txt
jupyter notebook notebooks/SmartSpace_AI_Jupyter_Workflow.ipynb
```

To use the Streamlit UI:

```powershell
cd ml
streamlit run streamlit_app.py
```

The Streamlit UI can train models, show cross-validation metrics, make rental price predictions, and display Explainable AI feature importance.

## Script Workflow

```powershell
cd ml
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python train.py
python evaluate.py
python predict.py --task price --json "{\"city\":\"Bangalore\",\"locality\":\"Whitefield\",\"area\":1200,\"beds\":2,\"bathrooms\":2,\"furnishing\":\"Semi-Furnished\",\"property_type\":\"Flat\"}"
python streamlit_train.py
```

## Outputs

```text
models/price_prediction_model.pkl
models/fraud_detection_model.pkl
models/recommendation_model.pkl
models/preprocessing_pipeline.pkl
reports/eda_summary.json
reports/model_metrics.json
reports/price_feature_importance.png
models_streamlit/model.pkl
models_streamlit/preprocessing_pipeline.pkl
models_streamlit/training_metadata.pkl
reports_streamlit/training_report.json
reports_streamlit/explainable_ai_permutation_importance.png
```

## Notes

- The no-API Streamlit workflow compares exactly 3 models: Ridge Regression, Random Forest, and Gradient Boosting.
- Model selection uses 5-fold cross-validation plus validation/test splits.
- Explainable AI uses permutation importance.
- The older `api.py` file is still present from the FastAPI workflow, but it is not needed for this Streamlit workflow.
