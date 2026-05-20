from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.text import Text
from rich.table import Table

from .converter import clean as run_clean
from .converter import convert as run_convert
from .discovery import discover
from .models import ReportEntry
from .safety import reject_user_claude_path

app = typer.Typer(no_args_is_help=True)
console = Console(width=200, force_terminal=True, color_system="truecolor", no_color=False)
STATUS_STYLES = {
    "written": "green",
    "planned": "cyan",
    "convertible": "cyan",
    "skipped": "yellow",
    "unsupported": "magenta",
    "conflict": "red",
    "error": "bold red",
}


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
    console.print(f"Inspecting {source}", highlight=False)
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
    include_local_settings: bool = typer.Option(
        False,
        "--include-local-settings",
        help="Merge .claude/settings.local.json over .claude/settings.json.",
    ),
    gitignore: bool = typer.Option(False, "--gitignore", help="Append generated output paths to .gitignore."),
) -> None:
    """Convert project-local Claude Code assets to Codex project files."""
    try:
        source = reject_user_claude_path(source, "source")
        output_root = reject_user_claude_path(output or source, "output")
        entries = run_convert(
            source,
            output_root,
            dry_run=dry_run,
            force=force,
            include_local_settings=include_local_settings,
            update_gitignore=gitignore,
        )
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    console.print(f"Converting {source} -> {output_root}", highlight=False)
    _print_report(entries, output_root)


@app.command()
def clean(
    target: Path = typer.Argument(
        Path("."),
        help="Codex project directory to clean.",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show planned removals without deleting files."),
    force: bool = typer.Option(False, "--force", help="Remove known generated targets even without markers."),
) -> None:
    """Remove generated codex-converter output from a project."""
    try:
        target = reject_user_claude_path(target, "target")
        entries = run_clean(target, dry_run=dry_run, force=force)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    console.print(f"Cleaning {target}", highlight=False)
    _print_report(entries, target)


def _print_report(entries: list[ReportEntry], root: Path) -> None:
    console.print(_build_report_table(entries, root))


def _build_report_table(entries: list[ReportEntry], root: Path) -> Table:
    table = Table(
        title="Conversion Report",
        title_style="bold white",
        header_style="bold",
        border_style="dim",
    )
    table.add_column("Status")
    table.add_column("Kind", style="cyan")
    table.add_column("Source", style="bright_cyan", no_wrap=True)
    table.add_column("Target", style="green", no_wrap=True)
    table.add_column("Detail", style="dim white", no_wrap=True)
    for entry in sorted(entries, key=lambda item: (str(item.source), item.kind, item.status.value)):
        table.add_row(
            Text(entry.status.value, style=STATUS_STYLES.get(entry.status.value, "")),
            entry.kind,
            _display_path(entry.source, root),
            _display_path(entry.target, root) if entry.target else "",
            entry.detail,
        )
    return table


def _display_path(path: Path | None, root: Path) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    app()
