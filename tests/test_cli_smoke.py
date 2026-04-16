from __future__ import annotations

from typer.testing import CliRunner

from greenscreen.cli import app

runner = CliRunner()


def test_help() -> None:
    r = runner.invoke(app, ["--help"])
    assert r.exit_code == 0
    assert "convert" in r.stdout


def test_convert_help() -> None:
    r = runner.invoke(app, ["convert", "--help"])
    assert r.exit_code == 0
