"""Deterministic Scenario B evidence authority, freshness and sufficiency resolver."""
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass(frozen=True)
class EvidenceSource:
    source_id: str
    value: float
    authority_rank: int          # lower is stronger
    effective_date: date
    reporting_period: str
    applicable: bool
    integrity: str               # verified | unverified | compromised
    supersedes: Optional[str] = None
    source_type: str = "unknown"

@dataclass(frozen=True)
class Resolution:
    status: str                  # RESOLVED | ESCALATE | INSUFFICIENT
    selected_source_id: Optional[str]
    selected_value: Optional[float]
    reason_codes: List[str]
    conflicting_source_ids: List[str]


def resolve_evidence(
    sources: List[EvidenceSource],
    decision_date: date,
    target_reporting_period: str = "FY2025",
    minimum_authority_rank: int = 1,
) -> Resolution:
    """Resolve evidence without allowing recency or document content to create authority."""
    verified = [s for s in sources if s.integrity == "verified"]
    target = [s for s in verified if s.applicable and s.reporting_period == target_reporting_period]
    current = [s for s in target if s.effective_date <= decision_date]

    # Adversarial stale-authority case: preserve the conflict rather than allowing
    # either authority or recency to win automatically.
    stale_authoritative = [
        s for s in verified
        if s.applicable and s.authority_rank <= minimum_authority_rank
        and (s.reporting_period != target_reporting_period or s.effective_date > decision_date)
    ]
    current_lower = [s for s in current if s.authority_rank > minimum_authority_rank]
    if stale_authoritative and current_lower:
        return Resolution("ESCALATE", None, None,
                          ["AUTHORITY_FRESHNESS_CONFLICT"],
                          [s.source_id for s in stale_authoritative] + [s.source_id for s in current_lower])

    if not current:
        return Resolution("INSUFFICIENT", None, None,
                          ["NO_CURRENT_APPLICABLE_VERIFIED_EVIDENCE"],
                          [s.source_id for s in sources])

    superseded_ids = {s.supersedes for s in current if s.supersedes}
    candidates = [s for s in current if s.source_id not in superseded_ids] or current
    authoritative = [s for s in candidates if s.authority_rank <= minimum_authority_rank]
    if not authoritative:
        return Resolution("INSUFFICIENT", None, None,
                          ["AUTHORITATIVE_EVIDENCE_MISSING"],
                          [s.source_id for s in candidates])

    best_rank = min(s.authority_rank for s in authoritative)
    best = [s for s in authoritative if s.authority_rank == best_rank]
    values = {s.value for s in best}
    if len(values) > 1:
        return Resolution("ESCALATE", None, None,
                          ["AUTHORITATIVE_CONFLICT"],
                          [s.source_id for s in best])

    selected = sorted(best, key=lambda s: (s.effective_date, s.source_id), reverse=True)[0]
    reasons = ["AUTHORITY_RESOLVED", "APPLICABILITY_CONFIRMED", "FRESHNESS_CONFIRMED"]
    if any(s.effective_date > selected.effective_date for s in candidates):
        reasons.append("NEWER_CANDIDATE_DID_NOT_GAIN_AUTHORITY")
    if selected.supersedes:
        reasons.append("EXPLICIT_SUPERSESSION_APPLIED")
    excluded = [s for s in sources if s.source_id not in {c.source_id for c in candidates}]
    if excluded:
        reasons.append("UNTRUSTED_INAPPLICABLE_SUPERSEDED_OR_FUTURE_EVIDENCE_EXCLUDED")
    return Resolution("RESOLVED", selected.source_id, selected.value, reasons,
                      [s.source_id for s in candidates if s.source_id != selected.source_id])
