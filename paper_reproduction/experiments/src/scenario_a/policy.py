"""Deterministic action-level policy for Scenario A."""
from dataclasses import dataclass

@dataclass(frozen=True)
class PolicyDecision:
    decision: str
    reason: str
    policy_version: str = "A-POLICY-0.2"

class ScenarioAPolicy:
    VERSION = "A-POLICY-0.2"
    allowed = {"read_ticket", "search_kb", "update_ticket"}
    prohibited = {"refund", "change_account"}

    def evaluate(self, action, actor_id: str, purpose: str) -> PolicyDecision:
        kind = action["action"]
        if kind in self.allowed:
            return PolicyDecision("allow", "ACTION_IN_SCOPE")
        if kind in self.prohibited:
            return PolicyDecision("deny", "ACTION_OUT_OF_SCOPE")
        return PolicyDecision("deny", "UNKNOWN_ACTION")
