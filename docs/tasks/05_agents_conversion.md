# Task 05: Agents Conversion

## Goal

Convert Claude Code project subagents into Codex custom agent TOML files.

## Scope

- Read `.claude/agents/*.md`.
- Parse YAML frontmatter and Markdown body.
- Write `.codex/agents/<name>.toml`.
- Map Claude body content to Codex `developer_instructions`.
- Populate required Codex fields:
  - `name`
  - `description`
  - `developer_instructions`
- Respect `--dry-run` and `--force`.

## Out of Scope

- User-scoped agents under `~/.claude/agents`.
- Converting unavailable or unverified Claude-only fields.
- Running converted agents.

## Checklist

- [ ] Agent Markdown files are parsed.
- [ ] YAML frontmatter parsing handles normal quoted and multiline values.
- [ ] Missing required Codex fields are reported clearly.
- [ ] TOML output is valid.
- [ ] Body content maps to `developer_instructions`.
- [ ] Existing output conflicts are handled consistently.

## Success Criteria

- Each valid Claude project agent becomes one Codex TOML agent file.
- Invalid agent files produce clear report entries instead of partial output.
- The converter does not inspect user-scoped agent directories.

## Expected Unit Tests

- Test a valid Claude agent converts to TOML.
- Test body content appears in `developer_instructions`.
- Test missing description is reported.
- Test invalid YAML frontmatter is reported.
- Test TOML output can be parsed after conversion.
- Test dry run does not create `.codex/agents`.
