from __future__ import annotations

from pathlib import Path


def resolved(path: Path) -> Path:
    return path.expanduser().resolve()


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def claude_user_dir() -> Path:
    return resolved(Path.home() / ".claude")


def reject_user_claude_path(path: Path, label: str) -> Path:
    candidate = resolved(path)
    user_dir = claude_user_dir()
    if candidate == user_dir or is_relative_to(candidate, user_dir):
        raise ValueError(f"{label} must not be under user-scoped Claude path {user_dir}")
    return candidate


def contained_path(root: Path, target: Path) -> Path:
    root = resolved(root)
    candidate = resolved(target)
    if not is_relative_to(candidate, root):
        raise ValueError(f"planned output escapes output directory: {candidate}")
    reject_user_claude_path(candidate, "output path")
    return candidate

