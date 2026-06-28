from dataclasses import dataclass
from enum import Enum


class FtmsArchitecture(str, Enum):
    COREBLUETOOTH = "corebluetooth"
    ESP32_BRIDGE = "esp32_bridge"


@dataclass(frozen=True)
class FtmsInteropEvidence:
    peripheral_powered_on: bool
    service_added: bool
    advertising_started: bool
    central_discovers_ftms_service: bool
    central_discovers_ftms_characteristics: bool


@dataclass(frozen=True)
class FtmsArchitectureDecision:
    architecture: FtmsArchitecture
    reason: str


class FtmsArchitectureDecider:
    def decide(self, evidence: FtmsInteropEvidence) -> FtmsArchitectureDecision:
        runtime_ok = (
            evidence.peripheral_powered_on
            and evidence.service_added
            and evidence.advertising_started
        )

        central_ok = (
            evidence.central_discovers_ftms_service
            and evidence.central_discovers_ftms_characteristics
        )

        if runtime_ok and central_ok:
            return FtmsArchitectureDecision(
                architecture=FtmsArchitecture.COREBLUETOOTH,
                reason="CoreBluetooth FTMS is discoverable by an external BLE central.",
            )

        if runtime_ok and not central_ok:
            return FtmsArchitectureDecision(
                architecture=FtmsArchitecture.ESP32_BRIDGE,
                reason=(
                    "CoreBluetooth runtime is healthy, but external BLE central "
                    "does not discover ProjectAtlas FTMS service/characteristics."
                ),
            )

        return FtmsArchitectureDecision(
            architecture=FtmsArchitecture.ESP32_BRIDGE,
            reason="CoreBluetooth runtime is not sufficient for FTMS peripheral delivery.",
        )
