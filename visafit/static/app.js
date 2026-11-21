const $ = (id) => document.getElementById(id);
const HIST_KEY = "visafit.history.v1";

const SKIP_SAMPLE = `Eligibility: Year 2 UK undergraduates only.
Format: In-person San Francisco, must attend all days.
This is a paid internship. Please attach your CV. Applications closed.`;

const OK_SAMPLE = `Open to university students worldwide.
Remote / online hackathon. Submit your project on Devpost.
United Kingdom residents welcome. No travel required.
Final-year undergraduates are eligible.`;

let lastVerdict = null;

function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem(HIST_KEY) || "[]");
  } catch (_) {
    return [];
  }
}

function saveHistory(items) {
  localStorage.setItem(HIST_KEY, JSON.stringify(items.slice(0, 8)));
}

function renderHistory() {
  const ul = $("history");
  if (!ul) return;
  const items = loadHistory();
  ul.innerHTML = items
    .map((it, i) => {
      const snippet = (it.rules || "").replace(/\s+/g, " ").slice(0, 72);
      return `<li data-i="${i}"><span class="tag ${it.status}">${it.status}</span>${snippet}</li>`;
    })
    .join("");
  ul.querySelectorAll("li").forEach((li) => {
    li.onclick = () => {
      const it = loadHistory()[Number(li.dataset.i)];
      if (!it) return;
      $("rules").value = it.rules || "";
      render(it.verdict || { status: it.status, summary: it.summary, reasons: [], signals: {} });
    };
  });
}

function pushHistory(rules, data) {
  const items = loadHistory();
  items.unshift({
    at: new Date().toISOString(),
    status: data.status,
    summary: data.summary,
    rules,
    verdict: data,
  });
  saveHistory(items);
  renderHistory();
}

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

const clearBtn = $("clear_history");
if (clearBtn) {
  clearBtn.onclick = () => {
    localStorage.removeItem(HIST_KEY);
    renderHistory();
  };
}

$("run").onclick = async () => {
  const body = {
    rules_text: $("rules").value,
    ...profileFromForm(),
  };
  let data;
  try {
    const res = await fetch("/api/screen", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (res.ok) data = await res.json();
  } catch (_) {
    /* static host */
  }
  if (!data && window.VisaFit && typeof window.VisaFit.screen === "function") {
    data = window.VisaFit.screen(body.rules_text, body);
  }
  if (!data) {
    data = {
      status: "uncertain",
      summary: "No API and no client engine loaded.",
      reasons: [],
      signals: {},
    };
  }
  render(data);
  pushHistory(body.rules_text, data);
};

renderHistory();
