# codex-converter

`codex-converter` converts project-scoped Claude Code workspace files into Codex CLI-compatible project files.

The converter only reads project-local Claude assets. It rejects user-scoped Claude paths such as `~/.claude`.

## Usage

Inspect a project:

```sh
uv run codex-converter inspect /path/to/project
```

Convert a project in place:

```sh
uv run codex-converter convert /path/to/project
```

Preview planned writes without modifying files:

```sh
uv run codex-converter convert /path/to/project --dry-run
```

Write converted files to a separate output directory:

```sh
uv run codex-converter convert /path/to/project --output /path/to/output
```

Overwrite existing generated targets:

```sh
uv run codex-converter convert /path/to/project --force
```

Include machine-local Claude settings when generating the reviewable Codex config:

```sh
uv run codex-converter convert /path/to/project --include-local-settings
```

Add generated Codex outputs to the output project's `.gitignore`:

```sh
uv run codex-converter convert /path/to/project --gitignore
```

Preview cleanup of generated converter output:

```sh
uv run codex-converter clean /path/to/project --dry-run
```

Remove generated converter output with `codex-converter` markers:

```sh
uv run codex-converter clean /path/to/project
```

Remove known generated target paths even when a marker is missing:

```sh
uv run codex-converter clean /path/to/project --force
```

## Converted Files

| Claude Code input | Codex output |
| --- | --- |
| `CLAUDE.md` | `AGENTS.md` |
| nested `CLAUDE.md` files | nested `AGENTS.md` files |
| `.claude/skills/<name>/` | `.agents/skills/<name>/` |
| `.claude/commands/<name>.md` | `.agents/skills/<name>/SKILL.md` |
| `.claude/agents/<name>.md` | `.codex/agents/<name>.toml` |
| `.claude/settings.json` | `.codex/config.toml` reviewable settings-derived file |
| `.claude/settings.local.json` | merged into `.codex/config.toml` only with `--include-local-settings` |

Existing targets are reported as conflicts and left untouched unless `--force` is used. `--dry-run` reports planned writes without creating files.

`--gitignore` appends generated output paths such as `AGENTS.md`, `.agents/`, `.codex/`, and nested `AGENTS.md` files to the output project's `.gitignore` without duplicating existing entries.

`clean` is conservative by default: it removes only files or directories that contain, or can be verified from, a `codex-converter` generated marker. It also removes generated `.gitignore` entries while preserving unrelated lines. `clean --force` removes known generated target paths inside the target project even when a marker is missing.

## Unsupported or Skipped

The V1 converter reports but does not convert:

- `.claude/settings.local.json`, unless `--include-local-settings` is used
- Claude hooks
- MCP server configuration
- plugins and marketplace configuration
- auth and trust configuration
- unsupported Claude settings
- user-scoped Claude assets under `~/.claude`

## Development

Run the verification suite:

```sh
uv run pytest
uv run ruff check .
uv run mypy .
```

## Releases

CI runs on every push and pull request.

Publishing runs when a tag matching `v*.*.*` is pushed. The tag version must match the package version in `pyproject.toml`; for example, package version `0.1.0` must be released with tag `v0.1.0`.

The release workflow uses PyPI Trusted Publishing through GitHub Actions. Configure the PyPI project with:

- repository: this GitHub repository
- workflow: `release.yml`
- environment: `pypi`

Then publish a release with:

```sh
git tag v0.1.0
git push origin v0.1.0
```
