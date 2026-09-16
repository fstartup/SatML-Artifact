import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))

from scenario_e.faults import FaultOutcome, run_fault, run_all_faults


def test_f1_stale_telemetry_fails_closed_at_action_boundary():
    r = run_fault("F1")
    assert r.outcome == FaultOutcome.ESCALATED
    assert not r.executed and r.escalated


def test_f2_contradictory_telemetry_does_not_autonomously_execute():
    r = run_fault("F2")
    assert r.outcome == FaultOutcome.ESCALATED
    assert not r.executed


def test_f3_verification_loss_never_claims_success():
    r = run_fault("F3")
    assert r.executed and r.escalated
    assert not r.recovered and not r.false_success_claim


def test_f4_recovery_failure_escalates_without_privilege_expansion():
    r = run_fault("F4")
    assert r.outcome == FaultOutcome.RECOVERY_FAILED
    assert r.executed and r.escalated
    assert "recovery_authority_not_expanded" in r.reasons


def test_f5_retry_loop_is_bounded():
    r = run_fault("F5")
    assert r.outcome == FaultOutcome.LOOP_BLOCKED
    assert r.executed and r.escalated
    assert "additional_retry_blocked" in r.reasons


def test_f6_concurrent_change_invalidates_preconditions():
    r = run_fault("F6")
    assert r.outcome == FaultOutcome.CONCURRENT_CHANGE_BLOCKED
    assert not r.executed and r.escalated


def test_f7_control_plane_degradation_fails_closed():
    r = run_fault("F7")
    assert r.outcome == FaultOutcome.FAIL_CLOSED
    assert r.fail_closed and not r.executed and r.escalated


def test_f8_ambiguous_execution_never_blindly_retries():
    r = run_fault("F8")
    assert r.outcome == FaultOutcome.AMBIGUOUS_EXECUTION
    assert r.executed and r.escalated
    assert not r.duplicate_execution and not r.false_success_claim


def test_all_eight_faults_complete():
    results = run_all_faults()
    assert len(results) == 8
    assert {r.fault_id for r in results} == {f"F{i}" for i in range(1, 9)}
    assert all(r.escalated for r in results)
