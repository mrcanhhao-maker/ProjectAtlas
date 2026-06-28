from engine.environment_check import RuntimeEnvironment, RuntimeEnvironmentChecker


def test_runtime_environment_supports_corebluetooth_candidate_when_all_required_parts_exist():
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

    assert env.supports_corebluetooth_candidate is True


def test_runtime_environment_rejects_corebluetooth_candidate_without_pyobjc():
    env = RuntimeEnvironment(
        system="Darwin",
        machine="x86_64",
        python_version="3.9.6",
        python_major=3,
        python_minor=9,
        compiler_available=True,
        pyobjc_available=False,
        corebluetooth_available=False,
    )

    assert env.supports_corebluetooth_candidate is False


def test_runtime_environment_as_dict_contains_decision_flag():
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

    data = env.as_dict()

    assert data["supports_corebluetooth_candidate"] is False
    assert data["python_version"] == "3.9.6"


def test_runtime_environment_checker_returns_environment_object():
    env = RuntimeEnvironmentChecker().check()

    assert isinstance(env, RuntimeEnvironment)
    assert env.python_major >= 3
