from __future__ import annotations
import argparse, json
from dataclasses import asdict
from .compound_faults import run_compound, run_all_compounds


def main():
    p = argparse.ArgumentParser(description="Run deterministic Scenario E compound-fault closure cases.")
    p.add_argument("--case", choices=[c.case_id for c in run_all_compounds()])
    p.add_argument("--all", action="store_true")
    args = p.parse_args()
    if not args.all and not args.case:
        p.error("provide --case C1..C3 or --all")
    results = run_all_compounds() if args.all else [run_compound(args.case)]
    print(json.dumps({
        "harness_version": "E-COMPOUND-01",
        "synthetic_only": True,
        "case_count": len(results),
        "results": [asdict(r) for r in results],
    }, indent=2))


if __name__ == "__main__":
    main()
