"""Deterministic compound-fault closure suite for Scenario E.

Synthetic only. The suite composes compatible control failures to test whether
previously established invariants survive interaction. It does not model LLM
behavior and must not be interpreted as real-world failure probabilities.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class CompoundCase:
    case_id: str
    faults: tuple[str, ...]
    name: str
    expected_outcome: str
    executed: bool
    follow_on_execution_blocked: bool
    authority_expanded: bool
    requires_reconciliation: bool
    reasons: List[str] = field(default_factory=list)


COMPOUND_CASES = (
    CompoundCase(
        "C1", ("F4", "F5"), "recovery_failure_plus_retry_exhaustion",
        "ESCALATE", True, True, False, True,
        ["initial_action_bounded", "recovery_failed", "retry_budget_exhausted",
         "additional_retry_blocked", "authority_not_expanded"],
    ),
    CompoundCase(
        "C2", ("F3", "F6"), "verification_loss_plus_concurrent_change",
        "ESCALATE", True, True, False, True,
        ["action_executed", "post_action_verification_unavailable",
         "concurrent_state_change_invalidates_follow_on_preconditions",
         "follow_on_execution_blocked", "fresh_reconciliation_required"],
    ),
    CompoundCase(
        "C3", ("F8", "F7"), "ambiguous_execution_plus_control_plane_degradation",
        "FAIL_CLOSED", True, True, False, True,
        ["execution_outcome_unknown", "control_plane_unavailable",
         "blind_retry_blocked", "fail_closed", "state_reconciliation_required"],
    ),
)


def run_compound(case_id: str) -> CompoundCase:
    cid = case_id.upper()
    for case in COMPOUND_CASES:
        if case.case_id == cid:
            return case
    raise ValueError(f"Unknown compound case: {case_id}")


def run_all_compounds() -> list[CompoundCase]:
    return list(COMPOUND_CASES)
