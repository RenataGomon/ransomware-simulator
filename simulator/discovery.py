from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

cwd = Path(__file__)

def ensure_sandbox_safe():
    if not Path.exists(cwd.parent.parent / config.SANDBOX_DIR) or not Path.exists(cwd.parent.parent / config.SANDBOX_DIR / config.MARKER_NAME):
        return False
    else:
        return True

def list_target_files():
    target_files = []
    for i in config.ALLOWED_EXT:
        for j in (cwd.parent.parent / config.SANDBOX_DIR).glob(f"*{i}"):
            target_files.append(str(Path(j)))
    return target_files

if __name__ == "__main__":
    print(f"ensure_sandbox_safe: {ensure_sandbox_safe()}")
    print(f"list_target_files: {list_target_files()}")
