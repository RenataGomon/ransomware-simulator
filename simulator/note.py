from __future__ import annotations

from pathlib import Path
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
            f"Safety marker '{config.MARKER_NAME}' not found in sandbox: {sandbox}"
        )

    if sandbox == Path("/"):
        raise SandboxSafetyError("Refusing to operate on filesystem root '/'.")

    return sandbox


def write_education_note(session_id: str, impacted_count: int) -> str:
    sandbox = _ensure_sandbox_safe()
    note_path = sandbox / config.NOTE_NAME

    now = time.strftime("%Y-%m-%d %H:%M:%S")
    text = f"""\
EDUCATIONAL RANSOMWARE SIMULATION (SAFE)

Session: {session_id}
Time:    {now}

What happened?
- The simulator created harmless '{config.LOCKED_SUFFIX}' placeholder files in '{config.SANDBOX_DIR}/'.
- No original files were encrypted or modified.
- This is a coursework demo to study ransomware workflow + defenses.

Placeholders created: {impacted_count}

How to restore (demo):
- Run: python main.py restore

Defense ideas for the report:
- Regular offline backups + restore practice
- Least privilege (limit write access to important folders)
- Monitoring for suspicious new extensions (like '{config.LOCKED_SUFFIX}')
- File inventory / integrity monitoring (baseline)
- Patching + phishing awareness
"""
    note_path.write_text(text, encoding="utf-8")
    return str(note_path.relative_to(sandbox))


# if __name__ == "__main__":
#     print(write_education_note("TEST", 2))