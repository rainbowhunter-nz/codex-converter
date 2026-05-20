# Task 05: README and Acceptance Sweep

## Goal

Update user-facing documentation and perform the final acceptance sweep for the feedback release.

## Scope

- Update README usage examples for:
  - `--include-local-settings`
  - `--gitignore`
  - `clean`
- Update the converted files table if config behavior changes.
- Update unsupported or skipped notes to explain the default skip behavior for `.claude/settings.local.json`.
- Confirm unsupported hooks, MCP servers, plugins, auth, trust, marketplace, and unknown settings remain documented.
- Run the full verification suite expected by this project.
- Fix only documentation or small integration issues discovered during the acceptance sweep.

## Suggested Files

- `README.md`
- `tests/test_cli.py`
- Other files only for small integration fixes discovered during verification.

## Assumptions

- This task should run after Tasks 01 through 04.
- README should document actual shipped behavior, not future behavior.
- If verification finds a substantial implementation bug, create a focused follow-up rather than mixing a large fix into this task.

## Success Criteria

- [ ] README shows `convert --include-local-settings`.
- [ ] README shows `convert --gitignore`.
- [ ] README shows `clean`, `clean --dry-run`, and `clean --force`.
- [ ] README explains `.claude/settings.local.json` is skipped unless explicitly included.
- [ ] README explains generated outputs can be ignored with `--gitignore`.
- [ ] README explains cleanup is conservative and marker-based by default.
- [ ] Full project tests pass.
- [ ] Lint and type checks pass if they are part of the current project workflow.

## Expected Unit Tests

- [ ] No README-only tests are required.
- [ ] Run `uv run pytest`.
- [ ] Run `uv run ruff check .`.
- [ ] Run `uv run mypy .`.

