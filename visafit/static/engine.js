/** Client-side port of visafit.engine.screen — keep in sync with engine.py */
(function (global) {
  const JOB_MARKERS = [
    "internship",
    "graduate scheme",
    "placement year",
    "full-time role",
    "job description",
    "we are hiring",
    "cv ",
    "resume",
    "recruiter",
  ];
  const TRAVEL_MARKERS = [
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
  ];
  const REMOTE_MARKERS = [
    "remote",
    "online only",
    "fully online",
    "virtual hackathon",
    "submit online",
  ];
  const UK_MARKERS = [
    "united kingdom",
    " uk ",
    "uk-",
    "uk/",
    "britain",
    "england",
    "london",
  ];
  const STUDENT_MARKERS = [
    "students only",
    "current student",
    "university student",
    "undergraduate",
    "enrolled student",
  ];
  const YEAR2_MARKERS = ["year 2", "second year", "year two", "sophomore"];
  const FINAL_YEAR_MARKERS = [
    "final year",
    "graduating",
    "penultimate",
    "last year of study",
  ];

  function norm(text) {
    return String(text || "")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  }

  function anyIn(text, markers) {
    return markers.some((m) => text.includes(m));
  }

  function screen(rulesText, profile) {
    const p = Object.assign(
      {
        student_visa: true,
        final_year: true,
        uk_based: true,
        will_travel_abroad: false,
      },
      profile || {}
    );
    const text = norm(rulesText);
    const reasons = [];
    const signals = {
      job_shaped: false,
      travel_abroad: false,
      remote_ok: false,
      uk_mentioned: false,
      student_only: false,
      year2_only: false,
      final_year_friendly: false,
      chars: text.length,
    };

    if (text.length < 40) {
      return {
        status: "uncertain",
        summary:
          "Not enough rules text to judge. Paste the official eligibility section.",
        reasons: [
          {
            code: "too_short",
            detail: "Need the opportunity's own criteria, not a one-liner.",
            severity: "warn",
          },
        ],
        signals,
      };
    }

    if (anyIn(text, JOB_MARKERS)) {
      signals.job_shaped = true;
      reasons.push({
        code: "job_shaped",
        detail:
          "Reads like employment (internship/job/CV). Skip for the student opportunity queue.",
        severity: "skip",
      });
    }

    const remote = anyIn(text, REMOTE_MARKERS);
    const travel = anyIn(text, TRAVEL_MARKERS);
    signals.remote_ok = remote;
    signals.travel_abroad = travel && !remote;
    if (travel && !remote && !p.will_travel_abroad) {
      reasons.push({
        code: "travel_abroad",
        detail:
          "Looks in-person abroad (or travel-required) without a remote path.",
        severity: "skip",
      });
    }

    const uk = anyIn(` ${text} `, UK_MARKERS) || text.includes("uk student");
    signals.uk_mentioned = uk;
    if (
      (text.includes("us only") ||
        text.includes("united states only") ||
        text.includes("us citizens")) &&
      !uk
    ) {
      reasons.push({
        code: "country_limit",
        detail: "Geographic limit appears to exclude UK residents.",
        severity: "skip",
      });
    }

    const student = anyIn(text, STUDENT_MARKERS);
    signals.student_only = student;
    if (
      text.includes("not open to students") ||
      text.includes("professionals only")
    ) {
      reasons.push({
        code: "not_students",
        detail: "Stated as not open to students.",
        severity: "skip",
      });
    }

    const year2 = anyIn(text, YEAR2_MARKERS);
    signals.year2_only = year2;
    if (
      year2 &&
      p.final_year &&
      !text.includes("final year") &&
      !text.includes("any year")
    ) {
      reasons.push({
        code: "year_level",
        detail: "Year-2 (or similar) gate while profile is final year.",
        severity: "skip",
      });
    }

    if (anyIn(text, FINAL_YEAR_MARKERS)) {
      signals.final_year_friendly = true;
    }

    if (
      text.includes("deadline has passed") ||
      text.includes("applications closed") ||
      text.includes("registration closed")
    ) {
      reasons.push({
        code: "closed",
        detail: "Text says applications/registration already closed.",
        severity: "skip",
      });
    }

    const skips = reasons.filter((r) => r.severity === "skip");
    if (skips.length) {
      return {
        status: "skip",
        summary: "Skip: at least one hard filter fired.",
        reasons,
        signals,
      };
    }

    if (student || remote || (uk && text.includes("hackathon"))) {
      reasons.push({
        code: "plausible_fit",
        detail:
          "No hard skip fired; student/remote/UK signals look workable.",
        severity: "ok",
      });
      return {
        status: "eligible",
        summary:
          "Eligible on the stated text for this profile (verify on the official page).",
        reasons,
        signals,
      };
    }

    reasons.push({
      code: "ambiguous",
      detail:
        "No hard skip, but student/remote/UK fit is unclear. Check the official page.",
      severity: "warn",
    });
    return {
      status: "uncertain",
      summary:
        "Uncertain: need clearer eligibility language from the official page.",
      reasons,
      signals,
    };
  }

  global.VisaFit = { screen };
})(typeof window !== "undefined" ? window : globalThis);
