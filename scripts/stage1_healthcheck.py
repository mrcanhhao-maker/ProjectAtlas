#!/usr/bin/env python3
from __future__ import annotations

import importlib
import json
import py_compile
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
    "plugins/visionrow/alpha10/app_alpha10.py",
]

REQUIRED_MODULES = [
    "engine.pose_engine",
    "engine.stroke_v3",
    "engine.quality_engine",
    "engine.motion_metrics",
    "engine.stroke_validator",
    "engine.stroke_history",
]


def fail(message: str) -> None:
    print(json.dumps({"stage": "stage1", "status": "FAIL", "error": message}, ensure_ascii=False, indent=2))
    sys.exit(1)


def public_symbols(module) -> list[str]:
    return sorted(
        name for name in dir(module)
        if not name.startswith("_")
    )


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail(f"Missing required files: {missing}")

    compiled = []
    for path in REQUIRED_FILES:
        source = ROOT / path
        py_compile.compile(str(source), doraise=True)
        compiled.append(path)

    imported = {}
    for module_name in REQUIRED_MODULES:
        module = importlib.import_module(module_name)
        symbols = public_symbols(module)
        if not symbols:
            fail(f"Module has no public production symbols: {module_name}")
        imported[module_name] = symbols

    result = {
        "stage": "stage1",
        "version": "Alpha11.2",
        "status": "PASS",
        "compiled_files": compiled,
        "imported_modules": imported,
        "next": "Stage 1 foundation is healthy. Continue to Stage 1 final lock before Virtual Rower Engine.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
