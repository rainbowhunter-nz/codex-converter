# Task 03: Gitignore Flag

## Goal

Add an opt-in `--gitignore` conversion flag that appends converter-generated output paths to the output project's `.gitignore`.

## Scope

- Add `--gitignore` to `codex-converter convert`.
- Append generated top-level output paths to `<output>/.gitignore`:
  - `AGENTS.md`
  - `.agents/`
  - `.codex/`
- For nested `CLAUDE.md` conversions, also append the generated nested `AGENTS.md` paths.
- Avoid duplicate entries.
- Preserve existing `.gitignore` content.
- Respect `--dry-run` by reporting planned `.gitignore` changes without writing.
- Keep `--force` scoped to generated target conflicts; `.gitignore` updates should remain non-destructive.

## Suggested Files

- `codex_converter/cli.py`
- `codex_converter/converter.py`
- `codex_converter/models.py`
- `tests/test_cli.py`

## Assumptions

- The flag applies to the output directory, not the source directory when `--output` is supplied.
- Appended entries should be simple `.gitignore` patterns, not absolute paths.
- Existing comments and formatting in `.gitignore` should be preserved as much as practical.

## Success Criteria

- [ ] `convert` help shows `--gitignore`.
- [ ] `--gitignore` appends generated output paths to `<output>/.gitignore`.
- [ ] Existing `.gitignore` content is preserved.
- [ ] Existing matching entries are not duplicated.
- [ ] Nested generated `AGENTS.md` paths are included.
- [ ] `--dry-run --gitignore` reports the planned update and writes nothing.
- [ ] Conversion without `--gitignore` does not modify `.gitignore`.
- [ ] Existing conversion behavior still passes.

## Expected Unit Tests

- [ ] `--gitignore` creates `.gitignore` when missing.
- [ ] `--gitignore` appends entries to an existing `.gitignore`.
- [ ] Running conversion with `--gitignore --force` twice does not duplicate entries.
- [ ] Nested `CLAUDE.md` produces a nested `AGENTS.md` ignore entry.
- [ ] `--dry-run --gitignore` leaves `.gitignore` unchanged and reports a planned entry.
- [ ] `--output <path> --gitignore` updates the output project's `.gitignore`.

