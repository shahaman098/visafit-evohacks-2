#!/usr/bin/env bash
# Run at/after 21 Nov 2026 17:00 UTC when EvoHacks submissions open.
# Usage: ./scripts/submit-now.sh "OFFICIAL THEME TEXT"
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="/Users/efi/VIP/Sheets/Daily Log sheet"
ART="$LOG/artifacts/2026-11-21/evohacks-2"
THEME="${1:-}"

cd "$LOG"
bash "$ART/poll-gate.sh" "$ART/gate-status.txt" || true
GATE=$?
if [[ "$GATE" -eq 2 ]]; then
  echo "BLOCKED: Devpost still says Submissions open soon. Re-run after 17:00 UTC."
  exit 2
fi

cd "$ROOT"
if [[ -z "$THEME" ]]; then
  echo "Theme text required once the official prompt drops."
  echo "Usage: $0 \"THEME TEXT\""
  exit 1
fi

.venv/bin/python -m visafit.pivot "$THEME"
.venv/bin/python -m pytest -q
git add -A
git commit -m "Pivot VisaFit copy to official EvoHacks theme." || true
git push origin main

echo ""
echo "NEXT (browser, signed in as shahaman098):"
echo "1. https://devpost.com/software/visafit-evohacks-2/edit  — refresh About if needed"
echo "2. https://devpost.com/submit-to/31721-evohacks-2/manage/submissions"
echo "3. Submit a project → VisaFit → final Submit"
echo "4. Screenshot → $ART/submitted.png"
echo "5. Then:"
cat <<EOF
python3 sheet_planner.py remember --kind submitted --thread evohacks-2 \\
  --subject "EvoHacks 2: VisaFit submitted" \\
  --channel "web:evohacks2.devpost.com" \\
  --evidence "path:artifacts/2026-11-21/evohacks-2/submitted.png" \\
  --evidence "url:https://devpost.com/software/visafit-evohacks-2"
python3 sheet_planner.py done --match 173 --notes "VisaFit submitted; receipt in artifacts/2026-11-21/evohacks-2/"
python3 sheet_planner.py approve --match 173 --notes "Owner goal: submit; verified receipt"
EOF

# Open manage page for the human/session
open "https://devpost.com/submit-to/31721-evohacks-2/manage/submissions" 2>/dev/null || true
