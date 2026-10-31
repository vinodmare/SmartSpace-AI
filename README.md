# SmartSpace AI - Full Stack AI Rental Platform

### Take a look at this Project
Repository: https://github.com/vinodmare/SmartSpace-AI

### It is a Full Stack AI Application. Built with Next.js, FastAPI and Machine Learning.
## It is an AI-powered Space Rental Platform.

### Application Features:
- It shows the working example of how an online space/property rental platform works, powered by machine learning.
- Where a User can browse and search rental spaces, view property details, register, login and logout.
- Where an Owner can add new property listings with images and manage their own listings.
- ML models help with smart predictions and recommendations for rental spaces.
- A separate Streamlit app is provided to train, test and demo the ML models.

### Technology used in this Project:
- i) Next.js (React): all frontend pages and UI have been written in Next.js.
- ii) FastAPI (Python): all backend APIs and business logic have been written in FastAPI.
- iii) Machine Learning (Python): model training, notebook and prediction logic live in the `ml` folder.
- iv) Streamlit: interactive ML demo and owner listing UI.
- v) CSV / Model files: owner listings and trained models are stored as files inside the `ml` folder.
- vi) Docker: deployment files are kept in the `deployment` folder.
- vii) GitHub Actions: CI/CD workflows are kept in the `.github` folder, if available.

### Software And Tools Required:
- Git
- Node.js 18+ and npm
- Python 3.10+
- pip (Python package manager)
- VS Code (or any code editor)
- Docker (optional, for deployment)

### Project Structure

```text
SmartSpace-AI/
  frontend/      Next.js frontend application
  backend/       FastAPI backend application
  ml/            Machine learning training, notebook, and Streamlit UI
  deployment/    Docker/deployment files
  docs/          Architecture and project notes
  .github/       GitHub Actions workflows, if available
```

### Steps To Clone And Run The Project

- Open Command Prompt / Terminal
- Clone the repository:

```bat
git clone https://github.com/vinodmare/SmartSpace-AI.git
cd SmartSpace-AI
```

- Now the project is downloaded. Run the three parts below (Frontend, Backend and ML app) in **separate terminals**.

#### 1. Run Frontend

```bat
cd frontend
npm install
npm run dev
```

Open in Browser:

```text
http://localhost:3000
```

#### 2. Run Backend

```bat
cd backend
copy .env.example .env
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

- Note: On Mac / Linux use `cp .env.example .env` instead of `copy .env.example .env`.
- Open `.env` file and put your own values (keys, database, secrets) if required.

Open API docs:

```text
http://127.0.0.1:8000/docs
```

#### 3. Run ML Streamlit App

```bat
cd ml
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open in Browser:

```text
http://localhost:8501
```

- Note: In Url put Port according to your system, if the default port is already in use.

### Default Ports

| Part      | URL                           |
|-----------|-------------------------------|
| Frontend  | http://localhost:3000         |
| Backend   | http://127.0.0.1:8000         |
| API Docs  | http://127.0.0.1:8000/docs    |
| ML App    | http://localhost:8501         |

### Where Data Is Stored

- Owner property images are stored in `ml/reports_streamlit/owner_images`.
- Owner listing rows are stored in `ml/reports_streamlit/owner_space_listings.csv`.
- ML model files are stored in `ml/models_streamlit`.

### Some Screenshots of this Project:
(Add your screenshots inside a `docs/screenshots` folder and update the file names below.)

![Home Page](docs/screenshots/home.png)
==================================================================================================================================================================
![Search / Listing Page](docs/screenshots/listings.png)
==================================================================================================================================================================
![Property Details Page](docs/screenshots/property.png)
==================================================================================================================================================================
![Owner Dashboard](docs/screenshots/owner-dashboard.png)
==================================================================================================================================================================
![Backend API Docs](docs/screenshots/api-docs.png)
==================================================================================================================================================================
![ML Streamlit App](docs/screenshots/streamlit.png)
==================================================================================================================================================================

### Notes

- Heavy generated folders were not copied: `node_modules`, `.next`, backend `.venv`, and Python `__pycache__`.
- Run `npm install` in `frontend` and `pip install -r requirements.txt` in `backend` and `ml` to recreate the required dependencies.
- It is recommended to create a Python virtual environment for the backend and ML parts:

```bat
python -m venv .venv
.venv\Scripts\activate
```

- Never commit your real `.env` file to GitHub. Only `.env.example` should be shared.

### Troubleshooting

- **Port already in use:** stop the other app or run on another port, e.g. `python -m uvicorn app.main:app --reload --port 8001`.
- **Frontend cannot reach backend:** make sure the backend is running and the API URL in the frontend config points to `http://127.0.0.1:8000`.
- **Module not found (Python):** activate your virtual environment and re-run `python -m pip install -r requirements.txt`.
- **Module not found (Node):** delete `node_modules` and run `npm install` again.

### Contributing

- Fork the repository
- Create a new branch: `git checkout -b feature/your-feature`
- Commit your changes: `git commit -m "Add your feature"`
- Push the branch: `git push origin feature/your-feature`
- Open a Pull Request

### Project Creator: Vinod Mare

- GitHub: [vinodmare](https://github.com/vinodmare)
- Email: vinodmare05@gmail.com
- Repository: https://github.com/vinodmare/SmartSpace-AI
