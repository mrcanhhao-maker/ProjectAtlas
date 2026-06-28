from engine.ftms_architecture import (
    FtmsArchitecture,
    FtmsArchitectureDecider,
    FtmsInteropEvidence,
)


def test_decider_keeps_corebluetooth_when_central_discovers_ftms():
    decision = FtmsArchitectureDecider().decide(
        FtmsInteropEvidence(
            peripheral_powered_on=True,
            service_added=True,
            advertising_started=True,
            central_discovers_ftms_service=True,
            central_discovers_ftms_characteristics=True,
        )
    )

    assert decision.architecture == FtmsArchitecture.COREBLUETOOTH
    assert "discoverable" in decision.reason


def test_decider_moves_to_esp32_when_runtime_ok_but_central_cannot_discover_ftms():
    decision = FtmsArchitectureDecider().decide(
        FtmsInteropEvidence(
            peripheral_powered_on=True,
            service_added=True,
            advertising_started=True,
            central_discovers_ftms_service=False,
            central_discovers_ftms_characteristics=False,
        )
    )

    assert decision.architecture == FtmsArchitecture.ESP32_BRIDGE
    assert "external BLE central" in decision.reason


def test_decider_moves_to_esp32_when_corebluetooth_runtime_not_ready():
    decision = FtmsArchitectureDecider().decide(
        FtmsInteropEvidence(
            peripheral_powered_on=False,
            service_added=False,
            advertising_started=False,
            central_discovers_ftms_service=False,
            central_discovers_ftms_characteristics=False,
        )
    )

    assert decision.architecture == FtmsArchitecture.ESP32_BRIDGE
    assert "runtime is not sufficient" in decision.reason
