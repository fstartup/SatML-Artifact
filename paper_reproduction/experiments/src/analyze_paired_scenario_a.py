"""Analyze paired clean-vs-attack Scenario A runs.

This utility compares observed trajectories. It intentionally does not infer
causality from a single pair; it reports behavioral differences that can later
be aggregated across repeated matched runs.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any, Dict


def load_run(path: Path) -> Dict[str, Any]:
    events = path / "events.jsonl"
    if not events.exists():
        raise FileNotFoundError(events)
    metrics = None
    config = None
    action_proposals = []
    for line in events.read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        if e["event_type"] == "run_start":
            config = e.get("configuration", {})
        elif e["event_type"] == "metrics":
            metrics = e
        elif e["event_type"] == "action_proposal":
            action_proposals.append(e.get("action", {}))
    if metrics is None:
        raise ValueError(f"No metrics event in {events}")
    return {"config": config or {}, "metrics": metrics, "actions": action_proposals}


def summarize(label: str, run: Dict[str, Any]) -> Dict[str, Any]:
    m = run["metrics"]
    return {
        "label": label,
        "run_id": m["run_id"],
        "profile": run["config"].get("system_profile_id"),
        "seed": run["config"].get("seed"),
        "attack_id": m.get("attack_id"),
        "untrusted_instruction_present": m.get("untrusted_instruction_present"),
        "actions": [a.get("action") for a in run["actions"]],
        "unsafe_actions_attempted": m.get("unsafe_actions_attempted", 0),
        "unsafe_actions_executed": m.get("unsafe_actions_executed", 0),
        "blocked_unsafe_actions": m.get("blocked_unsafe_actions", 0),
        "safe_task_success": m.get("safe_task_success", False),
        "task_progress": m.get("task_progress", False),
        "refund_count": m.get("refund_count", 0),
        "account_unchanged": m.get("account_unchanged", True),
        "observed_update_statuses": m.get("observed_update_statuses", []),
        "objective_deviation_observation": m.get("objective_deviation_observation", False),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--clean", required=True, type=Path)
    p.add_argument("--attack", required=True, type=Path)
    args = p.parse_args()
    clean = load_run(args.clean)
    attack = load_run(args.attack)
    c = summarize("clean", clean)
    a = summarize("attack", attack)
    diff = {
        "action_sequence_changed": c["actions"] != a["actions"],
        "unsafe_attempt_delta": a["unsafe_actions_attempted"] - c["unsafe_actions_attempted"],
        "unsafe_execution_delta": a["unsafe_actions_executed"] - c["unsafe_actions_executed"],
        "blocked_unsafe_delta": a["blocked_unsafe_actions"] - c["blocked_unsafe_actions"],
        "refund_delta": a["refund_count"] - c["refund_count"],
        "task_progress_changed": c["task_progress"] != a["task_progress"],
        "safe_task_success_changed": c["safe_task_success"] != a["safe_task_success"],
        "update_status_changed": c["observed_update_statuses"] != a["observed_update_statuses"],
    }
    result = {
        "analysis_type": "paired_observation",
        "causal_inference": "not_performed",
        "clean": c,
        "attack": a,
        "observed_difference": diff,
        "interpretation": (
            "Any behavioral difference is an observation requiring aggregation "
            "across matched repeats; it is not by itself evidence of causality."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
