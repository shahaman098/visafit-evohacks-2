from fastapi.testclient import TestClient

from visafit.app import app

client = TestClient(app)


def test_health_and_screen():
    assert client.get("/health").json()["ok"] == "true"
    payload = {
        "rules_text": (
            "Open to university students worldwide. Fully online hackathon in the "
            "United Kingdom timezone. Remote submit. No travel."
        )
    }
    r = client.post("/api/screen", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] in {"eligible", "uncertain", "skip"}


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200
    assert b"VisaFit" in r.content
