# 🎓 Student Performance Predictor

> An AI-powered web application that predicts a student's academic **Performance Index** (0–100) based on study habits and lifestyle inputs — built with CatBoost, FastAPI, and deployed on Render.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://student-performance-model-s23t.onrender.com)
[![API Docs](https://img.shields.io/badge/API%20Docs-Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://student-performance-model-s23t.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [API Reference](#-api-reference)
- [Local Development](#-local-development)
- [Deployment on Render](#-deployment-on-render)
- [Grade Scale](#-grade-scale)
- [Author](#-author)

---

## 🔍 Overview

The **Student Performance Predictor** uses a trained **CatBoostRegressor** machine learning model to estimate a student's performance index. Users enter 5 simple inputs through a clean web interface and instantly receive a predicted score and grade.

The app is split into two independently deployed services on Render:

| Service | Technology | Purpose |
|---------|-----------|---------|
| **Backend** | FastAPI + Python | REST API, ML inference |
| **Frontend** | Static HTML/CSS/JS | User interface |

---

## ✨ Features

- 🤖 **ML-powered predictions** using CatBoostRegressor trained on student performance data
- ⚡ **Instant results** with animated progress bar and grade badge
- 🌐 **REST API** with full Swagger/OpenAPI documentation at `/docs`
- 📦 **Batch prediction** endpoint — predict up to 100 students at once
- 🔒 **Input validation** on both frontend and backend
- 📱 **Responsive design** — works on desktop and mobile
- 🚀 **Deployed on Render** — free tier, always available

---

## 📁 Project Structure

```
student-performance-model/
│
├── backend/                        # FastAPI backend (Render Web Service)
│   ├── app.py                      # Main API application
│   ├── cat_model.pkl               # Trained CatBoostRegressor model
│   ├── scaler_cat.sav              # Fitted StandardScaler
│   └── requirements.txt            # Python dependencies
│
├── frontend/                       # Static site (Render Static Site)
│   ├── index.html                  # Main HTML page
│   ├── style.css                   # Styles and animations
│   └── app.js                      # Fetch API calls + UI logic
│
├── render.yaml                     # Render deployment configuration
└── README.md                       # This file
```

---

## 🛠 Tech Stack

**Machine Learning**
- [CatBoost](https://catboost.ai/) — gradient boosting model for regression
- [scikit-learn](https://scikit-learn.org/) — StandardScaler for feature normalization
- [NumPy](https://numpy.org/) — numerical computations

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — high-performance Python web framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [Pydantic v2](https://docs.pydantic.dev/) — data validation and serialization

**Frontend**
- Vanilla HTML5, CSS3, JavaScript (no frameworks)
- Google Fonts — Syne + DM Sans
- Fetch API for backend communication

**Infrastructure**
- [Render](https://render.com/) — cloud deployment (Web Service + Static Site)
- [GitHub](https://github.com/) — source control and CI/CD trigger

---

## ⚙️ How It Works

```
User fills form
      │
      ▼
Frontend validates input (JS)
      │
      ▼
POST /predict  ──►  FastAPI backend
                          │
                          ▼
                   StandardScaler
                   normalizes features
                          │
                          ▼
                   CatBoostRegressor
                   predicts score (0–100)
                          │
                          ▼
                   Returns JSON response
      │
      ▼
Frontend displays
score + grade + progress bar
```

**Input features used by the model:**

| Feature | Range | Description |
|---------|-------|-------------|
| `hours_studied` | 1 – 9 | Hours of study per day |
| `previous_scores` | 40 – 99 | Score in previous exam |
| `extracurricular_activities` | Yes / No | Participation in activities |
| `sleep_hours` | 4 – 9 | Hours of sleep per day |
| `sample_question_papers_practiced` | 0 – 9 | Practice papers completed |

---

## 📡 API Reference

Base URL: `https://student-performance-model-s23t.onrender.com`

### `GET /health`
Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### `POST /predict`
Predict performance index for a single student.

**Request body:**
```json
{
  "hours_studied": 7,
  "previous_scores": 75,
  "extracurricular_activities": "Yes",
  "sleep_hours": 8,
  "sample_question_papers_practiced": 5
}
```

**Response:**
```json
{
  "performance_index": 83.47,
  "grade": "A",
  "message": "Performance Index: 83.5/100 — Grade A"
}
```

---

### `POST /predict/batch`
Predict performance for multiple students at once (max 100).

**Request body:**
```json
[
  {
    "hours_studied": 7,
    "previous_scores": 75,
    "extracurricular_activities": "Yes",
    "sleep_hours": 8,
    "sample_question_papers_practiced": 5
  },
  {
    "hours_studied": 3,
    "previous_scores": 50,
    "extracurricular_activities": "No",
    "sleep_hours": 6,
    "sample_question_papers_practiced": 2
  }
]
```

**Response:**
```json
{
  "count": 2,
  "predictions": [
    { "performance_index": 83.47, "grade": "A" },
    { "performance_index": 41.22, "grade": "F" }
  ]
}
```

> Full interactive API docs available at [`/docs`](https://student-performance-model-s23t.onrender.com/docs)

---

## 💻 Local Development

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the repository
```bash
git clone https://github.com/Abdalla-bakar/student-performance-model.git
cd student-performance-model
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the backend server
```bash
uvicorn app:app --reload --port 8000
```

API is now running at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### 4. Run the frontend

In a new terminal, serve the frontend folder with any static server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 5500
```

Then open `http://localhost:5500` in your browser.

> **Note:** For local development, temporarily change line 1 of `frontend/app.js`:
> ```js
> const API_URL = 'http://localhost:8000/predict';
> ```

---

## 🚀 Deployment on Render

This project is deployed as **two separate Render services**.

### Service 1 — Backend (Web Service)

| Setting | Value |
|---------|-------|
| **Type** | Web Service |
| **Environment** | Python 3 |
| **Root Directory** | `backend` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free |

### Service 2 — Frontend (Static Site)

| Setting | Value |
|---------|-------|
| **Type** | Static Site |
| **Root Directory** | `frontend` |
| **Build Command** | *(leave empty)* |
| **Publish Directory** | `frontend` |

### Environment Variables (Backend)

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.12.0` |

### Auto-Deploy
Both services are connected to GitHub. Every `git push` to `main` triggers an automatic redeploy.

---

## 📊 Grade Scale

| Performance Index | Grade |
|:-----------------:|:-----:|
| 90 – 100 | A+ |
| 80 – 89 | A |
| 70 – 79 | B |
| 60 – 69 | C |
| 50 – 59 | D |
| 0 – 49 | F |

---

## 👤 Author

**Abdalla Bakar**

[![GitHub](https://img.shields.io/badge/GitHub-Abdalla--bakar-181717?style=flat-square&logo=github)](https://github.com/Abdalla-bakar)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with ❤️ using FastAPI + CatBoost · Deployed on Render</sub>
</div>
