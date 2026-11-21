from pathlib import Path

from visafit.pivot import apply_theme


def test_apply_theme_rewrites_files(tmp_path, monkeypatch):
    root = tmp_path
    (root / "visafit" / "static").mkdir(parents=True)
    theme = root / "THEME.md"
    readme = root / "README.md"
    index = root / "visafit" / "static" / "index.html"
    theme.write_text("# Theme\n\nWaiting.\n")
    readme.write_text("# VisaFit\n\nHello.\n")
    index.write_text('<p class="lede">Old lede</p>\n')

    import visafit.pivot as pivot

    monkeypatch.setattr(pivot, "ROOT", root)
    monkeypatch.setattr(pivot, "THEME_FILE", theme)
    monkeypatch.setattr(pivot, "README", readme)
    monkeypatch.setattr(pivot, "INDEX", index)

    apply_theme("Build tools that help students learn faster")
    assert "Official theme" in theme.read_text()
    assert "Build tools that help students learn faster" in readme.read_text()
    assert "Build tools that help students learn faster" in index.read_text()
