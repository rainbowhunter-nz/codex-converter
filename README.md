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

## Converted Files

| Claude Code input | Codex output |
| --- | --- |
| `CLAUDE.md` | `AGENTS.md` |
| nested `CLAUDE.md` files | nested `AGENTS.md` files |
| `.claude/skills/<name>/` | `.agents/skills/<name>/` |
| `.claude/commands/<name>.md` | `.agents/skills/<name>/SKILL.md` |
| `.claude/agents/<name>.md` | `.codex/agents/<name>.toml` |
| `.claude/settings.json` | `.codex/config.toml` default file |

Existing targets are reported as conflicts and left untouched unless `--force` is used. `--dry-run` reports planned writes without creating files.

## Unsupported or Skipped

The V1 converter reports but does not convert:

- `.claude/settings.local.json`
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
