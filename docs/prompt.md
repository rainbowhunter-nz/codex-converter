# V1 Implementation Prompt

You are the main implementation agent for `codex_converter`. Complete the V1 converter described in `docs/proposal.md` and `docs/tasks/*.md` without further user interruption unless a requirement is genuinely ambiguous or unsafe.

## Current Project Context

The project goal is to build a Python CLI that converts project-scoped Claude Code workspace configuration into Codex CLI-compatible project configuration.

Scope is project-local only. The converter must never read from or write to user-scoped Claude Code paths such as `~/.claude/settings.json`, `~/.claude/skills`, or `~/.claude/agents`.

Primary inputs:

- `docs/proposal.md`
- `docs/progress.md`
- `docs/tasks/01_project_scaffold.md`
- `docs/tasks/02_discovery_and_report.md`
- `docs/tasks/03_instruction_conversion.md`
- `docs/tasks/04_skills_and_commands_conversion.md`
- `docs/tasks/05_agents_conversion.md`
- `docs/tasks/06_settings_and_safety.md`
- `docs/tasks/07_end_to_end_and_docs.md`

Current repository notes:

- `docs/progress.md` says Task 01 has been implemented.
- Verify the actual scaffold before relying on that note. At prompt creation time, `main.py` imports `codex_converter.cli`, but the package files may need to be created or restored.
- Keep implementation minimal and aligned with the task files. Do not add speculative features.

## Required V1 Behavior

Implement these commands with `typer` and `rich`:

```text
codex-converter inspect [SOURCE]
codex-converter convert [SOURCE] [--output PATH] [--dry-run] [--force]
```

`inspect` must discover project-local Claude Code assets and print a deterministic Rich table showing each asset and whether it is convertible, skipped, unsupported, or conflicted.

`convert` must write Codex-compatible project files into the selected output directory, respecting `--dry-run` and `--force`.

Default behavior:

- `SOURCE` defaults to the current working directory.
- `--output` defaults to `SOURCE`.
- `.codex/config.toml` is created by default.
- Existing generated targets are not overwritten unless `--force` is set.
- `.claude/settings.local.json` is skipped by default and reported.

## Conversion Requirements

Convert only these project-scoped inputs:

- `CLAUDE.md` to `AGENTS.md`, including nested `CLAUDE.md` files.
- `.claude/skills/<name>/` to `.agents/skills/<name>/`.
- `.claude/commands/<name>.md` to `.agents/skills/<name>/SKILL.md`.
- `.claude/agents/<name>.md` to `.codex/agents/<name>.toml`.
- `.claude/settings.json` to safe `.codex/config.toml` output where a mapping is verified.

Report but do not guess at unsafe or unsupported areas:

- hooks
- plugins
- MCP configuration
- unsupported Claude settings
- `.claude/settings.local.json`
- user-scoped Claude assets

Instruction conversion details:

- Add a generated header to each `AGENTS.md` that records the source `CLAUDE.md` path.
- Preserve relative directory structure.
- Treat `CLAUDE.md` as the truth. Do not merge existing `AGENTS.md` content.
- Without `--force`, existing outputs must be reported as conflicts and left untouched.

Skill and command conversion details:

- Preserve supporting files in skill directories.
- Ensure every converted `SKILL.md` has frontmatter with `name` and `description`.
- If `description` is missing, generate a conservative deterministic description.
- Convert command Markdown files into skill directories named from the command file stem.
- Do not semantically rewrite skill or command instructions.

Agent conversion details:

- Read only `.claude/agents/*.md` under the selected source tree.
- Parse YAML frontmatter and Markdown body.
- Write valid TOML under `.codex/agents/<name>.toml`.
- Required Codex fields are `name`, `description`, and `developer_instructions`.
- Map the Markdown body to `developer_instructions`.
- Invalid or incomplete agent files must produce clear report entries, not partial output files.

Settings and safety details:

- Enforce output path containment for every planned write.
- Reject or ignore any source path under `~/.claude`.
- Create `.codex/config.toml` by default even when no safe Claude setting is converted.
- Unsupported settings must appear in the conversion report.
- Do not convert hooks, MCP servers, plugins, auth, trust, or marketplace configuration unless the mapping is direct, verified, and safe.

## Suggested Implementation Order

Use subagents for bounded tasks where helpful. The main agent is responsible for assembling context, avoiding duplicated work, integrating results, and verifying the final system.

Recommended task split:

1. Project scaffold: verify or create package layout, CLI entrypoint, dependencies, and baseline tests.
2. Discovery and report model: implement asset discovery, status classification, path safety helpers, and Rich table output.
3. Instruction conversion: implement `CLAUDE.md` to `AGENTS.md`, dry-run, force, and conflict handling.
4. Skills and commands conversion: implement skill directory copying, frontmatter normalization, and command-to-skill conversion.
5. Agents conversion: implement YAML frontmatter parsing and TOML agent output.
6. Settings and safety: implement default `.codex/config.toml`, unsupported setting reporting, and containment enforcement.
7. End-to-end tests and README: add realistic fixtures, CLI coverage, and user documentation.

Before assigning a subagent, provide it with:

- the relevant task file contents;
- the relevant proposal sections;
- the current module boundaries;
- the exact files or modules it owns;
- the tests it must add or update;
- a requirement to run the focused tests before finishing.

Tell subagents they are not alone in the codebase. They must not revert edits made by others and must keep their work within their assigned files or responsibility area.

## Verification Requirements

All Python code must pass:

```text
uv run pytest
uv run ruff check .
uv run mypy .
```

If `ruff` or `mypy` are not yet configured or installed, add the minimal project configuration/dependencies needed for these commands to run. Keep configuration strict enough to be useful but do not over-engineer it.

Add focused unit tests from each task file. Also add end-to-end tests for:

- `inspect` on a realistic Claude Code fixture;
- `convert --dry-run` writing no files;
- `convert` creating the expected Codex file tree;
- rerunning without `--force` reporting conflicts;
- rerunning with `--force` updating generated outputs.

## Progress Updates

After each task is complete:

- tick off the completed checklist items in the corresponding `docs/tasks/*.md` file;
- tick off the task in `docs/progress.md`;
- add a concise note to `docs/progress.md` if there is important implementation context or a known limitation.

Do not mark a task complete until its implementation and tests pass.

## Constraints

- Prefer simple, deterministic transforms over model-generated rewrites.
- Keep code self-explanatory and comments sparse.
- Do not implement features beyond V1.
- Do not read or write outside the selected source/output trees except for normal project tooling.
- Do not mutate user-scoped Claude Code configuration.
- Do not hide unsupported behavior. Report it clearly.

## Final Deliverable

Finish with:

- all task files and `docs/progress.md` updated;
- README usage documentation updated;
- all required tests passing;
- a concise summary of implemented behavior, known unsupported conversions, and verification commands run.
