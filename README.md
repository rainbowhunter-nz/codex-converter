# codex-converter

Convert project-scoped Claude Code workspace files into Codex CLI-compatible project files.

`codex-converter` is intentionally conservative. It reads only project-local Claude assets and rejects user-scoped Claude paths such as `~/.claude`.

## Install

Install with `uv`.

```sh
uv tool install codex-converter
```

You can also run it without a persistent install:

```sh
uvx codex-converter --help
```

## Usage

Inspect a project without writing files:

```sh
codex-converter inspect /path/to/project
```

Preview a conversion:

```sh
codex-converter convert /path/to/project --dry-run
```

Convert in place:

```sh
codex-converter convert /path/to/project
```

Write converted files to a separate directory:

```sh
codex-converter convert /path/to/project --output /path/to/output
```

Overwrite previously generated targets:

```sh
codex-converter convert /path/to/project --force
```

Add generated Codex output paths to the output project's `.gitignore`:

```sh
codex-converter convert /path/to/project --gitignore
```

Remove generated converter output:

```sh
codex-converter clean /path/to/project
```

Preview cleanup first:

```sh
codex-converter clean /path/to/project --dry-run
```

Show the installed version:

```sh
codex-converter --version
```

## What Gets Converted

| Claude Code input | Codex output |
| --- | --- |
| `CLAUDE.md` | `AGENTS.md` |
| nested `CLAUDE.md` files | nested `AGENTS.md` files |
| `.claude/skills/<name>/` | `.agents/skills/<name>/` |
| `.claude/commands/<name>.md` | `.agents/skills/<name>/SKILL.md` |
| `.claude/agents/<name>.md` | `.codex/agents/<name>.toml` |
| `.claude/settings.json` | `.codex/config.toml` |
| `.claude/settings.local.json` | merged into `.codex/config.toml` only with `--include-local-settings` |

Existing targets are reported as conflicts and left untouched unless `--force` is used. `--dry-run` reports planned writes without creating files.

`clean` removes only files or directories that contain, or can be verified from, a `codex-converter` generated marker. `clean --force` removes known generated target paths even when a marker is missing.

## Unsupported

The converter reports but does not convert:

- Claude hooks
- MCP server configuration
- plugins and marketplace configuration
- auth and trust configuration
- unsupported Claude settings
- user-scoped Claude assets under `~/.claude`
