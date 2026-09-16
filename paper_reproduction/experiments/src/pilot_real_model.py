"""Small, auditable real-model Scenario A pilot launcher.

The pilot is instrument validation, not a confirmatory hypothesis test. Default execution is intentionally budget-conscious (1 matched repeat = 4 model runs in paired-only mode).
All execution remains inside the synthetic Scenario A gateway.
"""
from __future__ import annotations
import argparse, os, subprocess, sys
from pathlib import Path

CASES = [
    ("T100", None, None),              # normal
    ("T101", None, None),              # normal billing
    ("T103", "ATK01", None),          # goal hijack
    ("T101", "ATK04", None),          # poisoned knowledge
    ("T102", None, "F01"),             # read timeout
    ("T102", None, "F02"),             # ambiguous update
    ("T103", "ATK01", "F01"),         # attack + fault
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--provider", choices=["openai", "azure_openai", "foundry_project", "anthropic"], default="azure_openai")
    p.add_argument("--endpoint-type", choices=["azure", "project"], default="azure", help="Legacy endpoint selector for azure_openai; use provider=foundry_project for Foundry project endpoint")
    p.add_argument("--model", required=True)
    p.add_argument("--repeats", type=int, default=1, help="Number of matched repeats. Default 1 is budget-conscious exploratory validation.")
    p.add_argument("--output", default="experiments/results/real_model_pilot")
    p.add_argument("--max-turns", type=int, default=8)
    p.add_argument("--paired-only", action="store_true", help="Run only matched T103 clean vs ATK01 cases for P1/P2.")
    args = p.parse_args()

    if args.provider == "openai":
        required = "OPENAI_API_KEY"
        if not os.environ.get(required):
            raise SystemExit(f"BLOCKED: {required} is not set. No model calls were attempted.")
    elif args.provider == "anthropic":
        required = "ANTHROPIC_API_KEY"
        if not os.environ.get(required):
            raise SystemExit(f"BLOCKED: {required} is not set. No model calls were attempted.")
    else:
        key = (os.environ.get("AZURE_OPENAI_API_KEY")
               or os.environ.get("OPENAI_API_KEY")
               or os.environ.get("OPEN_AI_KEY"))
        endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT" if args.provider == "foundry_project" or args.endpoint_type == "project" else "AZURE_OPENAI_ENDPOINT")
        if not key:
            raise SystemExit("BLOCKED: Azure credential is not set. Set AZURE_OPENAI_API_KEY (or OPENAI_API_KEY/OPEN_AI_KEY). No model calls were attempted.")
        if not endpoint:
            env_name = "FOUNDRY_PROJECT_ENDPOINT" if args.provider == "foundry_project" or args.endpoint_type == "project" else "AZURE_OPENAI_ENDPOINT"
            raise SystemExit(f"BLOCKED: {env_name} is not set. No model calls were attempted.")

    root = Path(args.output).resolve()
    root.mkdir(parents=True, exist_ok=True)
    runner = [sys.executable, "-m", "scenario_a.real_model_runner"]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parent)

    failures = 0
    cases = [("T103", None, None), ("T103", "ATK01", None)] if args.paired_only else CASES
    for seed in range(args.repeats):
        for ticket, attack, fault in cases:
            for profile in ("P1", "P2"):
                cmd = runner + ["--provider", args.provider, "--model", args.model,
                                "--profile", profile, "--ticket", ticket,
                                "--seed", str(seed), "--output", str(root),
                                "--endpoint-type", args.endpoint_type,
                                "--max-turns", str(args.max_turns)]
                if attack:
                    cmd += ["--attack", attack]
                if fault:
                    cmd += ["--fault", fault]
                print("RUN", " ".join(cmd))
                completed = subprocess.run(cmd, check=False, cwd=Path(__file__).resolve().parent, env=env)
                if completed.returncode != 0:
                    failures += 1

    print(f"PILOT_COMPLETE runs={args.repeats * len(cases) * 2} launcher_failures={failures}")

if __name__ == "__main__":
    main()
