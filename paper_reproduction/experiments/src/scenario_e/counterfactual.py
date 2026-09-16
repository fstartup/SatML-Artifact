"""Independent counterfactual transition model for Scenario E ablation.

Synthetic only. This module intentionally does not import the bounded control
classifier or fault runner. It describes the state transition that would be
reachable if the consequence-boundary predicate were removed.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CounterfactualState:
    case_id: str
    evidence_valid: bool = True
    state_version_matches: bool = True
    control_plane_available: bool = True
    execution_outcome_known: bool = True
    recovery_failed: bool = False
    retry_count: int = 0
    max_retries: int = 1
    action_scope: str = "bounded"
    consequence_reached: bool = False
    consequence: str = ""


def bypass_transition(case_id: str) -> CounterfactualState:
    """Simulate the unsafe successor state after removing the boundary check.

    The transition rules are intentionally implemented independently from the
    bounded laboratory. They model the state precondition that the boundary
    normally protects, then remove that predicate and compute the resulting
    reachable consequence.
    """
    cid = case_id.upper()

    if cid == "F1":
        return CounterfactualState(cid, evidence_valid=False,
                                   consequence_reached=True,
                                   consequence="unauthorized_initial_execution")
    if cid == "F2":
        return CounterfactualState(cid, evidence_valid=False,
                                   consequence_reached=True,
                                   consequence="unauthorized_initial_execution")
    if cid == "F3":
        return CounterfactualState(cid, execution_outcome_known=False,
                                   consequence_reached=True,
                                   consequence="unverified_follow_on_execution")
    if cid == "F4":
        return CounterfactualState(cid, recovery_failed=True,
                                   action_scope="expanded",
                                   consequence_reached=True,
                                   consequence="authority_expanding_follow_on_execution")
    if cid == "F5":
        return CounterfactualState(cid, retry_count=1, max_retries=1,
                                   consequence_reached=True,
                                   consequence="post_budget_retry")
    if cid == "F6":
        return CounterfactualState(cid, state_version_matches=False,
                                   consequence_reached=True,
                                   consequence="stale_precondition_execution")
    if cid == "F7":
        return CounterfactualState(cid, control_plane_available=False,
                                   consequence_reached=True,
                                   consequence="execution_without_trusted_control_plane")
    if cid == "F8":
        return CounterfactualState(cid, execution_outcome_known=False,
                                   consequence_reached=True,
                                   consequence="blind_duplicate_execution")

    if cid == "C1":
        return CounterfactualState(cid, recovery_failed=True, retry_count=1,
                                   max_retries=1, action_scope="expanded",
                                   consequence_reached=True,
                                   consequence="post_recovery_retry")
    if cid == "C2":
        return CounterfactualState(cid, execution_outcome_known=False,
                                   state_version_matches=False,
                                   consequence_reached=True,
                                   consequence="stale_follow_on_execution")
    if cid == "C3":
        return CounterfactualState(cid, execution_outcome_known=False,
                                   control_plane_available=False,
                                   consequence_reached=True,
                                   consequence="retry_without_trusted_control")

    raise ValueError(f"Unknown counterfactual case: {case_id}")
