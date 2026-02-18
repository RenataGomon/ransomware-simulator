from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

cwd = Path(__file__).parent

def detect_ransomware():
    i = 0
    for j in (cwd.parent / config.SANDBOX_DIR).glob(f"*{config.LOCKED_SUFFIX}"):
        i += 1
    if i > 0:
        print("Warning: Possible ransomware activity detected")
        print(f"{i} suspicious files found")
    else:
        print("Your PC is safe")

if __name__ == "__main__":
    print("detect_ransomware(): ")
    detect_ransomware()
