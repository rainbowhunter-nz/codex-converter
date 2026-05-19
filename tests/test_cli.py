from pathlib import Path

from typer.testing import CliRunner

from codex_converter.cli import app


runner = CliRunner()


def test_root_help_exits_successfully() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "inspect" in result.output
    assert "convert" in result.output


def test_inspect_help_exits_successfully() -> None:
    result = runner.invoke(app, ["inspect", "--help"])

    assert result.exit_code == 0
    assert "Claude Code project directory to inspect" in result.output


def test_convert_help_exits_successfully() -> None:
    result = runner.invoke(app, ["convert", "--help"])

    assert result.exit_code == 0
    assert "--dry-run" in result.output
    assert "--force" in result.output


def test_inspect_default_source_is_current_directory() -> None:
    with runner.isolated_filesystem():
        cwd = Path.cwd().resolve()

        result = runner.invoke(app, ["inspect"])

        assert result.exit_code == 0
        assert f"Inspecting {cwd}" in result.output
