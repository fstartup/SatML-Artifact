# Anonymous SaTML Artifact — Consequence-Boundary Control

This artifact supports the deterministic and exploratory evidence reported in the SaTML 2027 manuscript **Failure-Compositional Evaluation of Consequence-Boundary Control in Agentic AI Systems**.

## What can be reproduced without model-provider credentials

From the `experiments/` directory:

```text
python -m pytest -q
```

Expected result for the archived working copy: **82 passed**.

The deterministic Scenario E fault laboratory and compound-fault tests require no provider credentials and are the primary reproducibility target.

## What is included

- Scenario E control, fault, compound-fault, stateful-fault and evaluator implementations.
- Test suite and schemas.
- Fault catalog and experimental protocols.
- Recorded F3/F8 real-model traces.
- Archived F4 result records recovered from the saved experiment transcript; the JSON contents are the recorded provider outputs.
- Architecture, validation, evidence and audit documents used to establish the manuscript's evidence chain.
- Vector figures used by the manuscript.

## Real-model experiments

Real-model adapters are included for inspection and optional reruns. Reruns require the user's own provider credentials and are not required to reproduce the deterministic claims. No credentials are stored in this artifact.

## Anonymization

Author names, employer references, local usernames, private endpoints and branding have been removed or replaced with anonymous placeholders. The artifact contains no production credentials or customer data.

## Scope of reproducibility

The artifact reproduces the implemented synthetic control semantics and exposes the recorded exploratory traces. It does not reproduce closed-model provider internals or guarantee identical future outputs from hosted models.

## Counterfactual ablation

The artifact includes an 11-case bounded-vs-bypass counterfactual ablation covering F1-F8 and C1-C3. The bounded implementation is checked against an independently implemented reference specification. The bypass is an independently implemented synthetic state-transition counterfactual showing which fault-specific consequence would become reachable if the boundary were removed; it is not a live execution path.
