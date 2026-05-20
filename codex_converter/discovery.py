from __future__ import annotations

import json
from pathlib import Path

from .models import ReportEntry, Status
from .safety import reject_user_claude_path


UNSUPPORTED_SETTINGS = {
    "hooks": "Claude hooks are safety-sensitive and are not converted.",
    "mcpServers": "MCP server configuration is not converted.",
    "plugins": "Claude plugins are not converted.",
    "auth": "Auth configuration is not converted.",
    "trust": "Trust configuration is not converted.",
    "marketplace": "Marketplace configuration is not converted.",
}


def discover(source: Path, *, include_local_settings: bool = False) -> list[ReportEntry]:
    source = reject_user_claude_path(source, "source")
    entries: list[ReportEntry] = []

    for path in sorted(source.rglob("CLAUDE.md")):
        if ".claude" in path.relative_to(source).parts:
            continue
        entries.append(ReportEntry("instructions", path, Status.CONVERTIBLE, "convert to AGENTS.md"))

    claude_dir = source / ".claude"
    skills_dir = claude_dir / "skills"
    if skills_dir.is_dir():
        for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
            entries.append(ReportEntry("skill", skill_md, Status.CONVERTIBLE, "copy to .agents/skills"))

    commands_dir = claude_dir / "commands"
    if commands_dir.is_dir():
        for command in sorted(commands_dir.glob("*.md")):
            entries.append(ReportEntry("command", command, Status.CONVERTIBLE, "convert to Codex skill"))

    agents_dir = claude_dir / "agents"
    if agents_dir.is_dir():
        for agent in sorted(agents_dir.glob("*.md")):
            entries.append(ReportEntry("agent", agent, Status.CONVERTIBLE, "convert to Codex agent TOML"))

    settings = claude_dir / "settings.json"
    if settings.exists():
        entries.append(ReportEntry("settings", settings, Status.CONVERTIBLE, "create safe .codex/config.toml"))
        if include_local_settings and local_settings_exists(claude_dir):
            entries.extend(_unsupported_merged_settings_entries(settings, claude_dir / "settings.local.json"))
        else:
            entries.extend(_unsupported_settings_entries(settings))

    local_settings = claude_dir / "settings.local.json"
    if local_settings.exists():
        if include_local_settings:
            entries.append(
                ReportEntry("settings.local", local_settings, Status.CONVERTIBLE, "merge over base settings")
            )
            if not settings.exists():
                entries.extend(_unsupported_settings_entries(local_settings, kind_prefix="settings.local"))
        else:
            entries.append(
                ReportEntry("settings.local", local_settings, Status.SKIPPED, "machine-local settings are skipped")
            )

    return entries


def local_settings_exists(claude_dir: Path) -> bool:
    return (claude_dir / "settings.local.json").exists()


def _unsupported_settings_entries(settings: Path, *, kind_prefix: str = "settings") -> list[ReportEntry]:
    try:
        data = json.loads(settings.read_text())
    except json.JSONDecodeError as exc:
        return [ReportEntry(kind_prefix, settings, Status.ERROR, f"invalid JSON: {exc.msg}")]
    if not isinstance(data, dict):
        return [ReportEntry(kind_prefix, settings, Status.ERROR, "settings file must contain a JSON object")]
    return _unsupported_settings_entries_for_data(data, settings, kind_prefix=kind_prefix)


def _unsupported_merged_settings_entries(base: Path, local: Path) -> list[ReportEntry]:
    try:
        base_data = json.loads(base.read_text())
    except json.JSONDecodeError as exc:
        return [ReportEntry("settings", base, Status.ERROR, f"invalid JSON: {exc.msg}")]
    if not isinstance(base_data, dict):
        return [ReportEntry("settings", base, Status.ERROR, "settings file must contain a JSON object")]
    try:
        local_data = json.loads(local.read_text())
    except json.JSONDecodeError as exc:
        return [ReportEntry("settings.local", local, Status.ERROR, f"invalid JSON: {exc.msg}")]
    if not isinstance(local_data, dict):
        return [ReportEntry("settings.local", local, Status.ERROR, "settings file must contain a JSON object")]
    return _unsupported_settings_entries_for_data(_merge_settings(base_data, local_data), base, kind_prefix="settings")


def _unsupported_settings_entries_for_data(
    data: dict[str, object], settings: Path, *, kind_prefix: str
) -> list[ReportEntry]:
    entries: list[ReportEntry] = []
    for key in sorted(data):
        detail = UNSUPPORTED_SETTINGS.get(key)
        if detail is not None:
            entries.append(ReportEntry(f"{kind_prefix}.{key}", settings, Status.UNSUPPORTED, detail))
        elif key not in SUPPORTED_SETTINGS:
            entries.append(ReportEntry(f"{kind_prefix}.{key}", settings, Status.UNSUPPORTED, "unsupported Claude setting"))
    return entries


SUPPORTED_SETTINGS: set[str] = set()


def _merge_settings(base: dict[str, object], local: dict[str, object]) -> dict[str, object]:
    merged = dict(base)
    for key, local_value in local.items():
        base_value = merged.get(key)
        if isinstance(base_value, dict) and isinstance(local_value, dict):
            merged[key] = _merge_settings(base_value, local_value)
        else:
            merged[key] = local_value
    return merged
