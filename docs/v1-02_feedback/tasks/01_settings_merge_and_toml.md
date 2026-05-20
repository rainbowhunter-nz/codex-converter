# Task 01: Settings Merge and Readable TOML

## Goal

Implement opt-in `.claude/settings.local.json` conversion and replace placeholder `.codex/config.toml` generation with readable, parseable TOML for supported settings.

## Scope

- Add `--include-local-settings` to `codex-converter convert`.
- Keep `.claude/settings.local.json` skipped by default.
- Load `.claude/settings.json` as the base settings object when present.
- When the flag is set and `.claude/settings.local.json` exists, recursively merge local settings over base settings.
- For matching object values, merge recursively.
- For arrays, strings, booleans, numbers, and nulls, replace base values with local values.
- Report invalid JSON for either settings file without crashing the whole conversion.
- Generate `.codex/config.toml` from the merged settings data instead of only writing the placeholder header.
- Format generated TOML for reviewability, targeting a 120 character maximum line length.
- Keep unsupported hooks, MCP servers, plugins, auth, trust, marketplace, and unknown settings reported as unsupported.

## Suggested Files

- `codex_converter/cli.py`
- `codex_converter/converter.py`
- `codex_converter/discovery.py`
- `codex_converter/models.py`
- `tests/test_cli.py`

## Assumptions

- There are currently no verified safe direct mappings for Claude settings, so unsupported setting reporting should remain conservative.
- A small helper scoped to the generated settings/config data is preferred over a general TOML pretty-printer.
- Generated TOML must remain valid according to Python `tomllib`.

## Success Criteria

- [ ] `convert` help shows `--include-local-settings`.
- [ ] `.claude/settings.local.json` is discovered but skipped unless the flag is passed.
- [ ] With `--include-local-settings`, local settings override base settings in the generated config data.
- [ ] Nested object settings are recursively merged.
- [ ] Non-object values from local settings replace base values.
- [ ] Unsupported merged settings are reported the same way unsupported base settings are reported.
- [ ] Generated `.codex/config.toml` parses with `tomllib`.
- [ ] Generated TOML avoids long unreadable single-line structures and targets lines of 120 characters or less.
- [ ] Existing conversion behavior still passes.

## Expected Unit Tests

- [ ] Default conversion reports `settings.local` as skipped and does not merge local settings.
- [ ] `--include-local-settings` merges local values over base values.
- [ ] Recursive object merge preserves unrelated base keys.
- [ ] Local arrays/scalars replace base arrays/scalars.
- [ ] Invalid base settings JSON reports an error and does not write an invalid config.
- [ ] Invalid local settings JSON reports an error when `--include-local-settings` is used.
- [ ] Generated config parses with `tomllib`.
- [ ] A fixture with long arrays or nested values has no generated TOML line over 120 characters.

