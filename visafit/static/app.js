const $ = (id) => document.getElementById(id);

const SKIP_SAMPLE = `Eligibility: Year 2 UK undergraduates only.
Format: In-person San Francisco, must attend all days.
This is a paid internship. Please attach your CV. Applications closed.`;

const OK_SAMPLE = `Open to university students worldwide.
Remote / online hackathon. Submit your project on Devpost.
United Kingdom residents welcome. No travel required.
Final-year undergraduates are eligible.`;

$("sample_skip").onclick = () => { $("rules").value = SKIP_SAMPLE; };
$("sample_ok").onclick = () => { $("rules").value = OK_SAMPLE; };

$("run").onclick = async () => {
  const body = {
    rules_text: $("rules").value,
    student_visa: $("student_visa").checked,
    final_year: $("final_year").checked,
    uk_based: $("uk_based").checked,
    will_travel_abroad: $("will_travel_abroad").checked,
  };
  const res = await fetch("/api/screen", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  const result = $("result");
  result.hidden = false;
  const status = $("status");
  status.textContent = data.status;
  status.className = "status " + data.status;
  $("summary").textContent = data.summary;
  $("reasons").innerHTML = (data.reasons || [])
    .map((r) => `<li><strong>${r.code}</strong> (${r.severity}): ${r.detail}</li>`)
    .join("");
  $("signals").textContent = JSON.stringify(data.signals, null, 2);
};
