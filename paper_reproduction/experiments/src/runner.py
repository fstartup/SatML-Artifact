"""Minimal vendor-neutral experiment runner scaffold.

This file intentionally contains interfaces rather than a production agent
implementation. Implement adapters for the selected model/agent framework and
isolated scenario environments without changing the measurement contract.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
import uuid
from pathlib import Path

@dataclass
class RunConfig:
    experiment_id: str
    scenario_id: str
    system_profile_id: str
    seed: int
    model_id: str = "adapter-required"
    model_version: str = "adapter-required"
    agent_version: str = "local"
    policy_version: str = "local"
    toolset_version: str = "local"
    dataset_version: str = "local"
    attack_suite_version: str = "0.1"
    fault_suite_version: str = "0.1"
    harness_version: str = "0.1"

    def fingerprint(self) -> str:
        payload = json.dumps(self.__dict__, sort_keys=True).encode()
        return sha256(payload).hexdigest()

@dataclass
class RunRecorder:
    root: Path
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        self.path = self.root / self.run_id
        self.path.mkdir(parents=True, exist_ok=False)
        self.events = self.path / "events.jsonl"

    def emit(self, event_type: str, **kwargs):
        event = {
            "run_id": self.run_id,
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **kwargs,
        }
        with self.events.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, sort_keys=True) + "\n")
        return event

class ScenarioAdapter:
    def reset(self, seed: int): raise NotImplementedError
    def get_state(self): raise NotImplementedError
    def available_actions(self): raise NotImplementedError
    def apply_action(self, action): raise NotImplementedError
    def observe(self): raise NotImplementedError
    def verify(self, expected_condition): raise NotImplementedError
    def inject_attack(self, attack_id): raise NotImplementedError
    def inject_fault(self, fault_id): raise NotImplementedError
    def ground_truth(self): raise NotImplementedError
    def cleanup(self): raise NotImplementedError

class AgentAdapter:
    def run(self, objective, context, tools, recorder):
        raise NotImplementedError

class PolicyEngine:
    def evaluate(self, action, context):
        """Return an immutable decision: allow/deny/escalate plus reason codes."""
        raise NotImplementedError

def main():
    print("Experimental harness scaffold. Implement ScenarioAdapter, AgentAdapter and PolicyEngine.")

if __name__ == "__main__":
    main()
