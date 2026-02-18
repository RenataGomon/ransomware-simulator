import json
from pathlib import Path
import config


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def create_baseline():
    root = _get_project_root()
    sandbox = root / config.SANDBOX_DIR
    baseline_path = root / config.BASELINE_FILE

    files = []
    for f in sandbox.rglob("*"):
        if f.is_file() and not f.name.endswith(config.LOCKED_SUFFIX) and f.name != config.LOG_NAME:
            files.append(str(f.relative_to(sandbox)))

    baseline_path.write_text(json.dumps(files, indent=4), encoding="utf-8")
    print(f"Baseline created with {len(files)} files.")


def detect_changes():
    root = _get_project_root()
    sandbox = root / config.SANDBOX_DIR
    baseline_path = root / config.BASELINE_FILE

    if not baseline_path.exists():
        print("Baseline not found. Run 'baseline' command first.")
        return

    baseline = set(json.loads(baseline_path.read_text(encoding="utf-8")))

    current = []
    for f in sandbox.rglob("*"):
        if f.is_file() and not f.name.endswith(config.LOCKED_SUFFIX) and f.name != config.LOG_NAME:
            current.append(str(f.relative_to(sandbox)))
    current = set(current)

    new_files = current - baseline
    missing_files = baseline - current

    if not new_files and not missing_files:
        print("Integrity Check: OK. No changes detected.")
    else:
        print("INTEGRITY ALERT!")
        if new_files: print(f"  [+] New/Unknown files: {list(new_files)}")
        if missing_files: print(f"  [-] Missing files: {list(missing_files)}")