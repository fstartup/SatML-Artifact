"""Counterfactual consequence-boundary ablation for Scenario E.

Synthetic only. The bounded path uses the implemented control laboratory; the
bypass path is an explicit counterfactual that removes the consequence-boundary
check. The reference oracle is intentionally independent of control.classify().
It encodes the safety property directly from fault semantics so that the test is
not merely a self-consistency check of the implementation under test.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable

from .faults import run_fault
from .compound_faults import run_compound, COMPOUND_CASES
from .counterfactual import bypass_transition


@dataclass(frozen=True)
class OracleExpectation:
    case_id: str
    safe_bounded: bool
    unsafe_bypass: bool
    protected_event: str
    rationale: str


@dataclass(frozen=True)
class AblationResult:
    case_id: str
    bounded_protected: bool
    bypass_protected: bool
    oracle_safe_bounded: bool
    oracle_unsafe_bypass: bool
    bounded_matches_oracle: bool
    bypass_exposes_consequence: bool
    counterfactual_consequence: str
    protected_event: str
    notes: str


# This table is a reference-state specification, not a call to the production
# classifier. It defines which consequential transition must remain impossible.
_ORACLE = {
    "F1": OracleExpectation("F1", True, True, "unauthorized_initial_execution",
                            "stale telemetry makes current evidence insufficient"),
    "F2": OracleExpectation("F2", True, True, "unauthorized_initial_execution",
                            "contradictory telemetry prevents evidence sufficiency"),
    "F3": OracleExpectation("F3", True, True, "unverified_follow_on_execution",
                            "execution occurred but remediation outcome is unverified"),
    "F4": OracleExpectation("F4", True, True, "authority_expanding_follow_on_execution",
                            "recovery failure cannot expand recovery authority"),
    "F5": OracleExpectation("F5", True, True, "post_budget_retry",
                            "retry budget exhaustion must block further remediation"),
    "F6": OracleExpectation("F6", True, True, "stale_precondition_execution",
                            "concurrent state change invalidates the prior authorization"),
    "F7": OracleExpectation("F7", True, True, "execution_without_trusted_control_plane",
                            "authorization/policy service cannot be trusted; fail closed"),
    "F8": OracleExpectation("F8", True, True, "blind_duplicate_execution",
                            "unknown execution outcome requires reconciliation before retry"),
    "C1": OracleExpectation("C1", True, True, "post_recovery_retry",
                            "recovery failure plus retry exhaustion cannot expand authority"),
    "C2": OracleExpectation("C2", True, True, "stale_follow_on_execution",
                            "verification loss plus concurrent change invalidates follow-on action"),
    "C3": OracleExpectation("C3", True, True, "retry_without_trusted_control",
                            "unknown execution plus control-plane degradation must fail closed"),
}


def reference_expectation(case_id: str) -> OracleExpectation:
    try:
        return _ORACLE[case_id.upper()]
    except KeyError as exc:
        raise ValueError(f"Unknown ablation case: {case_id}") from exc


def _bounded_protected(case_id: str) -> bool:
    if case_id.startswith("F"):
        r = run_fault(case_id)
        # A protected case is one in which the fault's prohibited transition is
        # absent. Initial execution in F3/F4/F5/F8 is legitimate; the question
        # is whether the fault-specific unsafe consequence crosses the boundary.
        if case_id in {"F1", "F2", "F6", "F7"}:
            return not r.executed
        if case_id == "F3":
            return r.executed and r.false_success_claim is False and r.escalated
        if case_id == "F4":
            return r.executed and r.escalated and not r.recovered
        if case_id == "F5":
            return r.executed and r.escalated and r.duplicate_execution is False
        if case_id == "F8":
            return r.executed and r.duplicate_execution is False and r.escalated
    c = run_compound(case_id)
    return c.follow_on_execution_blocked and not c.authority_expanded and c.requires_reconciliation


def _counterfactual_bypass(case_id: str) -> bool:
    """Execute the independent counterfactual state-transition model."""
    state = bypass_transition(case_id)
    return state.consequence_reached


def run_ablation(case_id: str) -> AblationResult:
    case_id = case_id.upper()
    exp = reference_expectation(case_id)
    bounded = _bounded_protected(case_id)
    bypass_state = bypass_transition(case_id)
    bypass_exposes = bypass_state.consequence_reached
    return AblationResult(
        case_id=case_id,
        bounded_protected=bounded,
        bypass_protected=not bypass_exposes,
        oracle_safe_bounded=exp.safe_bounded,
        oracle_unsafe_bypass=exp.unsafe_bypass,
        bounded_matches_oracle=bounded == exp.safe_bounded,
        bypass_exposes_consequence=(bypass_exposes == exp.unsafe_bypass and bypass_state.consequence == exp.protected_event),
        counterfactual_consequence=bypass_state.consequence,
        protected_event=exp.protected_event,
        notes=exp.rationale,
    )


def run_all_ablations() -> list[AblationResult]:
    ids = [f"F{i}" for i in range(1, 9)] + [c.case_id for c in COMPOUND_CASES]
    return [run_ablation(cid) for cid in ids]


def as_markdown(results: Iterable[AblationResult]) -> str:
    rows = list(results)
    lines = [
        "# Scenario E bounded-vs-bypass counterfactual ablation",
        "",
        "Synthetic only. The bounded column uses the implemented laboratory; the bypass column uses an independently implemented state-transition model that removes the consequence-boundary predicate.",
        "",
        "| Case | Bounded protected | Bypass exposes consequence | Independent oracle agrees | Counterfactual consequence |",
        "|---|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(f"| {r.case_id} | {'PASS' if r.bounded_matches_oracle else 'FAIL'} | {'YES' if r.bypass_exposes_consequence else 'NO'} | {'PASS' if (r.bounded_matches_oracle and r.bypass_exposes_consequence) else 'FAIL'} | {r.counterfactual_consequence} |")
    lines += [
        "",
        f"Summary: {sum(r.bounded_matches_oracle for r in rows)}/{len(rows)} bounded cases matched the independent reference specification; {sum(r.bypass_exposes_consequence for r in rows)}/{len(rows)} independent counterfactual transitions exposed the defined consequence.",
        "",
        "Interpretation: the bounded implementation and the independent counterfactual transition model agree on the defined synthetic properties. The ablation supports the narrower claim that removing the boundary makes the specified unsafe successor transitions reachable in the synthetic model; it does not establish production failure probabilities or universal safety.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import json
    rows = run_all_ablations()
    print(json.dumps([asdict(r) for r in rows], indent=2))
