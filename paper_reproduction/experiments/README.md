# Experimental Harness

This directory is the executable research scaffold for the the anonymous research paper.

## First implementation sequence

1. Implement Scenario A in a fully synthetic environment.
2. Implement P0/P1/P2 profiles.
3. Implement immutable event capture and policy decisions.
4. Add ATK01–ATK03 and F01–F03.
5. Run pilot seeds and inspect raw evidence manually.
6. Add automated metric computation.
7. Add evidence-reconstruction evaluator.
8. Add Scenario B–E adapters.
9. Add P3 and delegation tests.
10. Perform power analysis before confirmatory runs.

## Safety rule

Never connect this harness to real production systems, real customer records, real financial decisions, real credentials or uncontrolled external agents. Use synthetic data and isolated disposable environments.

## Real model adapter layer (v0.9)

Scenario A now includes provider adapters for the OpenAI Responses API and
Anthropic Messages API. The adapters are deliberately thin: they generate
model responses and typed tool-call proposals; they do not receive direct
access to the scenario environment. Every state-changing request crosses the
`ScenarioAToolGateway` and deterministic policy engine.

This enables the next experimental comparison:

`scripted harness -> real model P1 -> real model P2 -> evidence/metrics`

The first real-model runs are still pilot experiments. They are not evidence
that a particular vendor/model is safe or unsafe in production.

See `cases/REAL_MODEL_RUNBOOK.md` before running provider-backed experiments.

## Scenario B — Consequential Decision Support

Scenario B is currently in architectural adversarial-design phase. The initial reusable test primitive is the **Three-Source Evidence Conflict Test (TSECT)**, covering source authority, freshness/versioning, legitimate conflict, untrusted evidence and indirect prompt injection. See:

- `cases/SCENARIO_B_CASEBOOK.md`
- `cases/SCENARIO_B_EXPERIMENT_PROTOCOL.md`

No real-model Scenario B calls should be made until the synthetic evidence-trust harness and evaluation controls satisfy the protocol exit criteria.

## Scenario B deterministic TSECT test

Run from the `experiments` directory:

```text
python -m pytest -q
python -m scenario_b.run_tsect
```

On Windows CMD, first set the source path:

```text
set PYTHONPATH=src
python -m pytest -q
python -m scenario_b.run_tsect
```

The TSECT suite uses synthetic evidence only. It makes no LLM/API calls and does not connect to production systems.

## Scenario B real-model pilot

`cases/SCENARIO_B_REAL_MODEL_RUNBOOK.md` defines the minimal B-LLM-01 experiment. TSECT resolves the evidence state before model analysis; the model is evaluated for respecting the resulting evidence boundary.


## Scenario B v2.6 measurement layer

The evaluator now distinguishes untrusted evidence presence from actual adoption and separates bounded recommendation from decision-directed or final-decision behavior. `evidence_refs` are treated as a stronger adoption signal than mere textual mention. The evaluator remains a research heuristic and requires human adjudication for confirmatory studies.

## Scenario E deterministic laboratory

Scenario E is implemented as a synthetic production-operations control harness. From the `experiments` directory on Windows:

```text
set PYTHONPATH=src
python -m pytest -q
python -m scenario_e.runner_e --case E1_bounded_restart
```

Or run the complete deterministic Scenario E case set with `run_scenario_e.cmd`. The harness never connects to real infrastructure.

## Scenario E deterministic fault injection

The fault-injection laboratory is synthetic and requires no model/API calls. Run from
`experiments`:

```text
set PYTHONPATH=src
python -m scenario_e.runner_faults --all
```

Or use `run_scenario_e_faults.cmd`. Faults F1-F8 cover stale evidence, contradictory
evidence, post-action verification loss, recovery failure, remediation loops,
concurrent human state changes, control-plane degradation and ambiguous execution.

## Counterfactual consequence-boundary ablation

The Scenario E laboratory now includes a bounded-vs-bypass counterfactual ablation in `src/scenario_e/ablation.py` and `runner_ablation.py`. It covers F1-F8 and C1-C3 (11 cases).

- **Bounded path:** uses the implemented deterministic gateway/state semantics.
- **Bypass path:** synthetic counterfactual removal of the consequence-boundary check; it is not connected to production infrastructure and does not execute a model.
- **Reference oracle:** independently implemented from the gateway classifier and used to specify the prohibited transition for each fault state.

Run:

```text
PYTHONPATH=src python -m scenario_e.runner_ablation --all --markdown
```

Expected result: 11/11 bounded cases match the independent reference specification, and 11/11 independently modeled counterfactual transitions expose the defined consequence. The ablation supports only the narrower claim that removing the boundary makes specified unsafe successor transitions reachable in the synthetic fault model; it is not a production safety probability estimate.
