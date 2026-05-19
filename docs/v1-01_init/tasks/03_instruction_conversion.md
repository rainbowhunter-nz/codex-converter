# Task 03: Instruction File Conversion

## Goal

Convert Claude Code `CLAUDE.md` files into Codex `AGENTS.md` files.

## Scope

- Convert root `CLAUDE.md` to root `AGENTS.md`.
- Convert nested `CLAUDE.md` files to nested `AGENTS.md` files.
- Preserve relative directory structure.
- Treat `CLAUDE.md` as the truth when an `AGENTS.md` already exists.
- Add a generated header that records the source file.
- Respect `--dry-run` and `--force`.

## Out of Scope

- Merging existing `AGENTS.md` content.
- Converting skills, commands, agents, or settings.

## Checklist

- [x] Root instruction conversion works.
- [x] Nested instruction conversion works.
- [x] Existing `AGENTS.md` handling follows the accepted proposal decision.
- [x] `--dry-run` reports planned writes without writing files.
- [x] `--force` overwrites generated targets when requested.

## Success Criteria

- Converted instruction files are deterministic.
- Dry runs do not modify the filesystem.
- Output paths never escape the selected output directory.

## Expected Unit Tests

- Test root `CLAUDE.md` produces `AGENTS.md`.
- Test nested `subdir/CLAUDE.md` produces `subdir/AGENTS.md`.
- Test generated header includes the source path.
- Test dry run creates no files.
- Test output path traversal is blocked.
- Test existing `AGENTS.md` behavior matches the proposal decision.
