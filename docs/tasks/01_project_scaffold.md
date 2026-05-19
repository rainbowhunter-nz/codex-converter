# Task 01: Project Scaffold

## Goal

Set up the Python package structure and CLI entrypoint for the converter.

## Scope

- Add runtime dependencies: `typer`, `rich`, `tomli-w`, and `pyyaml`.
- Add test dependency if needed.
- Replace the placeholder `main.py` with a minimal Typer app.
- Provide two commands:
  - `inspect [SOURCE]`
  - `convert [SOURCE] --output PATH --dry-run --force`
- Add packaging metadata so the command can be run through `uv`.

## Out of Scope

- Real conversion logic.
- File discovery beyond a placeholder call boundary.
- Writing Codex output files.

## Checklist

- [ ] Dependencies are declared in `pyproject.toml`.
- [ ] Typer CLI starts without import errors.
- [ ] `inspect --help` and `convert --help` render successfully.
- [ ] CLI command names and options match `docs/proposal.md`.
- [ ] Package can be run with `uv run`.

## Success Criteria

- A user can run the CLI and see command help.
- The CLI has stable function boundaries for later discovery and conversion tasks.
- No user-scoped Claude paths are accessed.

## Expected Unit Tests

- Test the CLI root help exits with code `0`.
- Test `inspect --help` exits with code `0`.
- Test `convert --help` exits with code `0`.
- Test default source path is the current working directory.
