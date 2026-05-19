# Codex Converter Proposal

## Goal

Build a Python CLI that converts project-scoped Claude Code workspace configuration into Codex CLI-compatible project configuration.

The converter must not read from or write to user-scoped Claude Code settings such as `~/.claude/settings.json`, `~/.claude/skills`, or `~/.claude/agents`.

## Research Summary

Codex and Claude Code both support project instructions, skills, subagents, and project configuration, but their file layouts differ.

### Codex CLI project files

Codex reads project instructions from `AGENTS.md`. It builds an instruction chain by starting at the project root and walking down to the current directory. In each directory, Codex checks `AGENTS.override.md`, then `AGENTS.md`, then configured fallback names. Files closer to the current directory appear later in the merged prompt and can override earlier guidance. Source: [OpenAI Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md).

Codex user config lives in `~/.codex/config.toml`, while project overrides live in `.codex/config.toml`. Project-scoped `.codex` layers only load after the project is trusted. Source: [OpenAI Codex config basics](https://developers.openai.com/codex/config-basic).

Codex skills are directories containing a required `SKILL.md` plus optional scripts, references, assets, and agent metadata. Repository skills live under `.agents/skills`, and Codex scans `.agents/skills` from the current working directory up to the repository root. Source: [OpenAI Codex skills](https://developers.openai.com/codex/skills).

Codex custom project agents are standalone TOML files under `.codex/agents/`. Each custom agent requires `name`, `description`, and `developer_instructions`. Source: [OpenAI Codex subagents](https://developers.openai.com/codex/subagents).

### Claude Code project files

Claude Code uses `CLAUDE.md` memory files for startup instructions and context. Settings JSON files configure permissions, environment variables, and tool behavior. Source: [Claude Code settings](https://code.claude.com/docs/en/settings).

Claude Code project subagents live in `.claude/agents/` and are Markdown files with YAML frontmatter. User subagents live under `~/.claude/agents/`, which is out of scope for this tool. Source: [Claude Code settings](https://code.claude.com/docs/en/settings#subagent-configuration).

Claude Code project skills live under `.claude/skills/<skill-name>/SKILL.md`. Each skill is a directory with `SKILL.md` as the entrypoint and optional supporting files. Existing `.claude/commands/` files still work like skills, but skills are recommended. Source: [Claude Code skills](https://code.claude.com/docs/en/skills).

## Proposed Conversion

The tool should convert only project-local files:

| Claude Code input | Codex output | Strategy |
| --- | --- | --- |
| `CLAUDE.md` | `AGENTS.md` | Copy content, adding a generated header that notes the source file. |
| Nested `CLAUDE.md` files | Nested `AGENTS.md` files | Preserve relative directory structure. |
| `.claude/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` | Copy skill directories. Ensure Codex-required `name` and `description` exist in frontmatter. |
| `.claude/commands/<name>.md` | `.agents/skills/<name>/SKILL.md` | Convert command markdown into a skill directory. |
| `.claude/agents/<name>.md` | `.codex/agents/<name>.toml` | Parse YAML frontmatter and body. Map body to `developer_instructions`. |
| `.claude/settings.json` | `.codex/config.toml` | Convert supported project-safe settings only. Preserve unsupported settings in a conversion report. |
| `.claude/settings.local.json` | No default output | Skip by default because it is machine-local. Optionally report that it was skipped. |

The first version should avoid trying to convert plugins, hooks, MCP servers, or marketplace configuration unless the mapping is direct and verified. These areas have higher security and trust implications, so the converter should report them as unsupported rather than guessing.

## CLI Shape

Use `typer` for commands and `rich` for console output.

Proposed commands:

```text
codex-converter inspect [SOURCE]
codex-converter convert [SOURCE] [--output PATH] [--dry-run] [--force]
```

`inspect` should print a table of discovered Claude Code project assets and explain whether each asset is convertible, skipped, or unsupported.

`convert` should write Codex files into the target project. By default, `SOURCE` is the current directory and `--output` is the same directory. `--dry-run` should show planned writes without modifying files. `--force` should allow overwriting generated Codex files; without it, existing Codex files should be left untouched and reported as conflicts.

## Safety Rules

1. Never read or write `~/.claude`.
2. Never write outside the selected output directory.
3. Treat existing Codex files as user-owned unless `--force` is set.
4. Emit a conversion report for skipped and unsupported files.
5. Prefer deterministic file transforms over model-generated rewrites.

## Implementation Plan

1. Add dependencies with `uv`: `typer`, `rich`, `tomli-w`, and `pyyaml`.
2. Replace the placeholder `main.py` with a Typer app, or create a package module if the project is expanded beyond one file.
3. Implement discovery:
   - find `CLAUDE.md` files under the source tree;
   - find `.claude/skills`;
   - find `.claude/commands`;
   - find `.claude/agents`;
   - find `.claude/settings.json` and `.claude/settings.local.json`.
4. Implement converters one asset type at a time.
5. Add tests around path safety, dry-run behavior, frontmatter parsing, agent TOML output, and overwrite protection.
6. Add README usage examples after the CLI behavior is stable.

## Open Questions

1. Should the converter create `.codex/config.toml` by default, or only when supported Claude settings are found? Create by default.
2. Should `.claude/settings.local.json` always be skipped, or should there be an explicit opt-in to convert local settings into `.codex/config.toml`? skip with explicit opt-in.
3. Should existing `AGENTS.md` files be merged with `CLAUDE.md`, or should conversion stop and report a conflict? Treat the CLAUDE.md as the truth.

## Recommended First Version

Implement a conservative first version:

- Convert `CLAUDE.md` to `AGENTS.md`.
- Copy `.claude/skills` to `.agents/skills` with frontmatter normalization.
- Convert `.claude/commands` to Codex skills.
- Convert `.claude/agents` to `.codex/agents/*.toml`.
- Detect settings, hooks, plugins, and MCP configuration, but report them as skipped unless a safe direct mapping is implemented.

This gives useful migration coverage while keeping the tool understandable and avoiding silent security-sensitive behavior changes.
