from visafit.__main__ import main


def test_cli_eligible(tmp_path, capsys):
    f = tmp_path / "rules.txt"
    f.write_text(
        "Open to university students worldwide. Remote online hackathon. "
        "United Kingdom residents welcome. Submit on Devpost."
    )
    assert main([str(f)]) == 0
    out = capsys.readouterr().out
    assert "ELIGIBLE" in out
