"""CLI: python -m visafit path/to/rules.txt"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from visafit.engine import Profile, screen


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Screen opportunity rules for UK student-visa fit")
    p.add_argument("rules", nargs="?", help="Path to rules text (default: stdin)")
    p.add_argument("--json", action="store_true", help="Print JSON verdict")
    p.add_argument("--travel", action="store_true", help="Profile will travel abroad")
    p.add_argument("--not-final-year", action="store_true")
    args = p.parse_args(argv)

    if args.rules:
        text = Path(args.rules).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    profile = Profile(
        final_year=not args.not_final_year,
        will_travel_abroad=args.travel,
    )
    verdict = screen(text, profile)
    if args.json:
        print(json.dumps(verdict.to_dict(), indent=2))
    else:
        print(verdict.status.upper(), "-", verdict.summary)
        for r in verdict.reasons:
            print(f"  [{r.severity}] {r.code}: {r.detail}")
    return 0 if verdict.status != "skip" else 2


if __name__ == "__main__":
    raise SystemExit(main())
