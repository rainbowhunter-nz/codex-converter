# Task 02: Discovery and Report Model

## Goal

Implement project-local Claude Code asset discovery and a structured report model used by both `inspect` and `convert`.

## Scope

- Discover these project-local assets:
  - `CLAUDE.md` files, including nested files.
  - `.claude/skills/<name>/SKILL.md`.
  - `.claude/commands/*.md`.
  - `.claude/agents/*.md`.
  - `.claude/settings.json`.
  - `.claude/settings.local.json`.
- Classify each asset as `convertible`, `skipped`, `unsupported`, or `conflict`.
- Explicitly skip user-scoped paths such as `~/.claude`.
- Add rich table output for `inspect`.

## Out of Scope

- Writing output files.
- Parsing skill or agent frontmatter.
- Converting settings into TOML.

## Checklist

- [ ] Discovery walks only under the selected source directory.
- [ ] Nested `CLAUDE.md` files are found.
- [ ] Project skills, commands, agents, and settings files are identified.
- [ ] `.claude/settings.local.json` is reported as skipped by default.
- [ ] `inspect` prints a readable Rich table.

## Success Criteria

- `inspect` gives a deterministic inventory of convertible and skipped files.
- Discovery does not read outside the source directory.
- User-scoped Claude settings are never inspected.

## Expected Unit Tests

- Test discovery finds root and nested `CLAUDE.md`.
- Test discovery finds `.claude/skills/name/SKILL.md`.
- Test discovery finds `.claude/commands/name.md`.
- Test discovery finds `.claude/agents/name.md`.
- Test `.claude/settings.local.json` is marked skipped.
- Test paths outside the source root are rejected or ignored.
