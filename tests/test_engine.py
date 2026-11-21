from visafit.engine import Profile, screen


def test_skip_job_and_year_and_travel():
    text = (
        "Year 2 UK undergraduates only. In-person San Francisco must attend. "
        "Paid internship. Attach your CV. Applications closed."
    )
    v = screen(text, Profile(final_year=True, will_travel_abroad=False))
    assert v.status == "skip"
    codes = {r.code for r in v.reasons}
    assert "job_shaped" in codes
    assert "year_level" in codes
    assert "travel_abroad" in codes
    assert "closed" in codes


def test_eligible_remote_student_hackathon():
    text = (
        "Open to university students worldwide. Remote online hackathon. "
        "Submit on Devpost. United Kingdom residents welcome. Final year OK."
    )
    v = screen(text, Profile(final_year=True))
    assert v.status == "eligible"


def test_too_short_uncertain():
    v = screen("students only")
    assert v.status == "uncertain"
    assert v.reasons[0].code == "too_short"
