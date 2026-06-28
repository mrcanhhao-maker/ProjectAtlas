#!/usr/bin/env python3
from __future__ import annotations

import importlib
import json
import py_compile
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


REQUIRED_FILES = [
    "engine/__init__.py",
    "engine/pose_engine.py",
    "engine/stroke_v3.py",
    "engine/quality_engine.py",
    "engine/motion_metrics.py",
    "engine/stroke_validator.py",
    "engine/stroke_history.py",
    "engine/virtual_rower.py",
    "engine/session_recorder.py",
    "plugins/visionrow/alpha10/app_alpha10.py",
    "plugins/visionrow/alpha12/app_alpha12.py",
    "scripts/stage1_healthcheck.py",
    "tests/test_virtual_rower_engine.py",
    "docs/STAGE1_LOCK.md",
    "docs/STAGE1_COMPLETE.md",
]


REQUIRED_MODULES = [
    "engine.pose_engine",
    "engine.stroke_v3",
    "engine.quality_engine",
    "engine.motion_metrics",
    "engine.stroke_validator",
    "engine.stroke_history",
    "engine.virtual_rower",
    "engine.session_recorder",
]


def fail(message: str) -> None:
    print(json.dumps({"stage": "stage2", "version": "Alpha12.3", "status": "FAIL", "error": message}, ensure_ascii=False, indent=2))
    sys.exit(1)


def run_command(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode != 0:
        fail(
            "Command failed: "
            + " ".join(command)
            + "\nSTDOUT:\n"
            + completed.stdout
            + "\nSTDERR:\n"
            + completed.stderr
        )


def public_symbols(module) -> list[str]:
    return sorted(name for name in dir(module) if not name.startswith("_"))


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail(f"Missing required files: {missing}")

    for path in REQUIRED_FILES:
        if path.endswith(".py"):
            py_compile.compile(str(ROOT / path), doraise=True)

    imported = {}
    for module_name in REQUIRED_MODULES:
        module = importlib.import_module(module_name)
        symbols = public_symbols(module)
        if not symbols:
            fail(f"Module has no public production symbols: {module_name}")
        imported[module_name] = symbols

    run_command([sys.executable, "scripts/stage1_healthcheck.py"])
    run_command([sys.executable, "tests/test_virtual_rower_engine.py"])

    result = {
        "stage": "stage2",
        "version": "Alpha12.3",
        "status": "PASS",
        "foundation": "Stage 1 complete",
        "virtual_rower": "ready",
        "imported_modules": imported,
        "next": "Integrate VirtualRowerEngine into the Alpha dashboard.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
