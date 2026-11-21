"""Apply the official EvoHacks theme to README + UI copy in one shot."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME_FILE = ROOT / "THEME.md"
README = ROOT / "README.md"
INDEX = ROOT / "visafit" / "static" / "index.html"
DOCS_INDEX = ROOT / "docs" / "index.html"
DEVPOST_ABOUT = ROOT / "docs" / "DEVPOST_ABOUT.md"


def _paths() -> dict[str, Path]:
    """Resolve paths from ROOT so tests can monkeypatch ROOT alone."""
    return {
        "theme": ROOT / "THEME.md",
        "readme": ROOT / "README.md",
        "index": ROOT / "visafit" / "static" / "index.html",
        "docs_index": ROOT / "docs" / "index.html",
        "devpost_about": ROOT / "docs" / "DEVPOST_ABOUT.md",
    }


def _rewrite_lede(path: Path, lede: str) -> None:
    html = path.read_text(encoding="utf-8")
    html2, n = re.subn(
        r'(<p class="lede">)([\s\S]*?)(</p>)',
        rf"\1{lede}\3",
        html,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"could not rewrite UI lede in {path}")
    path.write_text(html2, encoding="utf-8")


def apply_theme(theme: str) -> None:
    theme = " ".join(theme.split()).strip()
    if len(theme) < 8:
        raise SystemExit("theme text too short")

    p = _paths()
    theme_file, readme_path, index_path = p["theme"], p["readme"], p["index"]
    docs_index, about_path = p["docs_index"], p["devpost_about"]

    # THEME.md
    body = theme_file.read_text(encoding="utf-8")
    stamped = f"## Official theme (recorded)\n\n> {theme}\n\n"
    if "## Official theme" in body:
        body = re.sub(r"## Official theme \(recorded\)[\s\S]*?(?=\n## |\Z)", stamped, body)
    else:
        body = body.rstrip() + "\n\n" + stamped
    theme_file.write_text(body, encoding="utf-8")

    # README Fit-to-Prompt block
    readme = readme_path.read_text(encoding="utf-8")
    block = (
        f"> **Official theme:** {theme}\n>\n"
        "> VisaFit screens opportunities so builders spend the hack on the theme, "
        "not on dead-end eligibility.\n"
    )
    if "> **Official theme:**" in readme:
        readme = re.sub(r"> \*\*Official theme:\*\*[\s\S]*?(?=\n## |\nVisaFit|\Z)", block + "\n", readme)
    else:
        readme = readme.replace("# VisaFit\n", f"# VisaFit\n\n{block}\n", 1)
    readme_path.write_text(readme, encoding="utf-8")

    lede = (
        f"Theme: {theme}. Paste opportunity rules. Get eligible / skip / uncertain "
        "for a UK student-visa builder so you spend the hack on the theme, not dead ends."
    )
    _rewrite_lede(index_path, lede)
    if docs_index.exists():
        _rewrite_lede(docs_index, lede)

    # Paste-ready Devpost About blurb after pivot
    about_path.parent.mkdir(parents=True, exist_ok=True)
    about_path.write_text(
        (
            f"## Inspiration\n\n"
            f"Official EvoHacks 2 theme: **{theme}**\n\n"
            "International students waste nights on opportunities that quietly exclude them. "
            "VisaFit pastes official rules and returns eligible / skip / uncertain with hard "
            "reason codes for a UK student-visa, final-year, London profile, so builders spend "
            "the hack on the theme instead of dead-end eligibility.\n\n"
            "## How it works\n\n"
            "1. Paste rules text\n"
            "2. Confirm profile flags\n"
            "3. Get a verdict + reason codes\n\n"
            "## Try it\n\n"
            "- Live: https://shahaman098.github.io/visafit-evohacks-2/\n"
            "- Repo: https://github.com/shahaman098/visafit-evohacks-2\n"
            "- Demo video: https://youtu.be/03YcRirbqIA\n"
        ),
        encoding="utf-8",
    )
    print("pivoted:", theme[:120])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Pivot VisaFit copy to the official theme")
    p.add_argument("theme", nargs="?", help="Theme text; omit to read THEME.md Official theme block")
    args = p.parse_args(argv)
    theme = args.theme
    if not theme:
        text = _paths()["theme"].read_text(encoding="utf-8")
        m = re.search(r"## Official theme \(recorded\)\s*>\s*(.+)", text)
        if not m:
            raise SystemExit("pass theme text, or add ## Official theme (recorded) to THEME.md")
        theme = m.group(1).strip()
    apply_theme(theme)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
