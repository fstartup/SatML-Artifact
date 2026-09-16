# Scenario A Execution Runbook

## Step 1 — Install only local test dependencies
The first harness milestone should run without network access or cloud credentials.

## Step 2 — Run unit tests
```bash
PYTHONPATH=experiments/src pytest -q experiments/tests/test_scenario_a.py
```

## Step 3 — Run smoke pilot
```bash
PYTHONPATH=experiments/src python experiments/src/pilot_scenario_a.py
```

## Step 4 — Inspect raw evidence
Manually inspect at least one P1 attack run and one P2 attack run before accepting aggregate metrics.

## Step 5 — Introduce real model adapter
Only after the deterministic fixtures pass. The adapter must not receive evaluator ground truth, policy source files, or scoring code.

## Step 6 — Confirmatory design
The pilot estimates variance and failure frequency. Do not call the pilot statistically confirmatory. Perform power analysis and pre-register primary outcomes before the confirmatory run.
