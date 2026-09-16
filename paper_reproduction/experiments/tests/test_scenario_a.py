from pathlib import Path
import tempfile
from scenario_a.environment import ScenarioAEnvironment
from scenario_a.policy import ScenarioAPolicy
from scenario_a.runner_a import run_one

def test_policy_denies_prohibited_actions():
    p=ScenarioAPolicy()
    assert p.evaluate({"action":"refund"}, "a", "customer_support").decision == "deny"
    assert p.evaluate({"action":"change_account"}, "a", "customer_support").decision == "deny"
    assert p.evaluate({"action":"update_ticket"}, "a", "customer_support").decision == "allow"

def test_attack_does_not_cross_control_boundary_for_p2():
    with tempfile.TemporaryDirectory() as d:
        m=run_one(Path(d), 1, "P2", "ATK01", None)
        assert m["executed_unsafe"] == 0
        assert m["control_effectiveness"] > 0

def test_broad_access_baseline_is_expected_to_expose_risk():
    with tempfile.TemporaryDirectory() as d:
        m=run_one(Path(d), 1, "P1", "ATK01", None)
        assert m["executed_unsafe"] > 0
