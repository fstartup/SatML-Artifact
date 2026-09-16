from __future__ import annotations
import argparse, json
from dataclasses import asdict
from .faults import run_fault, run_all_faults


def main():
    p = argparse.ArgumentParser(description="Run deterministic Scenario E fault-injection cases.")
    p.add_argument("--fault", choices=[f"F{i}" for i in range(1, 9)])
    p.add_argument("--all", action="store_true")
    args = p.parse_args()
    if not args.all and not args.fault:
        p.error("provide --fault F1..F8 or --all")
    results = run_all_faults() if args.all else [run_fault(args.fault)]
    print(json.dumps({
        "harness_version": "E-FAULT-01",
        "synthetic_only": True,
        "fault_count": len(results),
        "results": [asdict(r) for r in results],
    }, indent=2))

if __name__ == "__main__":
    main()
