from __future__ import annotations
import argparse, json
from dataclasses import asdict
from .ablation import run_ablation, run_all_ablations, as_markdown


def main():
    p = argparse.ArgumentParser(description="Run Scenario E bounded-vs-bypass counterfactual ablation.")
    p.add_argument("--case", choices=[f"F{i}" for i in range(1,9)] + ["C1","C2","C3"])
    p.add_argument("--all", action="store_true")
    p.add_argument("--markdown", action="store_true")
    args = p.parse_args()
    if not args.all and not args.case:
        p.error("provide --case F1..F8/C1..C3 or --all")
    rows = run_all_ablations() if args.all else [run_ablation(args.case)]
    if args.markdown:
        print(as_markdown(rows))
    else:
        print(json.dumps({"harness_version":"E-ABLATION-01","synthetic_only":True,"counterfactual_bypass":True,"cases":len(rows),"results":[asdict(r) for r in rows]}, indent=2))

if __name__ == "__main__":
    main()
