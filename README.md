# SaTML 2027 Anonymous Artifact — Consequence-Boundary Control

This repository contains the anonymous artifact supporting the paper:

**Failure-Compositional Evaluation of Consequence-Boundary Control in Agentic AI Systems**

## Reproduction target

The primary reproducibility target is the deterministic implementation. It requires no model-provider credentials.

From `paper_reproduction/experiments/`:

```text
python -m pytest -q
```

Expected result for this artifact revision: **82 passed**.

The artifact also contains the 8-fault Scenario E laboratory (F1–F8), 3 compound cases (C1–C3), and the 11-case bounded-vs-bypass counterfactual ablation.

## Repository map

- `paper_reproduction/` — executable research implementation, tests, protocols, schemas, figures, manuscript source and PDF.
- `recorded_model_traces/` — scrubbed exploratory stateful traces for the two evaluated providers/models.
- `documentation/` — architecture, evaluation, evidence, manuscript-audit and citation-audit documents.
- `SHA256SUMS.txt` — integrity manifest for all release files.

## Scope

The deterministic experiments reproduce the implemented synthetic control semantics reported in the paper. Recorded model traces support inspection of exploratory observations. Closed-model provider internals and identical future hosted-model outputs are not claimed to be reproducible.

Provider-backed reruns are optional and require the researcher's own credentials. No credentials, customer data, production endpoints, or private infrastructure are included.

## Anonymity

This repository is intentionally anonymous for double-blind review. It contains no author names, affiliations, personal identifiers, employer identifiers, private paths, or author-linked public profiles.

## Integrity

The artifact was synchronized to the canonical manuscript before packaging. The deterministic regression result and artifact-to-manuscript consistency were independently checked during the submission preparation audit.

## Review freeze

The repository may be updated through the SaTML 2027 artifact-update deadline. After the final artifact update, the review copy should remain accessible and unedited, consistent with the venue requirements.
