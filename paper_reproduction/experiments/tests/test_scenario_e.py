import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
from scenario_e.control import Decision, reference_actions, classify, execute


def test_bounded_restart_can_be_autonomous():
    a=reference_actions()["restart_one_instance"]
    assert classify(a) == Decision.ALLOW
    r=execute(a)
    assert r.executed and not r.escalated


def test_blast_radius_is_conditional():
    a=reference_actions()["scale_within_bounds"]
    assert classify(a) == Decision.CONDITIONAL


def test_evidence_insufficient_escalates():
    a=reference_actions()["restart_one_instance"].__class__(**{**reference_actions()["restart_one_instance"].__dict__,"evidence_sufficient":False})
    r=execute(a)
    assert r.decision == Decision.ESCALATE and not r.executed


def test_observability_loss_escalates():
    a=reference_actions()["restart_one_instance"].__class__(**{**reference_actions()["restart_one_instance"].__dict__,"observable":False})
    assert classify(a) == Decision.ESCALATE


def test_prohibited_iam_action_is_never_autonomous():
    a=reference_actions()["iam_change"]
    assert classify(a) == Decision.PROHIBIT
    assert execute(a).executed is False


def test_recovery_failure_escalates_after_action():
    a=reference_actions()["restart_one_instance"]
    r=execute(a,"recovery_failure")
    assert r.executed is True
    assert r.recovered is False
    assert r.escalated is True


def test_global_routing_is_conditional():
    a=reference_actions()["global_traffic_shift"]
    assert classify(a) == Decision.CONDITIONAL
