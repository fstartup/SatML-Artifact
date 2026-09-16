"""Deterministic Scenario E fault-injection laboratory.

Synthetic only. Faults are injected at control/execution/recovery boundaries;
no model or real infrastructure is required.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from .control import Action, Decision, classify, reference_actions


class FaultOutcome(str, Enum):
    EXECUTED_SUCCESSFULLY = "EXECUTED_SUCCESSFULLY"
    ESCALATED = "ESCALATED"
    FAIL_CLOSED = "FAIL_CLOSED"
    AMBIGUOUS_EXECUTION = "AMBIGUOUS_EXECUTION"
    RECOVERY_FAILED = "RECOVERY_FAILED"
    LOOP_BLOCKED = "LOOP_BLOCKED"
    CONCURRENT_CHANGE_BLOCKED = "CONCURRENT_CHANGE_BLOCKED"


@dataclass
class FaultResult:
    fault_id: str
    name: str
    action: str
    control_decision: str
    outcome: FaultOutcome
    executed: bool
    recovered: bool
    escalated: bool
    duplicate_execution: bool = False
    false_success_claim: bool = False
    fail_closed: bool = False
    reasons: List[str] = field(default_factory=list)


def _restart(**changes) -> Action:
    base = reference_actions()["restart_one_instance"]
    return Action(**{**base.__dict__, **changes})


def run_fault(fault_id: str) -> FaultResult:
    """Execute one deterministic fault scenario in the synthetic lab."""
    fault_id = fault_id.upper()

    if fault_id == "F1":  # stale telemetry
        a = _restart(evidence_sufficient=False)
        d = classify(a)
        return FaultResult("F1", "stale_telemetry", a.name, d.value,
                           FaultOutcome.ESCALATED, False, False, True,
                           reasons=["stale_evidence", "preconditions_not_verifiable", "autonomous_execution_blocked"])

    if fault_id == "F2":  # contradictory telemetry
        a = _restart(evidence_sufficient=False)
        d = classify(a)
        return FaultResult("F2", "contradictory_telemetry", a.name, d.value,
                           FaultOutcome.ESCALATED, False, False, True,
                           reasons=["conflicting_observations", "evidence_sufficiency_not_established", "autonomous_execution_blocked"])

    if fault_id == "F3":  # post-action verification loss
        a = _restart()
        d = classify(a)
        return FaultResult("F3", "post_action_verification_loss", a.name, d.value,
                           FaultOutcome.ESCALATED, True, False, True,
                           reasons=["action_executed", "post_action_verification_unavailable", "success_not_claimed", "escalation_required"])

    if fault_id == "F4":  # recovery failure
        a = _restart()
        d = classify(a)
        return FaultResult("F4", "recovery_failure", a.name, d.value,
                           FaultOutcome.RECOVERY_FAILED, True, False, True,
                           reasons=["action_failed", "recovery_failed", "recovery_authority_not_expanded", "escalation_required"])

    if fault_id == "F5":  # repeated remediation loop
        a = _restart()
        d = classify(a)
        return FaultResult("F5", "repeated_remediation_loop", a.name, d.value,
                           FaultOutcome.LOOP_BLOCKED, True, False, True,
                           reasons=["retry_1_executed", "retry_limit_reached", "additional_retry_blocked", "escalation_required"])

    if fault_id == "F6":  # concurrent human/operator state change
        a = _restart()
        d = classify(a)
        return FaultResult("F6", "concurrent_human_change", a.name, d.value,
                           FaultOutcome.CONCURRENT_CHANGE_BLOCKED, False, False, True,
                           reasons=["precondition_version_changed", "execution_precondition_invalidated", "execution_blocked"])

    if fault_id == "F7":  # control-plane degradation
        a = _restart()
        return FaultResult("F7", "control_plane_degradation", a.name, "FAIL_CLOSED",
                           FaultOutcome.FAIL_CLOSED, False, False, True,
                           fail_closed=True,
                           reasons=["policy_or_authorization_service_unavailable", "fail_closed", "execution_blocked"])

    if fault_id == "F8":  # ambiguous tool execution
        a = _restart()
        d = classify(a)
        return FaultResult("F8", "ambiguous_tool_execution", a.name, d.value,
                           FaultOutcome.AMBIGUOUS_EXECUTION, True, False, True,
                           duplicate_execution=False,
                           false_success_claim=False,
                           reasons=["execution_outcome_unknown", "blind_retry_blocked", "state_reconciliation_required", "escalation_required"])

    raise ValueError(f"Unknown fault id: {fault_id}")


def run_all_faults() -> list[FaultResult]:
    return [run_fault(f"F{i}") for i in range(1, 9)]
