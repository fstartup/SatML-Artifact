import json
from pathlib import Path
from analyze_paired_scenario_a import load_run, summarize


def write_run(tmp_path, name, attack, actions):
    d = tmp_path / name
    d.mkdir()
    events = [
        {"event_type": "run_start", "configuration": {"system_profile_id": "P2", "seed": 0}},
        *[{"event_type": "action_proposal", "action": {"action": action}} for action in actions],
        {"event_type": "metrics", "run_id": name, "attack_id": attack,
         "untrusted_instruction_present": bool(attack), "unsafe_actions_attempted": 0,
         "unsafe_actions_executed": 0, "blocked_unsafe_actions": 0,
         "safe_task_success": True, "task_progress": True, "refund_count": 0,
         "account_unchanged": True},
    ]
    (d / "events.jsonl").write_text("\n".join(json.dumps(x) for x in events) + "\n")
    return d


def test_paired_summary_does_not_infer_causality(tmp_path):
    clean = load_run(write_run(tmp_path, "clean", None, ["read_ticket"]))
    attack = load_run(write_run(tmp_path, "attack", "ATK01", ["read_ticket", "update_ticket"]))
    c = summarize("clean", clean)
    a = summarize("attack", attack)
    assert c["untrusted_instruction_present"] is False
    assert a["untrusted_instruction_present"] is True
    assert c["actions"] != a["actions"]
