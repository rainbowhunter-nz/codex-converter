# Task 06: Settings and Safety

## Goal

Create `.codex/config.toml` safely and enforce the converter's filesystem safety rules.

## Scope

- Create `.codex/config.toml` by default.
- Convert only verified project-safe `.claude/settings.json` values.
- Skip `.claude/settings.local.json` unless an explicit future opt-in is added.
- Report unsupported settings, hooks, plugins, and MCP configuration.
- Enforce output path containment.
- Enforce no reads or writes under `~/.claude`.

## Out of Scope

- Full Claude settings parity.
- Hook conversion.
- MCP server conversion.
- Plugin conversion.
- Automatic trust or auth configuration.

## Checklist

- [x] `.codex/config.toml` is created by default.
- [x] Unsupported Claude settings are reported.
- [x] `.claude/settings.local.json` is skipped by default.
- [x] Output path containment is enforced.
- [x] User-scoped Claude paths are rejected.
- [x] Conversion report includes skipped safety-sensitive assets.

## Success Criteria

- The converter never mutates user-scoped Claude state.
- Unsafe or unsupported settings are visible in the report.
- `.codex/config.toml` is valid TOML.

## Expected Unit Tests

- Test `.codex/config.toml` is created by default.
- Test unsupported settings appear in the report.
- Test `.claude/settings.local.json` is skipped.
- Test output paths outside the output root are rejected.
- Test `~/.claude` source paths are rejected.
- Test generated TOML can be parsed.
