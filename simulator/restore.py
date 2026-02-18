from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import config


def restore_system() -> dict:
    project_root = Path(__file__).resolve().parent.parent
    sandbox = project_root / config.SANDBOX_DIR

    removed_locked = 0
    if sandbox.exists():
        for file in sandbox.rglob(f"*{config.LOCKED_SUFFIX}"):
            file.unlink()
            removed_locked += 1

        note_path = sandbox / config.NOTE_NAME
        if note_path.exists():
            note_path.unlink()

    return {"removed_count": removed_locked, "note_deleted": True}