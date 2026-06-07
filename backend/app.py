from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import pickle
import numpy as np
import os

app = FastAPI(title="Student Performance Predictor", version="1.0.0")

# CORS — allows the frontend static site to call this API from a different domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "cat_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "scaler_cat.sav"), "rb") as f:
    scaler = pickle.load(f)


class StudentInput(BaseModel):
    hours_studied: int = Field(..., ge=1, le=9)
    previous_scores: int = Field(..., ge=40, le=99)
    extracurricular_activities: str
    sleep_hours: int = Field(..., ge=4, le=9)
    sample_question_papers_practiced: int = Field(..., ge=0, le=9)

    @field_validator("extracurricular_activities")
    @classmethod
    def check_extra(cls, v: str) -> str:
        if v not in ("Yes", "No"):
            raise ValueError("Must be 'Yes' or 'No'")
        return v


class PredictionOut(BaseModel):
    performance_index: float
    grade: str
    message: str


def to_grade(score: float) -> str:
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"


@app.get("/")
def root():
    return {"status": "ok", "api": "Student Performance Predictor", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionOut)
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
