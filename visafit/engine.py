"""Heuristic eligibility screen for UK international students.

Designed to be honest: uncertain beats a false eligible.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any


JOB_MARKERS = (
    "internship",
    "graduate scheme",
    "placement year",
    "full-time role",
    "job description",
    "we are hiring",
    "cv ",
    "resume",
    "recruiter",
)

TRAVEL_MARKERS = (
    "in-person",
    "in person",
    "on-site",
    "onsite",
    "must attend",
    "travel to",
    "san francisco",
    "new york",
    "silicon valley",
    "bangalore",
    "delhi",
)

REMOTE_MARKERS = (
    "remote",
    "online only",
    "fully online",
    "virtual hackathon",
    "submit online",
)

UK_MARKERS = (
    "united kingdom",
    " uk ",
    "uk-",
    "uk/",
    "britain",
    "england",
    "london",
)

STUDENT_MARKERS = (
    "students only",
    "current student",
    "university student",
    "undergraduate",
    "enrolled student",
)

YEAR2_MARKERS = (
    "year 2",
    "second year",
    "year two",
    "sophomore",
)

FINAL_YEAR_MARKERS = (
    "final year",
    "graduating",
    "penultimate",
    "last year of study",
)


@dataclass
class Profile:
    student_visa: bool = True
    final_year: bool = True
    uk_based: bool = True
    will_travel_abroad: bool = False


@dataclass
class Reason:
    code: str
    detail: str
    severity: str  # skip | warn | ok


@dataclass
class Verdict:
    status: str  # eligible | skip | uncertain
    summary: str
    reasons: list[Reason] = field(default_factory=list)
    signals: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "summary": self.summary,
            "reasons": [asdict(r) for r in self.reasons],
            "signals": self.signals,
        }


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def screen(rules_text: str, profile: Profile | None = None) -> Verdict:
    profile = profile or Profile()
    text = _norm(rules_text)
    reasons: list[Reason] = []
    signals: dict[str, Any] = {
        "job_shaped": False,
        "travel_abroad": False,
        "remote_ok": False,
        "uk_mentioned": False,
        "student_only": False,
        "year2_only": False,
        "final_year_friendly": False,
        "chars": len(text),
    }

    if len(text) < 40:
        return Verdict(
            status="uncertain",
            summary="Not enough rules text to judge. Paste the official eligibility section.",
            reasons=[
                Reason("too_short", "Need the opportunity's own criteria, not a one-liner.", "warn")
            ],
            signals=signals,
        )

    if any(m in text for m in JOB_MARKERS):
        signals["job_shaped"] = True
        reasons.append(
            Reason(
                "job_shaped",
                "Reads like employment (internship/job/CV). Skip for the student opportunity queue.",
                "skip",
            )
        )

    remote = any(m in text for m in REMOTE_MARKERS)
    travel = any(m in text for m in TRAVEL_MARKERS)
    signals["remote_ok"] = remote
    signals["travel_abroad"] = travel and not remote
    if travel and not remote and not profile.will_travel_abroad:
        reasons.append(
            Reason(
                "travel_abroad",
                "Looks in-person abroad (or travel-required) without a remote path.",
                "skip",
            )
        )

    uk = any(m in f" {text} " for m in UK_MARKERS) or "uk student" in text
    signals["uk_mentioned"] = uk
    if ("us only" in text or "united states only" in text or "us citizens" in text) and not uk:
        reasons.append(
            Reason("country_limit", "Geographic limit appears to exclude UK residents.", "skip")
        )

    student = any(m in text for m in STUDENT_MARKERS)
    signals["student_only"] = student
    if "not open to students" in text or "professionals only" in text:
        reasons.append(Reason("not_students", "Stated as not open to students.", "skip"))

    year2 = any(m in text for m in YEAR2_MARKERS)
    signals["year2_only"] = year2
    if year2 and profile.final_year and "final year" not in text and "any year" not in text:
        reasons.append(
            Reason(
                "year_level",
                "Year-2 (or similar) gate while profile is final year.",
                "skip",
            )
        )

    if any(m in text for m in FINAL_YEAR_MARKERS):
        signals["final_year_friendly"] = True

    if "deadline has passed" in text or "applications closed" in text or "registration closed" in text:
        reasons.append(Reason("closed", "Text says applications/registration already closed.", "skip"))

    skips = [r for r in reasons if r.severity == "skip"]
    if skips:
        return Verdict(
            status="skip",
            summary="Skip: at least one hard filter fired.",
            reasons=reasons,
            signals=signals,
        )

    if student or remote or (uk and "hackathon" in text):
        reasons.append(
            Reason("plausible_fit", "No hard skip fired; student/remote/UK signals look workable.", "ok")
        )
        return Verdict(
            status="eligible",
            summary="Eligible on the stated text for this profile (verify on the official page).",
            reasons=reasons,
            signals=signals,
        )

    reasons.append(
        Reason(
            "ambiguous",
            "No hard skip, but student/remote/UK fit is unclear. Check the official page.",
            "warn",
        )
    )
    return Verdict(
        status="uncertain",
        summary="Uncertain: need clearer eligibility language from the official page.",
        reasons=reasons,
        signals=signals,
    )
