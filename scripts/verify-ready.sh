#!/usr/bin/env bash
# Exit 0 only when VisaFit is submit-ready (local + public assets).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ART="/Users/efi/VIP/Sheets/Daily Log sheet/artifacts/2026-11-21/evohacks-2"
fail=0
check() {
  local name="$1" ok="$2"
  if [[ "$ok" == "1" ]]; then echo "OK  $name"; else echo "FAIL $name"; fail=1; fi
}

cd "$ROOT"
.venv/bin/python -m pytest -q >/tmp/visafit-pytest.txt 2>&1 && check "pytest" 1 || check "pytest (see /tmp/visafit-pytest.txt)" 0
[[ -f scripts/submit-now.sh ]] && check "submit-now.sh" 1 || check "submit-now.sh" 0
[[ -f visafit/pivot.py ]] && check "pivot.py" 1 || check "pivot.py" 0
[[ -f docs/index.html && -f docs/engine.js ]] && check "Pages docs/" 1 || check "Pages docs/" 0

code_pages=$(curl -s -o /dev/null -w "%{http_code}" "https://shahaman098.github.io/visafit-evohacks-2/")
[[ "$code_pages" == "200" ]] && check "Pages live ($code_pages)" 1 || check "Pages live ($code_pages)" 0
code_yt=$(curl -s -o /dev/null -w "%{http_code}" "https://youtu.be/03YcRirbqIA")
[[ "$code_yt" == "200" || "$code_yt" == "302" || "$code_yt" == "303" ]] && check "YouTube ($code_yt)" 1 || check "YouTube ($code_yt)" 0
code_repo=$(curl -s -o /dev/null -w "%{http_code}" "https://github.com/shahaman098/visafit-evohacks-2")
[[ "$code_repo" == "200" ]] && check "GitHub ($code_repo)" 1 || check "GitHub ($code_repo)" 0

code_v=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:8791/" || echo 000)
[[ "$code_v" == "200" ]] && check "local VisaFit :8791" 1 || check "local VisaFit :8791 ($code_v)" 0
code_c=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:8765/" || echo 000)
[[ "$code_c" == "200" ]] && check "ChonkVid :8765" 1 || check "ChonkVid :8765 ($code_c) — parallel only" 0

if [[ -x "$ART/poll-gate.sh" ]]; then
  if bash "$ART/poll-gate.sh" "$ART/gate-status.txt"; then
    check "Devpost gate OPEN" 1
  else
    echo "WAIT Devpost gate still closed (expected before 17:00 UTC)"
  fi
fi

exit $fail
