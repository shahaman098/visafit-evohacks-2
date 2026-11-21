const $ = (id) => document.getElementById(id);

const SKIP_SAMPLE = `Eligibility: Year 2 UK undergraduates only.
Format: In-person San Francisco, must attend all days.
This is a paid internship. Please attach your CV. Applications closed.`;

const OK_SAMPLE = `Open to university students worldwide.
Remote / online hackathon. Submit your project on Devpost.
United Kingdom residents welcome. No travel required.
Final-year undergraduates are eligible.`;

let lastVerdict = null;

function render(data) {
  lastVerdict = data;
  const result = $("result");
  result.hidden = false;
  const status = $("status");
  status.textContent = data.status;
  status.className = "status " + data.status;
  $("summary").textContent = data.summary;
  $("reasons").innerHTML = (data.reasons || [])
    .map(
      (r) =>
        `<li><strong>${r.code}</strong> (${r.severity}): ${r.detail}</li>`
    )
    .join("");
  $("signals").textContent = JSON.stringify(data.signals, null, 2);
  const copyBtn = $("copy_verdict");
  if (copyBtn) copyBtn.hidden = false;
}

function profileFromForm() {
  return {
    student_visa: $("student_visa").checked,
    final_year: $("final_year").checked,
    uk_based: $("uk_based").checked,
    will_travel_abroad: $("will_travel_abroad").checked,
  };
}

function verdictMarkdown(data) {
  const reasons = (data.reasons || [])
    .map((r) => `- **${r.code}** (${r.severity}): ${r.detail}`)
    .join("\n");
  return [
    `# VisaFit verdict: ${data.status}`,
    "",
    data.summary || "",
    "",
    "## Reasons",
    reasons || "_none_",
    "",
    "## Signals",
    "```json",
    JSON.stringify(data.signals || {}, null, 2),
    "```",
    "",
  ].join("\n");
}

$("sample_skip").onclick = () => {
  $("rules").value = SKIP_SAMPLE;
};
$("sample_ok").onclick = () => {
  $("rules").value = OK_SAMPLE;
};

const copyBtn = $("copy_verdict");
if (copyBtn) {
  copyBtn.onclick = async () => {
    if (!lastVerdict) return;
    const text = verdictMarkdown(lastVerdict);
    try {
      await navigator.clipboard.writeText(text);
      copyBtn.textContent = "Copied";
      setTimeout(() => {
        copyBtn.textContent = "Copy verdict";
      }, 1200);
    } catch (_) {
      copyBtn.textContent = "Copy failed";
    }
  };
}

$("run").onclick = async () => {
  const body = {
    rules_text: $("rules").value,
    ...profileFromForm(),
  };
  try {
    const res = await fetch("/api/screen", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (res.ok) {
      render(await res.json());
      return;
    }
  } catch (_) {
    /* static host */
  }
  if (window.VisaFit && typeof window.VisaFit.screen === "function") {
    render(window.VisaFit.screen(body.rules_text, body));
    return;
  }
  render({
    status: "uncertain",
    summary: "No API and no client engine loaded.",
    reasons: [],
    signals: {},
  });
};
