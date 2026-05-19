from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .converter import convert as run_convert
from .discovery import discover
from .models import ReportEntry
from .safety import reject_user_claude_path

app = typer.Typer(no_args_is_help=True)
console = Console(width=200)


@app.command()
def inspect(
    source: Path = typer.Argument(
        Path("."),
        help="Claude Code project directory to inspect.",
    ),
) -> None:
    """Inspect project-local Claude Code assets."""
    try:
        source = reject_user_claude_path(source, "source")
        entries = discover(source)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    console.print(f"Inspecting {source}")
    _print_report(entries, source)


@app.command()
def convert(
    source: Path = typer.Argument(
        Path("."),
        help="Claude Code project directory to convert.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output project directory. Defaults to SOURCE.",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show planned writes without modifying files."),
    force: bool = typer.Option(False, "--force", help="Overwrite existing generated targets."),
) -> None:
    """Convert project-local Claude Code assets to Codex project files."""
    try:
        source = reject_user_claude_path(source, "source")
        output_root = reject_user_claude_path(output or source, "output")
        entries = run_convert(source, output_root, dry_run=dry_run, force=force)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    console.print(f"Converting {source} -> {output_root}")
    _print_report(entries, output_root)


def _print_report(entries: list[ReportEntry], root: Path) -> None:
    table = Table(title="Conversion Report")
    table.add_column("Status")
    table.add_column("Kind")
    table.add_column("Source", no_wrap=True)
    table.add_column("Target", no_wrap=True)
    table.add_column("Detail", no_wrap=True)
    for entry in sorted(entries, key=lambda item: (str(item.source), item.kind, item.status.value)):
        table.add_row(
            entry.status.value,
            entry.kind,
            _display_path(entry.source, root),
            _display_path(entry.target, root) if entry.target else "",
            entry.detail,
        )
    console.print(table)


def _display_path(path: Path | None, root: Path) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    app()
