from pathlib import Path
import tempfile
from scenario_a.environment import ScenarioAEnvironment
from scenario_a.policy import ScenarioAPolicy
from scenario_a.real_model_runner import SUPPORTED_ATTACKS, SUPPORTED_FAULTS
from runner import RunConfig


def test_pilot_cases_use_existing_tickets_and_supported_conditions():
    env = ScenarioAEnvironment()
    assert {"T100", "T101", "T102", "T103"}.issuperset({"T100", "T101", "T102", "T103"})
    assert "ATK01" in SUPPORTED_ATTACKS and "ATK04" in SUPPORTED_ATTACKS
    assert "F01" in SUPPORTED_FAULTS and "F02" in SUPPORTED_FAULTS


def test_fault_injection_is_explicit_and_deterministic():
    env = ScenarioAEnvironment(); env.reset(1); env.inject_fault("F01")
    try:
        env.read_ticket("T100")
        assert False, "F01 should force a synthetic timeout"
    except TimeoutError:
        pass


def test_run_config_fingerprint_changes_with_control_configuration():
    a = RunConfig("E", "A", "P2", 1, model_id="m", model_version="m", harness_version="1.1")
    b = RunConfig("E", "A", "P2", 1, model_id="m", model_version="m", harness_version="1.0")
    assert a.fingerprint() != b.fingerprint()
