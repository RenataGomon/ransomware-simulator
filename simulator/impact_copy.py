from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
import time

import config


class SandboxSafetyError(RuntimeError):
    pass


def _sandbox_path() -> Path:
    project_root = Path(__file__).resolve().parent.parent
    return project_root / config.SANDBOX_DIR



def _ensure_sandbox_safe() -> Path:
    sandbox = _sandbox_path()
    marker = sandbox / config.MARKER_NAME

    if not sandbox.exists() or not sandbox.is_dir():
        raise SandboxSafetyError(f"Sandbox directory not found: {sandbox}")

    if not marker.exists():
        raise SandboxSafetyError(
            f"Safety marker '{config.MARKER_NAME}' not found in sandbox: {sandbox}\n"
            f"Create an empty file: {sandbox / config.MARKER_NAME}"
        )

    if sandbox == Path("/"):
        raise SandboxSafetyError("Refusing to operate on filesystem root '/'.")

    return sandbox


def create_locked_placeholders(
    targets: Iterable[str],
    session_id: str,
) -> List[str]:
    """
    Safe educational 'impact' simulation.

    Creates small placeholder files with suffix LOCKED_SUFFIX next to each target.
    Original files are NOT modified and NOT copied.

    Input: targets = relative paths inside sandbox (e.g., 'docs/a.txt')
    Output: list of created placeholder paths relative to sandbox
    """
    sandbox = _ensure_sandbox_safe()
    created: List[str] = []

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    header = (
        "=== EDUCATIONAL RANSOMWARE SIMULATION ===\n"
        "Harmless placeholder file created for coursework demo.\n"
        "No original data was encrypted or modified.\n"
        f"Session: {session_id}\n"
        f"Time: {timestamp}\n"
        "========================================\n\n"
    )

    for rel in targets:
        rel_path = Path(rel)

        if rel_path.is_absolute() or ".." in rel_path.parts:
            continue

        src = (sandbox / rel_path).resolve()

        try:
            src.relative_to(sandbox)
        except ValueError:
            continue

        if not src.exists() or not src.is_file():
            continue

        if src.name.endswith(config.LOCKED_SUFFIX):
            continue
        if src.name in {config.NOTE_NAME, config.LOG_NAME, config.MARKER_NAME}:
            continue

        locked_path = Path(str(src) + config.LOCKED_SUFFIX)

        if locked_path.exists():
            continue

        body = (
            header
            + f"Original (relative): {rel_path.as_posix()}\n"
            + "This is a simulation placeholder.\n"
            + f"To restore: run `python main.py restore`.\n"
        )

        locked_path.write_text(body[:2000], encoding="utf-8")
        created.append(str(locked_path.relative_to(sandbox)))

    return created


# if __name__ == "__main__":
#     created = create_locked_placeholders(["docs/a.txt",
#                                           "images/keyboard_test.png"],
#                                          session_id="TEST")
#     print("Created:", created)
