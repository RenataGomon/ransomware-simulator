import json
import datetime
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import config


def log_event(event_name: str, payload: dict):
    project_root = Path(__file__).resolve().parent.parent
    log_path = project_root / config.SANDBOX_DIR / config.LOG_NAME

    entry = {
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_name,
        "payload": payload
    }

    logs = []
    if log_path.exists():
        try:
            logs = json.loads(log_path.read_text(encoding="utf-8"))
        except:
            logs = []

    logs.append(entry)
    log_path.write_text(json.dumps(logs, indent=4), encoding="utf-8")