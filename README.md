# VisaFit

**Live demo:** https://shahaman098.github.io/visafit-evohacks-2/

**EvoHacks 2** solo project by [shahaman098](https://github.com/shahaman098) (Aman "Kris" Sah, Brunel CS AI).

Paste opportunity rules (hackathon, grant, programme). VisaFit returns a structured eligibility screen for a **UK international student on a student visa**: student-only gates, age, country/residency limits, travel, and whether it looks like a job (which this builder routes elsewhere).

> Theme note: EvoHacks 2 publishes its theme when hacking opens. The product below solves a real student problem today; if the theme needs a different surface, the same checker can be retargeted without rewriting the core.

## Problem

International students waste hours chasing opportunities that quietly exclude them (wrong year, no UK residents, in-person abroad with no travel support, or job ads dressed as "programmes"). Digest sites rarely encode visa reality.

## Solution

1. Paste rules text (or a short description).
2. Optionally set your profile flags (student visa, final year, London/UK only).
3. Get a verdict: **eligible / skip / uncertain**, with reason codes you can act on.

No API key required for the heuristic engine. An optional `OPENAI_COMPAT_*` env block can refine uncertain cases later.

## Quick start

```bash
cd ~/Hackathons/EvoHacks-2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn visafit.app:app --reload --port 8791
```

Open http://127.0.0.1:8791

```bash
pytest -q
```

## Demo script (≤3 min)

1. Open the UI.
2. Paste a sample: "Year 2 UK undergraduates only. In-person San Francisco. Paid internship."
3. Show the **skip** verdict with `year_level`, `travel_abroad`, `job_shaped` reasons.
4. Paste a student hackathon open worldwide with remote submit; show **eligible**.

## Built during the event

- Heuristic eligibility engine (`visafit/engine.py`)
- FastAPI API + single-page UI
- Pytest coverage for core reason codes
- This README and sample fixtures

## Stack

Python 3 · FastAPI · Uvicorn · Pytest · vanilla HTML/CSS/JS

## License

MIT
