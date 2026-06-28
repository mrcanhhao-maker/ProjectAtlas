from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import platform
import shutil
import sys
from typing import Dict


@dataclass(frozen=True)
class RuntimeEnvironment:
    system: str
    machine: str
    python_version: str
    python_major: int
    python_minor: int
    compiler_available: bool
    pyobjc_available: bool
    corebluetooth_available: bool

    @property
    def supports_corebluetooth_candidate(self) -> bool:
        return (
            self.system == "Darwin"
            and self.compiler_available
            and self.pyobjc_available
            and self.corebluetooth_available
        )

    def as_dict(self) -> Dict[str, object]:
        return {
            "system": self.system,
            "machine": self.machine,
            "python_version": self.python_version,
            "python_major": self.python_major,
            "python_minor": self.python_minor,
            "compiler_available": self.compiler_available,
            "pyobjc_available": self.pyobjc_available,
            "corebluetooth_available": self.corebluetooth_available,
            "supports_corebluetooth_candidate": self.supports_corebluetooth_candidate,
        }


class RuntimeEnvironmentChecker:
    def check(self) -> RuntimeEnvironment:
        return RuntimeEnvironment(
            system=platform.system(),
            machine=platform.machine(),
            python_version=platform.python_version(),
            python_major=sys.version_info.major,
            python_minor=sys.version_info.minor,
            compiler_available=self._has_compiler(),
            pyobjc_available=self._module_available("objc"),
            corebluetooth_available=self._module_available("CoreBluetooth"),
        )

    @staticmethod
    def _has_compiler() -> bool:
        return any(
            shutil.which(name) is not None
            for name in ("clang", "gcc", "cc")
        )

    @staticmethod
    def _module_available(module_name: str) -> bool:
        return importlib.util.find_spec(module_name) is not None
