from pathlib import Path

from visafit.pivot import apply_theme


def test_apply_theme_rewrites_files(tmp_path, monkeypatch):
    root = tmp_path
    (root / "visafit" / "static").mkdir(parents=True)
    (root / "docs").mkdir(parents=True)
    theme = root / "THEME.md"
    readme = root / "README.md"
    index = root / "visafit" / "static" / "index.html"
    docs_index = root / "docs" / "index.html"
    theme.write_text("# Theme\n\nWaiting.\n")
    readme.write_text("# VisaFit\n\nHello.\n")
    index.write_text('<p class="lede">Old lede</p>\n')
    docs_index.write_text('<p class="lede">Old pages lede</p>\n')

    import visafit.pivot as pivot

    monkeypatch.setattr(pivot, "ROOT", root)

    apply_theme("Build tools that help students learn faster")
    assert "Official theme" in theme.read_text()
    assert "Build tools that help students learn faster" in readme.read_text()
    assert "Build tools that help students learn faster" in index.read_text()
    assert "Build tools that help students learn faster" in docs_index.read_text()
    about = (root / "docs" / "DEVPOST_ABOUT.md").read_text()
    assert "Official EvoHacks 2 theme" in about
    assert "Build tools that help students learn faster" in about
