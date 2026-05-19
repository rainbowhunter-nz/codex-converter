from __future__ import annotations

from typing import Any

import yaml


def split_frontmatter(text: str) -> tuple[dict[str, Any], str, bool]:
    if not text.startswith("---\n"):
        return {}, text, False
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, False
    raw = text[4:end]
    body_start = end + len("\n---")
    if text[body_start : body_start + 1] == "\n":
        body_start += 1
    data = yaml.safe_load(raw) if raw.strip() else {}
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, text[body_start:], True


def build_frontmatter(data: dict[str, Any], body: str) -> str:
    rendered = yaml.safe_dump(data, sort_keys=False, allow_unicode=False).strip()
    return f"---\n{rendered}\n---\n{body.lstrip()}"

