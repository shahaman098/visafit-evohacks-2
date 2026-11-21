# Devpost submission checklist (EvoHacks 2)

Opens: **21 Nov 2026 9:00am PST** (17:00 UTC) · Due: **22 Nov 2026 12:00pm PST**

## Ready assets

| Field | Value |
|---|---|
| Name | VisaFit |
| Tagline | Paste opportunity rules. Get eligible / skip / uncertain for a UK student-visa builder. |
| Repo | https://github.com/shahaman098/visafit-evohacks-2 |
| Demo video | https://youtu.be/03YcRirbqIA |
| Demo | https://shahaman098.github.io/visafit-evohacks-2/ (GitHub Pages) · local `uvicorn visafit.app:app --port 8791` |
| Built with | Python, FastAPI, Uvicorn, Pytest, HTML, CSS, JavaScript, localStorage |

## When theme drops

1. Paste theme into `THEME.md`.
2. Rewrite Fit-to-Prompt paragraph in README + UI lede so the theme is central.
3. Re-record or keep slideshow demo if still shows the core workflow.
4. Create/update Devpost project → **Submit** to EvoHacks 2.
5. Capture confirmation → Daily Log ledger + queue `#173` done.

## Built during the event / pre-existing

- Built for this hackathon in `~/Hackathons/EvoHacks-2` (heuristic engine, API, UI, tests, demo).
- No sponsor SDK wired yet (MojoAuth / SSOJet / Agentboxd left for theme-fit if useful).

## Devpost project (pre-submit)

- Portfolio project: https://devpost.com/software/visafit-evohacks-2
- YouTube demo (unlisted): https://youtu.be/03YcRirbqIA
- Attach to EvoHacks 2 when submissions open (21 Nov 9:00am PST).


### Paste into Devpost — Built during the event

Heuristic eligibility engine, FastAPI API + vanilla UI, CLI (`python -m visafit`), pytest suite, theme-pivot helper, README/THEME, and a ≤3 min demo video recorded against the core screen workflow. No pre-existing product code; profile heuristics encode a UK student-visa builder's hard filters.

### Paste into Devpost — Try it out

```bash
git clone https://github.com/shahaman098/visafit-evohacks-2
cd visafit-evohacks-2
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn visafit.app:app --port 8791
# open http://127.0.0.1:8791
# or: .venv/bin/python -m visafit path/to/rules.txt
```
