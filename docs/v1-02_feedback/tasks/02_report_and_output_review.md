# Task 02: Report Styling and Output Review

## Goal

Make generated output easier to review without changing unsupported conversion behavior.

## Scope

- Add status-specific Rich styles to the conversion report table.
- Keep report text readable when ANSI color is disabled or captured in logs.
- Make generated headers consistent and concise.
- Improve report detail text for default config creation versus settings-based config conversion.
- Review generated config, agent, command, skill, and instruction output for small clarity improvements.
- Do not add new conversion mappings for unsupported Claude settings.

## Suggested Files

- `codex_converter/cli.py`
- `codex_converter/converter.py`
- `tests/test_cli.py`

## Status Styles

| Status | Style |
| --- | --- |
| `written` | `green` |
| `planned` | `cyan` |
| `convertible` | `cyan` |
| `skipped` | `yellow` |
| `unsupported` | `magenta` |
| `conflict` | `red` |
| `error` | `bold red` |

## Assumptions

- Styling should be applied through Rich table cell style support rather than embedding status text decorations.
- Generated markers should continue to include `codex-converter` so future cleanup can verify generated files.

## Success Criteria

- [ ] Each known status uses the requested Rich style.
- [ ] Plain-text report output still includes the same status values.
- [ ] Generated headers are concise, consistent, and still identify `codex-converter`.
- [ ] Report details distinguish default config creation from settings-derived config conversion.
- [ ] Unsupported settings remain unsupported unless a safe direct Codex mapping is verified.
- [ ] Existing tests continue to pass.

## Expected Unit Tests

- [ ] Report rendering still includes unstyled status text after `click.unstyle`.
- [ ] A direct `_print_report` or CLI rendering test verifies status styles are attached to status cells.
- [ ] Generated instruction headers still include the source path and `codex-converter`.
- [ ] Config conversion detail differs for default config creation and settings conversion.

