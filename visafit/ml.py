"""Train + load a classic ML screener (sklearn) for EvoHacks Fit-to-Prompt."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_DIR = Path(__file__).resolve().parent / "models"
MODEL_PATH = MODEL_DIR / "screener.joblib"
META_PATH = MODEL_DIR / "screener.meta.json"
LABELS = ("eligible", "skip", "uncertain")


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=4000)),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def default_corpus() -> list[tuple[str, str]]:
    """Synthetic labeled opportunity blurbs for a UK final-year student visa profile."""
    return [
        ("Open to all university students worldwide. Free to enter. Online only.", "eligible"),
        ("Undergraduate students welcome. Remote participation. No fee.", "eligible"),
        ("Open to students on a UK student visa. Online hackathon. Free.", "eligible"),
        ("Final year students encouraged. Virtual event. No travel required.", "eligible"),
        ("Open worldwide. Online. Students and recent grads. Free tier.", "eligible"),
        ("UK students only. Online. No payment required.", "eligible"),
        ("Global student hackathon. Virtual. Free registration.", "eligible"),
        ("Open to bachelor students. Online demo day. Free.", "eligible"),
        ("Must be year 1 or year 2 only. Not open to final year.", "skip"),
        ("High school students only. Ages 13-18. Not university.", "skip"),
        ("US citizens only. Must reside in the United States.", "skip"),
        ("In-person only in San Francisco. No travel support. Must attend on site.", "skip"),
        ("Paid entry $99 required. No free tier.", "skip"),
        ("Graduate scheme / full-time job application. Not a hackathon.", "skip"),
        ("Must be under 18. University students ineligible.", "skip"),
        ("Requires India residency and Aadhaar. Not open to UK visa holders.", "skip"),
        ("Eligibility unclear. Contact organisers for visa status.", "uncertain"),
        ("Some tracks online, some require travel. Details TBD.", "uncertain"),
        ("Open to students; residency restrictions may apply. Check with host.", "uncertain"),
        ("Free or paid tracks; unclear which are required.", "uncertain"),
        ("Theme revealed at kickoff. Confirm student status with organisers.", "uncertain"),
        ("Hybrid event. Travel optional but encouraged. Visa support unknown.", "uncertain"),
        ("Students welcome if enrolled. Country limits not listed.", "uncertain"),
        ("Prize pool crypto-only; eligibility for UK students unclear.", "uncertain"),
        ("Online AI hackathon for university students. Free. Worldwide.", "eligible"),
        ("Train a model. Open to students. Virtual. No fee.", "eligible"),
        ("Fine-tune a pretrained model. Open globally. Online.", "eligible"),
        ("Must travel to Singapore. No stipend. In person only.", "skip"),
        ("Internships and placements only. Not a competition.", "skip"),
        ("Age 16-17 only. Final year uni students out of scope.", "skip"),
    ]


def train(corpus: list[tuple[str, str]] | None = None) -> dict[str, Any]:
    data = corpus or default_corpus()
    texts = [t for t, _ in data]
    labels = [y for _, y in data]
    pipe = build_pipeline()
    pipe.fit(texts, labels)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    meta = {
        "model": "TfidfVectorizer + LogisticRegression",
        "labels": list(LABELS),
        "n_samples": len(data),
        "path": str(MODEL_PATH),
        "note": "Trained classifier over opportunity-rules text for eligibility triage.",
    }
    META_PATH.write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def load_pipeline() -> Pipeline | None:
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def predict(rules_text: str) -> dict[str, Any]:
    pipe = load_pipeline()
    if pipe is None:
        return {"label": "uncertain", "confidence": 0.0, "model_loaded": False}
    proba = pipe.predict_proba([rules_text])[0]
    classes = list(pipe.classes_)
    best_i = int(proba.argmax())
    return {
        "label": classes[best_i],
        "confidence": float(proba[best_i]),
        "probs": {c: float(p) for c, p in zip(classes, proba)},
        "model_loaded": True,
        "model": "sklearn LogisticRegression over TF-IDF",
    }
