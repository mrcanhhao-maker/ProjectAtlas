from __future__ import annotations

from dataclasses import dataclass

from engine.ble_backend import BleBackend
from engine.environment_check import RuntimeEnvironment, RuntimeEnvironmentChecker
from engine.mock_ble_backend import MockBleBackend


@dataclass(frozen=True)
class BleBackendSelection:
    name: str
    backend: BleBackend
    reason: str
    native_ready: bool


class BleBackendFactory:
    def __init__(self, environment_checker: RuntimeEnvironmentChecker | None = None) -> None:
        self.environment_checker = environment_checker or RuntimeEnvironmentChecker()

    def create(self, prefer_native: bool = False) -> BleBackendSelection:
        env = self.environment_checker.check()

        if prefer_native and env.supports_corebluetooth_candidate:
            return BleBackendSelection(
                name="corebluetooth_pending",
                backend=MockBleBackend(),
                reason="CoreBluetooth environment detected but native backend is not implemented yet",
                native_ready=True,
            )

        return BleBackendSelection(
            name="mock",
            backend=MockBleBackend(),
            reason=self._mock_reason(env, prefer_native),
            native_ready=False,
        )

    @staticmethod
    def _mock_reason(env: RuntimeEnvironment, prefer_native: bool) -> str:
        if not prefer_native:
            return "Mock backend selected by default for safe tests"

        missing = []
        if env.system != "Darwin":
            missing.append("macOS")
        if not env.compiler_available:
            missing.append("compiler")
        if not env.pyobjc_available:
            missing.append("PyObjC")
        if not env.corebluetooth_available:
            missing.append("CoreBluetooth")

        if missing:
            return "Native BLE unavailable; missing: " + ", ".join(missing)

        return "Native BLE unavailable because CoreBluetooth backend is not implemented yet"
