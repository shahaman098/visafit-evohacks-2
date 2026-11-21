from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from visafit.engine import Profile, screen

STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(title="VisaFit", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


class ScreenRequest(BaseModel):
    rules_text: str = Field(..., min_length=1)
    student_visa: bool = True
    final_year: bool = True
    uk_based: bool = True
    will_travel_abroad: bool = False


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"ok": "true", "service": "visafit"}


@app.post("/api/screen")
def api_screen(body: ScreenRequest) -> dict:
    profile = Profile(
        student_visa=body.student_visa,
        final_year=body.final_year,
        uk_based=body.uk_based,
        will_travel_abroad=body.will_travel_abroad,
    )
    return screen(body.rules_text, profile).to_dict()
