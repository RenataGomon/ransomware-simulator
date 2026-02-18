from __future__ import annotations

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from pathlib import Path
from typing import List, Tuple
import shutil
import config


class BackupError(RuntimeError):
    pass


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _sandbox_dir() -> Path:
    return _project_root() / config.SANDBOX_DIR


def _backup_dir() -> Path:
    return _project_root() / "sandbox_backup"


def _ensure_safe_sandbox() -> Path:
    sandbox = _sandbox_dir()
    marker = sandbox / config.MARKER_NAME

    if not sandbox.exists() or not sandbox.is_dir():
        raise BackupError(f"Sandbox directory not found: {sandbox}")

    if not marker.exists():
        raise BackupError(
            f"Safety marker '{config.MARKER_NAME}' not found in sandbox: {sandbox}"
        )

    if sandbox == Path("/"):
        raise BackupError("Refusing to operate on filesystem root '/'.")

    return sandbox


def _should_backup(path: Path) -> bool:

    name = path.name

    if name == config.MARKER_NAME:
        return False
    if name == config.NOTE_NAME:
        return False
    if name == config.LOG_NAME:
        return False
    if name.endswith(config.LOCKED_SUFFIX):
        return False

    return path.suffix.lower() in {ext.lower() for ext in config.ALLOWED_EXT}


def backup_files() -> List[str]:

    sandbox = _ensure_safe_sandbox()
    backup_root = _backup_dir()
    backup_root.mkdir(parents=True, exist_ok=True)

    backed_up: List[str] = []

    max_bytes = int(config.MAX_FILE_MB * 1024 * 1024)

    for src in sandbox.rglob("*"):
        if not src.is_file():
            continue

        try:
            rel = src.relative_to(sandbox)
        except ValueError:
            continue

        if not _should_backup(src):
            continue

        try:
            if src.stat().st_size > max_bytes:
                continue
        except OSError:
            continue

        dst = backup_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src, dst)
        backed_up.append(rel.as_posix())

    return backed_up


def restore_from_backup(overwrite: bool = True) -> Tuple[int, int]:

    sandbox = _ensure_safe_sandbox()
    backup_root = _backup_dir()

    if not backup_root.exists() or not backup_root.is_dir():
        raise BackupError(f"Backup directory not found: {backup_root}")

    restored = 0
    skipped = 0

    for src in backup_root.rglob("*"):
        if not src.is_file():
            continue

        rel = src.relative_to(backup_root)
        dst = sandbox / rel

        if dst.name == config.MARKER_NAME:
            skipped += 1
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)

        if dst.exists() and not overwrite:
            skipped += 1
            continue

        shutil.copy2(src, dst)
        restored += 1

    return restored, skipped


if __name__ == "__main__":
    files = backup_files()
    print(f"Backed up {len(files)} files.")
    # Example restore:
    # r, s = restore_from_backup(overwrite=True)
    # print("Restored:", r, "Skipped:", s)
