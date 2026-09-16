from pathlib import Path
import csv, statistics
from scenario_a.runner_a import run_pilot

root = Path(__file__).resolve().parents[1] / "results" / "pilot" / "scenario_a"
root.mkdir(parents=True, exist_ok=True)
rows = run_pilot(root, seeds=range(3))
out = root / "summary.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["seed","profile","attack","fault","safe_task_success","executed_unsafe","attempted_unsafe","prevented_unsafe","control_effectiveness"])
    for seed, profile, attack, fault, m in rows:
        w.writerow([seed, profile, attack or "none", fault or "none", m["safe_task_success"], m["executed_unsafe"], m["attempted_unsafe"], m["prevented_unsafe"], m["control_effectiveness"]])
print(f"wrote {len(rows)} runs to {out}")
