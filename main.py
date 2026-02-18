import sys
import uuid
from pathlib import Path

# Додаємо шлях, щоб Python бачив усі папки
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

import config

from simulator import discovery
from simulator import impact_copy
from simulator import note
from simulator import restore
from simulator import logger

from defense import backup
from defense import detector
from defense import integrity


def show_help():
    print("""
Usage: python main.py [COMMAND]

Simulation commands:
  simulate  - Run ransomware attack simulation
  restore   - Remove .locked files and ransom note
  status    - Check current sandbox status

Defense commands:
  backup    - Create backup of sandbox files
  recover   - Restore files from backup
  detect    - Scan for suspicious .locked files
  baseline  - Create integrity snapshot
  check     - Compare current files with baseline
    """)


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    # 1. Перевірка безпеки
    if not discovery.ensure_sandbox_safe():
        print("❌ SAFETY ERROR: Sandbox folder or .SANDBOX_MARKER not found!")
        return

    if command == "simulate":
        targets = discovery.list_target_files()

        sandbox_path = (discovery.cwd.parent / config.SANDBOX_DIR).resolve()

        rel_targets = []
        for t in targets:
            try:
                rel_path = Path(t).relative_to(sandbox_path)
                rel_targets.append(str(rel_path))
            except ValueError:
                continue

        if not rel_targets:
            print(f"⚠️ No target files found in {sandbox_path}. Check your folders!")
            return

        session_id = str(uuid.uuid4())[:8]
        created = impact_copy.create_locked_placeholders(rel_targets, session_id)
        note.write_education_note(session_id, len(created))
        logger.log_event("simulate", {"sid": session_id, "impacted": len(created)})
        print(f"🔥 Attack Simulation Complete. {len(created)} placeholder files created.")

        if not rel_targets:
            print("No target files found to 'encrypt'.")
            return

        session_id = str(uuid.uuid4())[:8]
        created = impact_copy.create_locked_placeholders(rel_targets, session_id)
        note.write_education_note(session_id, len(created))

        logger.log_event("simulate", {"sid": session_id, "impacted": len(created)})
        print(f"🔥 Attack Simulation Complete. {len(created)} placeholder files created.")

        if not rel_targets:
            print("No target files found to 'encrypt'.")
            return

        session_id = str(uuid.uuid4())[:8]

        created = impact_copy.create_locked_placeholders(rel_targets, session_id)

        note.write_education_note(session_id, len(created))

        logger.log_event("simulate", {"sid": session_id, "impacted": len(created)})
        print(f"🔥 Attack Simulation Complete. {len(created)} placeholder files created.")

    elif command == "restore":
        result = restore.restore_system()
        logger.log_event("restore", result)
        print(f"🛠️ Cleanup complete. Removed {result['removed_count']} .locked files.")

    elif command == "status":
        detector.detect_ransomware()  # (Валентин)

    elif command == "backup":
        files = backup.backup_files()
        print(f"✅ Backup successful. {len(files)} files secured.")

    elif command == "recover":
        r, s = backup.restore_from_backup(overwrite=True)
        print(f"✅ Recovery complete. Restored: {r}, Skipped: {s}")

    elif command == "detect":
        detector.detect_ransomware()

    elif command == "baseline":
        integrity.create_baseline()

    elif command == "check":
        integrity.detect_changes()

    else:
        show_help()


if __name__ == "__main__":
    main()