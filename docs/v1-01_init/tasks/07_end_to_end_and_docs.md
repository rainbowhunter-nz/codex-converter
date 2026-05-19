# Task 07: End-to-End Tests and User Documentation

## Goal

Validate the full converter workflow and document basic usage.

## Scope

- Add end-to-end tests with a realistic temporary Claude Code project.
- Verify `inspect`, `convert --dry-run`, and `convert` behavior.
- Update `README.md` with installation and usage examples.
- Document known unsupported conversions.
- Ensure all tests run through `uv`.

## Out of Scope

- New converter features.
- Broad refactors.
- Publishing automation.

## Checklist

- [x] End-to-end fixture covers instructions, skills, commands, agents, and settings.
- [x] Dry-run output is verified.
- [x] Real conversion output is verified.
- [x] README includes basic usage.
- [x] README lists unsupported areas.
- [x] Full test suite passes with `uv`.

## Success Criteria

- A user can understand and run the converter from the README.
- The test suite covers the main conversion path.
- Unsupported behavior is documented rather than hidden.

## Expected Unit Tests

- Test `inspect` on a realistic fixture.
- Test `convert --dry-run` writes no files.
- Test `convert` creates the expected Codex file tree.
- Test rerunning without `--force` reports conflicts.
- Test rerunning with `--force` updates generated outputs.
