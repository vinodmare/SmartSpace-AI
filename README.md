# SmartSpace AI Full Project

Clean full-project workspace for the SmartSpace AI rental platform.

## Folder Structure

```text
SmartSpaceAI_Full_Project/
  frontend/      Next.js frontend application
  backend/       FastAPI backend application
  ml/            Machine learning training, notebook, and Streamlit UI
  deployment/    Docker/deployment files
  docs/          Architecture and project notes
  .github/       GitHub Actions workflows, if available
```

## Run Frontend

```bat
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Run Backend

```bat
cd backend
copy .env.example .env
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

## Run ML Streamlit App

```bat
cd ml
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

## Notes

- Heavy generated folders were not copied: `node_modules`, `.next`, backend `.venv`, and Python `__pycache__`.
- Owner property images are stored in `ml/reports_streamlit/owner_images`.
- Owner listing rows are stored in `ml/reports_streamlit/owner_space_listings.csv`.
- ML model files are stored in `ml/models_streamlit`.
