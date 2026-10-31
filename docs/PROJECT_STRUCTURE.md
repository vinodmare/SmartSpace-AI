# Project Structure

## Frontend

Path:

```text
frontend/
```

Contains the completed Next.js UI:

- `app/` routes and pages
- `components/` reusable UI components
- `lib/` utilities and mock data
- `providers/` app providers
- Tailwind, TypeScript, and Next configuration files

## Backend

Path:

```text
backend/
```

Contains the FastAPI backend:

- `app/` API source code
- `alembic/` database migrations
- `tests/` backend tests
- `requirements.txt` Python dependencies
- `Dockerfile` backend container setup
- `.env.example` environment variable template

## Machine Learning

Path:

```text
ml/
```

Contains the ML workflow:

- `streamlit_app.py` clean Streamlit UI
- `streamlit_train.py` Streamlit/notebook training workflow
- `train.py`, `evaluate.py`, `predict.py` production ML scripts
- `preprocessing.py` data cleaning and preprocessing
- `feature_engineering.py` engineered ML features
- `model_loader.py` inference helpers
- `notebooks/` Jupyter notebook workflow
- `data/` local datasets
- `models_streamlit/` trained Streamlit model files
- `reports_streamlit/` EDA reports, explainability plots, owner listings, and uploaded images

## Deployment

Path:

```text
deployment/
```

Contains deployment-related files copied from the backend for easier access.

## Recommended Working Style

Use this clean folder for future development:

```text
SmartSpaceAI_Full_Project
```

Keep raw downloads in `ml/data`, trained artifacts in `ml/models_streamlit`, and generated reports/images in `ml/reports_streamlit`.
