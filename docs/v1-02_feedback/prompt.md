# V1.02 Feedback Implementation Prompt

You are the main implementation agent for `codex_converter`. Complete the V1.02 feedback release described in `docs/v1-02_feedback/proposal.md` and `docs/v1-02_feedback/tasks/*.md` without further user interruption unless a requirement is genuinely ambiguous or unsafe.

The main agent is the supervisor. Use subagents for bounded implementation tasks where useful, but the main agent owns task context, integration, verification, and progress tracking.

## Current Project Context

`codex-converter` is a Python CLI that converts project-scoped Claude Code workspace files into Codex CLI-compatible project files.

The project already has a working V1 implementation with:

- `codex-converter inspect [SOURCE]`
- `codex-converter convert [SOURCE] [--output PATH] [--dry-run] [--force]`
- conversion of `CLAUDE.md` to `AGENTS.md`, including nested files
- conversion of `.claude/skills/<name>/` to `.agents/skills/<name>/`
- conversion of `.claude/commands/<name>.md` to `.agents/skills/<name>/SKILL.md`
- conversion of `.claude/agents/<name>.md` to `.codex/agents/<name>.toml`
- default `.codex/config.toml` creation
- conservative reporting for unsupported Claude settings
- safety checks rejecting user-scoped Claude paths under `~/.claude`

At prompt creation time, the relevant code is concentrated in:

- `codex_converter/cli.py`: Typer commands and Rich report table
- `codex_converter/converter.py`: conversion orchestration and file writes
- `codex_converter/discovery.py`: project asset discovery and unsupported setting reports
- `codex_converter/models.py`: `Status` and `ReportEntry`
- `codex_converter/safety.py`: path containment and user-scoped Claude path rejection
- `tests/test_cli.py`: current CLI, discovery, conversion, and safety tests

Current verified gaps:

- `.claude/settings.local.json` is discovered but always skipped.
- `.codex/config.toml` is generated as a minimal placeholder.
- Conversion report statuses are plain text in the Rich table.
- There is no `convert --gitignore` flag.
- There is no `clean` command.

## Primary Inputs

Read these files before implementing:

- `docs/v1-02_feedback/proposal.md`
- `docs/v1-02_feedback/progress.md`
- `docs/v1-02_feedback/tasks/01_settings_merge_and_toml.md`
- `docs/v1-02_feedback/tasks/02_report_and_output_review.md`
- `docs/v1-02_feedback/tasks/03_gitignore_flag.md`
- `docs/v1-02_feedback/tasks/04_clean_command.md`
- `docs/v1-02_feedback/tasks/05_readme_and_acceptance_sweep.md`

Also inspect the current implementation and tests before assigning work or editing files. Do not rely on the task files alone.

## Required V1.02 Behavior

Extend `convert` to support:

```text
codex-converter convert [SOURCE] [--output PATH] [--dry-run] [--force] [--include-local-settings] [--gitignore]
```

Add:

```text
codex-converter clean [TARGET] [--dry-run] [--force]
```

Keep all existing V1 behavior unless the V1.02 task files explicitly change it.

## Task 01: Settings Merge and Readable TOML

Implement opt-in `.claude/settings.local.json` conversion and readable TOML generation.

Requirements:

- Add `--include-local-settings` to `convert`.
- Keep `.claude/settings.local.json` skipped by default.
- Load `.claude/settings.json` as base settings when present.
- When `--include-local-settings` is set and `.claude/settings.local.json` exists, merge local settings over base settings.
- Merge matching object values recursively.
- Replace arrays, strings, booleans, numbers, and nulls with the local value.
- Report invalid JSON for either settings file without crashing the conversion.
- Generate `.codex/config.toml` from the resulting settings data rather than only a placeholder.
- Keep unsupported hooks, MCP servers, plugins, auth, trust, marketplace, and unknown settings reported as unsupported.
- Keep generated TOML parseable by `tomllib`.
- Target a maximum generated TOML line length of 120 characters.

Implementation notes:

- There are no currently verified safe direct mappings for Claude settings. Stay conservative.
- It is acceptable for unsupported settings to be preserved only as report entries if no safe Codex mapping exists, but the generated config must remain valid TOML and more reviewable than the current placeholder.
- Prefer a small helper scoped to the generated config shapes over a broad TOML pretty-printer.

Expected tests:

- default conversion reports `settings.local` as skipped and does not merge local settings
- `--include-local-settings` merges local values over base values
- recursive object merge preserves unrelated base keys
- local arrays and scalars replace base arrays and scalars
- invalid base settings JSON reports an error and does not write invalid config
- invalid local settings JSON reports an error when `--include-local-settings` is used
- generated config parses with `tomllib`
- generated TOML has no line over 120 characters for long arrays or nested values

## Task 02: Report Styling and Output Review

Make generated output easier to review without adding unsupported conversions.

Requirements:

- Add status-specific Rich styles to report status cells:

| Status | Style |
| --- | --- |
| `written` | `green` |
| `planned` | `cyan` |
| `convertible` | `cyan` |
| `skipped` | `yellow` |
| `unsupported` | `magenta` |
| `conflict` | `red` |
| `error` | `bold red` |

- Keep plain text readable when ANSI color is disabled or stripped.
- Make generated headers consistent, concise, and still identifiable as `codex-converter` output.
- Improve report details for default config creation versus settings-derived config conversion.
- Review generated config, agent, command, skill, and instruction output for small clarity improvements only.
- Do not add new conversion mappings for unsupported Claude settings.

Expected tests:

- report rendering still includes unstyled status text after `click.unstyle`
- direct or CLI rendering coverage verifies styles are attached to status cells
- generated instruction headers include the source path and `codex-converter`
- config conversion details differ for default config creation and settings conversion

## Task 03: Gitignore Flag

Add an opt-in `--gitignore` conversion flag that appends generated output paths to the output project's `.gitignore`.

Requirements:

- Add `--gitignore` to `convert`.
- Append generated top-level output paths to `<output>/.gitignore`:
  - `AGENTS.md`
  - `.agents/`
  - `.codex/`
- For nested `CLAUDE.md` conversions, also append generated nested `AGENTS.md` paths.
- Avoid duplicate entries.
- Preserve existing `.gitignore` content.
- Respect `--dry-run` by reporting planned `.gitignore` changes without writing.
- Do not let `--force` make `.gitignore` updates destructive.
- Apply this to the output directory, not the source directory, when `--output` is supplied.

Expected tests:

- `--gitignore` creates `.gitignore` when missing
- `--gitignore` appends entries to an existing `.gitignore`
- running conversion with `--gitignore --force` twice does not duplicate entries
- nested `CLAUDE.md` produces a nested `AGENTS.md` ignore entry
- `--dry-run --gitignore` leaves `.gitignore` unchanged and reports a planned entry
- `--output <path> --gitignore` updates the output project's `.gitignore`
- conversion without `--gitignore` does not modify `.gitignore`

## Task 04: Clean Command

Add safe cleanup for generated converter output.

Command:

```text
codex-converter clean [TARGET] [--dry-run] [--force]
```

Requirements:

- Default `TARGET` to the current directory.
- Reject user-scoped Claude paths under `~/.claude`.
- Never remove source Claude files.
- Never remove files outside `TARGET`.
- By default, remove only files that contain or can be verified from a `codex-converter` generated marker.
- With `--force`, remove known generated target paths inside `TARGET` even when a marker is missing.
- Remove empty generated directories after generated files are removed.
- Do not remove `.agents/`, `.agents/skills/`, `.codex/`, or `.codex/agents/` if they still contain non-generated files.
- Remove `.gitignore` entries added by `--gitignore`, while preserving unrelated `.gitignore` content.
- Respect `--dry-run` by reporting planned removals without deleting anything.

Generated targets:

- root `AGENTS.md`
- nested `AGENTS.md` files generated from nested `CLAUDE.md` files
- `.agents/skills/<converted-skill>/`
- `.codex/agents/<converted-agent>.toml`
- `.codex/config.toml`

Expected tests:

- root help includes `clean`
- `clean --help` documents `TARGET`, `--dry-run`, and `--force`
- `clean --dry-run` after conversion reports removals and leaves files in place
- `clean` after conversion removes generated `AGENTS.md`, `.codex/config.toml`, converted agents, and converted skills
- unmarked `AGENTS.md` is preserved without `--force`
- `clean --force` removes an unmarked known generated target path inside the target
- source `CLAUDE.md` remains after cleanup
- a non-generated file under `.codex/agents/` prevents the directory from being removed
- generated `.gitignore` entries are removed while unrelated entries remain
- attempts to clean `~/.claude` are rejected

## Task 05: README and Acceptance Sweep

Update documentation and run final verification after Tasks 01 through 04 are complete.

Requirements:

- Update README usage examples for:
  - `convert --include-local-settings`
  - `convert --gitignore`
  - `clean`
  - `clean --dry-run`
  - `clean --force`
- Update the converted files table if config behavior changes.
- Explain that `.claude/settings.local.json` is skipped unless explicitly included.
- Explain generated outputs can be ignored with `--gitignore`.
- Explain cleanup is conservative and marker-based by default.
- Confirm unsupported hooks, MCP servers, plugins, auth, trust, marketplace, and unknown settings remain documented.
- Run the full verification suite.
- Fix documentation or small integration issues found during the final sweep.

Expected verification:

```text
uv run pytest
uv run ruff check .
uv run mypy .
```

## Subagent Guidance

Before assigning a subagent, provide:

- the relevant task file contents or a concise task-specific excerpt
- the relevant proposal sections
- current module boundaries
- the exact files or responsibility area it owns
- the focused tests it must add or update
- a requirement to run focused tests before finishing

Tell every subagent:

- You are not alone in the codebase.
- Do not revert edits made by others.
- Keep changes within your assigned ownership area.
- Make sure focused tests pass before finishing.
- Report the files changed and tests run.

Suggested parallel split:

- Worker 1: settings merge, readable config TOML, and focused tests.
- Worker 2: report styling and generated output review.
- Worker 3: gitignore flag behavior and tests.
- Worker 4: clean command behavior and tests.

Keep Task 05 for the main agent after integrating all implementation tasks.

Avoid overlapping writes where possible. If multiple workers need `cli.py`, coordinate carefully through the main agent before final integration.

## Progress Tracking

After each task is fully implemented and verified:

- tick off completed checklist items in the corresponding `docs/v1-02_feedback/tasks/*.md` file
- tick off the task in `docs/v1-02_feedback/progress.md`
- add a concise progress note only when there is important implementation context or a known limitation

Do not mark a task complete until its implementation and tests pass.

## Constraints

- Keep the implementation minimal and deterministic.
- Do not add speculative mappings or features.
- Prefer self-explanatory code over comments.
- Keep comments sparse and only where they clarify non-obvious safety or formatting logic.
- Do not read or write outside the selected source/output trees except for normal project tooling.
- Do not mutate user-scoped Claude Code configuration.
- Do not remove user-authored Codex files during cleanup unless `--force` applies to a known generated target path inside `TARGET`.
- Preserve unsupported behavior clearly in reports and documentation.

## Final Deliverable

Finish with:

- all V1.02 task files and `docs/v1-02_feedback/progress.md` updated
- README usage documentation updated
- all required tests passing
- a concise summary of implemented behavior, unsupported conversions that remain unsupported, and verification commands run
