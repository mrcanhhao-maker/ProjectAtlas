import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "VisionRow"
BACKUP_DIR = ROOT / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")

VERSION = "VisionRow Alpha 5.1 - Updater v1"

REQUIRED = [
    "cv2",
    "mediapipe",
    "numpy",
]

def log(msg):
    print(msg)

def check_python():
    log("🔍 Kiểm tra Python...")
    log(f"Python: {sys.version.split()[0]}")

def check_packages():
    log("🔍 Kiểm tra thư viện...")
    missing = []
    for pkg in REQUIRED:
        try:
            __import__(pkg)
            log(f"✅ {pkg}")
        except ImportError:
            missing.append(pkg)

    if missing:
        log("⚠️ Thiếu thư viện, đang cài...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "opencv-python", "mediapipe", "numpy"
        ])

def backup_project():
    log("💾 Backup phiên bản cũ...")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for name in ["app.py", "engine"]:
        src = ROOT / name
        if src.exists():
            dst = BACKUP_DIR / name
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

    log(f"✅ Backup xong: {BACKUP_DIR}")

def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)

def install_alpha_51():
    log("🚀 Cài VisionRow Alpha 5.1...")

    write_file(ROOT / "VERSION.txt", VERSION)

    write_file(ROOT / "run.sh", """#!/bin/bash
cd ~/VisionRow
source venv/bin/activate
python3 app.py
""")

    os.chmod(ROOT / "run.sh", 0o755)

    write_file(ROOT / "README.txt", """
VisionRow Alpha 5.1

Cách chạy:
cd ~/VisionRow
source venv/bin/activate
python3 app.py

Hoặc:
./run.sh

Phím điều khiển:
Q = thoát
R = reset
C = calibration
""")

    log("✅ Alpha 5.1 đã sẵn sàng.")

def run_app():
    log("▶️ Mở VisionRow...")
    subprocess.call([sys.executable, str(ROOT / "app.py")])

def main():
    print("=" * 50)
    print(VERSION)
    print("=" * 50)

    check_python()
    check_packages()
    backup_project()
    install_alpha_51()

    print("")
    print("✅ Update hoàn tất.")
    print("👉 Từ lần sau chỉ cần chạy:")
    print("cd ~/VisionRow && source venv/bin/activate && python3 update.py")
    print("")

    run_app()

if __name__ == "__main__":
    main()
