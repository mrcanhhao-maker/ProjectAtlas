from engine.ble_backend_factory import BleBackendFactory
from engine.environment_check import RuntimeEnvironment
from engine.mock_ble_backend import MockBleBackend


class StubEnvironmentChecker:
    def __init__(self, env: RuntimeEnvironment) -> None:
        self.env = env

    def check(self) -> RuntimeEnvironment:
        return self.env


def test_ble_backend_factory_defaults_to_mock_backend():
    env = RuntimeEnvironment(
        system="Darwin",
        machine="x86_64",
        python_version="3.9.6",
        python_major=3,
        python_minor=9,
        compiler_available=False,
        pyobjc_available=False,
        corebluetooth_available=False,
    )

    selection = BleBackendFactory(StubEnvironmentChecker(env)).create()

    assert selection.name == "mock"
    assert isinstance(selection.backend, MockBleBackend)
    assert selection.native_ready is False


def test_ble_backend_factory_reports_missing_native_dependencies():
    env = RuntimeEnvironment(
        system="Darwin",
        machine="x86_64",
        python_version="3.9.6",
        python_major=3,
        python_minor=9,
        compiler_available=False,
        pyobjc_available=False,
        corebluetooth_available=False,
    )

    selection = BleBackendFactory(StubEnvironmentChecker(env)).create(prefer_native=True)

    assert selection.name == "mock"
    assert "compiler" in selection.reason
    assert "PyObjC" in selection.reason
    assert "CoreBluetooth" in selection.reason


def test_ble_backend_factory_keeps_native_guarded_even_when_environment_ready():
    env = RuntimeEnvironment(
        system="Darwin",
        machine="x86_64",
        python_version="3.11.0",
        python_major=3,
        python_minor=11,
        compiler_available=True,
        pyobjc_available=True,
        corebluetooth_available=True,
    )

    selection = BleBackendFactory(StubEnvironmentChecker(env)).create(prefer_native=True)

    assert selection.name == "corebluetooth_pending"
    assert isinstance(selection.backend, MockBleBackend)
    assert selection.native_ready is True
