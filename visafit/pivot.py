"""Apply the official EvoHacks theme to README + UI copy in one shot."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME_FILE = ROOT / "THEME.md"
README = ROOT / "README.md"
INDEX = ROOT / "visafit" / "static" / "index.html"


def apply_theme(theme: str) -> None:
    theme = " ".join(theme.split()).strip()
    if len(theme) < 8:
        raise SystemExit("theme text too short")

    # THEME.md
    body = THEME_FILE.read_text(encoding="utf-8")
    stamped = f"## Official theme (recorded)\n\n> {theme}\n\n"
    if "## Official theme" in body:
        body = re.sub(r"## Official theme \(recorded\)[\s\S]*?(?=\n## |\Z)", stamped, body)
    else:
        body = body.rstrip() + "\n\n" + stamped
    THEME_FILE.write_text(body, encoding="utf-8")

    # README Fit-to-Prompt block
    readme = README.read_text(encoding="utf-8")
    block = (
        f"> **Official theme:** {theme}\n>\n"
        "> VisaFit screens opportunities so builders spend the hack on the theme, "
        "not on dead-end eligibility.\n"
    )
    if "> **Official theme:**" in readme:
        readme = re.sub(r"> \*\*Official theme:\*\*[\s\S]*?(?=\n## |\nVisaFit|\Z)", block + "\n", readme)
    else:
        readme = readme.replace("# VisaFit\n", f"# VisaFit\n\n{block}\n", 1)
    README.write_text(readme, encoding="utf-8")

    # UI lede
    html = INDEX.read_text(encoding="utf-8")
    lede = (
        f"Theme: {theme}. Paste opportunity rules. Get eligible / skip / uncertain "
        "for a UK student-visa builder so you spend the hack on the theme, not dead ends."
    )
    html2, n = re.subn(
        r'(<p class="lede">)([\s\S]*?)(</p>)',
        rf"\1{lede}\3",
        html,
        count=1,
    )
    if n != 1:
        raise SystemExit("could not rewrite UI lede")
    INDEX.write_text(html2, encoding="utf-8")
    print("pivoted:", theme[:120])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Pivot VisaFit copy to the official theme")
    p.add_argument("theme", nargs="?", help="Theme text; omit to read THEME.md Official theme block")
    args = p.parse_args(argv)
    theme = args.theme
    if not theme:
        text = THEME_FILE.read_text(encoding="utf-8")
        m = re.search(r"## Official theme \(recorded\)\s*>\s*(.+)", text)
        if not m:
            raise SystemExit("pass theme text, or add ## Official theme (recorded) to THEME.md")
        theme = m.group(1).strip()
    apply_theme(theme)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
