from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
import pickle
import numpy as np
import os

# ─────────────────────────────────────────────
#  App
# ─────────────────────────────────────────────
app = FastAPI(
    title="Student Performance Predictor",
    description="Predicts student Performance Index using CatBoostRegressor + StandardScaler.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
#  Load model & scaler
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "cat_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "scaler_cat.sav"), "rb") as f:
    scaler = pickle.load(f)

# ─────────────────────────────────────────────
#  Schemas
# ─────────────────────────────────────────────
class StudentInput(BaseModel):
    hours_studied: int = Field(..., ge=1, le=9,
        description="Hours studied per day (1–9)")
    previous_scores: int = Field(..., ge=40, le=99,
        description="Previous exam score (40–99)")
    extracurricular_activities: str = Field(...,
        description="Participates in extracurriculars: 'Yes' or 'No'")
    sleep_hours: int = Field(..., ge=4, le=9,
        description="Hours of sleep per day (4–9)")
    sample_question_papers_practiced: int = Field(..., ge=0, le=9,
        description="Number of sample papers practiced (0–9)")

    @field_validator("extracurricular_activities")
    @classmethod
    def check_extra(cls, v: str) -> str:
        if v not in ("Yes", "No"):
            raise ValueError("Must be 'Yes' or 'No'")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "hours_studied": 7,
                "previous_scores": 75,
                "extracurricular_activities": "Yes",
                "sleep_hours": 8,
                "sample_question_papers_practiced": 5,
            }
        }
    }


class PredictionOut(BaseModel):
    performance_index: float
    grade: str
    message: str


# ─────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────
def to_grade(score: float) -> str:
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"


# ─────────────────────────────────────────────
#  API Routes  (register BEFORE static mount)
# ─────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "model": "CatBoostRegressor", "scaler": "StandardScaler"}


@app.post("/predict", response_model=PredictionOut, tags=["Prediction"])
def predict(student: StudentInput):
    try:
        extra = 1 if student.extracurricular_activities == "Yes" else 0
        features = np.array([[
            student.hours_studied,
            student.previous_scores,
            extra,
            student.sleep_hours,
            student.sample_question_papers_practiced,
        ]])
        scaled = scaler.transform(features)
        score = float(np.round(model.predict(scaled)[0], 2))
        grade = to_grade(score)
        return PredictionOut(
            performance_index=score,
            grade=grade,
            message=f"Performance Index: {score:.1f}/100 — Grade {grade}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", tags=["Prediction"])
def predict_batch(students: list[StudentInput]):
    """Predict for multiple students at once (max 100)."""
    if len(students) > 100:
        raise HTTPException(status_code=400, detail="Max 100 students per batch.")
    results = []
    for s in students:
        extra = 1 if s.extracurricular_activities == "Yes" else 0
        features = np.array([[
            s.hours_studied,
            s.previous_scores,
            extra,
            s.sleep_hours,
            s.sample_question_papers_practiced,
        ]])
        scaled = scaler.transform(features)
        score = float(np.round(model.predict(scaled)[0], 2))
        results.append({"performance_index": score, "grade": to_grade(score)})
    return {"count": len(results), "predictions": results}


# ─────────────────────────────────────────────
#  Serve frontend static files
#  Mount AFTER API routes so /predict etc. win
# ─────────────────────────────────────────────
FRONTEND_DIR = os.path.join(BASE_DIR, "static")

if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
else:
    # Fallback root when no frontend is present
    @app.get("/", tags=["Health"])
    def root():
        return {
            "status": "ok",
            "api": "Student Performance Predictor",
            "model": "CatBoostRegressor",
            "version": "1.0.0",
            "docs": "/docs",
        }
