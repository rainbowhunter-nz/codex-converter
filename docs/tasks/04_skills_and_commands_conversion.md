# Task 04: Skills and Commands Conversion

## Goal

Convert project-scoped Claude Code skills and commands into Codex skills.

## Scope

- Copy `.claude/skills/<name>/` to `.agents/skills/<name>/`.
- Preserve supporting files inside each skill directory.
- Normalize `SKILL.md` frontmatter so required Codex `name` and `description` fields exist.
- Convert `.claude/commands/<name>.md` into `.agents/skills/<name>/SKILL.md`.
- Respect `--dry-run` and `--force`.

## Out of Scope

- User-scoped skills under `~/.claude/skills`.
- Semantic rewriting of skill instructions.
- Plugin or marketplace conversion.

## Checklist

- [ ] Project skills are copied to `.agents/skills`.
- [ ] Skill supporting files are preserved.
- [ ] Missing skill `name` frontmatter is added.
- [ ] Missing skill `description` frontmatter is added with a conservative generated value.
- [ ] Claude commands become Codex skills.
- [ ] Existing output conflicts are reported unless `--force` is set.

## Success Criteria

- Each converted Codex skill has a valid `SKILL.md`.
- Existing unrelated files are not overwritten by default.
- The conversion is deterministic and does not call a model.

## Expected Unit Tests

- Test a full skill directory is copied.
- Test supporting files remain under the converted skill directory.
- Test frontmatter with missing `name` is normalized.
- Test frontmatter with missing `description` is normalized.
- Test a command markdown file becomes a skill directory with `SKILL.md`.
- Test overwrite conflict behavior.
