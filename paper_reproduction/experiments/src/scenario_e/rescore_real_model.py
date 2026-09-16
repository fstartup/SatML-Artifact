from __future__ import annotations
import argparse
import json
from pathlib import Path

try:
    from .evaluator import evaluate_record
except ImportError:
    from evaluator import evaluate_record


def main() -> None:
    p = argparse.ArgumentParser(
        description="Re-score existing Scenario E real-model traces without new model calls."
    )
    p.add_argument("--input", required=True, help="Directory containing existing Scenario E JSON traces")
    p.add_argument(
        "--output",
        default=None,
        help="Optional output directory; defaults to input/rescored_v292",
    )
    args = p.parse_args()

    src = Path(args.input)
    dst = Path(args.output) if args.output else src / "rescored_v292"
    dst.mkdir(parents=True, exist_ok=True)

    files = sorted(src.glob("*.json"))
    if not files:
        raise SystemExit(f"No JSON traces found in {src}")

    rows = []
    for path in files:
        record = json.loads(path.read_text(encoding="utf-8"))
        score = evaluate_record(record)
        record["evaluation_v292"] = score
        out = dst / path.name
        out.write_text(json.dumps(record, indent=2), encoding="utf-8")
        rows.append({"file": path.name, "case": record.get("case"), **score})

    summary = {
        "evaluator_version": "v2.9.2",
        "trace_count": len(rows),
        "behaviorally_compliant": sum(r["behavioral_compliance"] for r in rows),
        "safe_abstentions": sum(r["safe_abstention"] for r in rows),
        "gateway_safety_enforcement_pass": sum(r["gateway_safety_enforcement"] for r in rows),
        "unauthorized_executions": sum(r["unauthorized_execution"] for r in rows),
        "consequence_boundary_violations": sum(r["consequence_boundary_violation"] for r in rows),
        "traces": rows,
    }
    (dst / "summary_v292.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
