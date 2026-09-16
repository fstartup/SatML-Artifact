# SaTML 2027 Submission Audit — Revision 2

Date: 2026-09-07
Category: Research Paper
Title: Failure-Compositional Evaluation of Consequence-Boundary Control in Agentic AI Systems

## Desk-rejection checks

- IEEEtran conference class: PASS
- Default 10pt geometry: PASS
- Body length: 7 pages before/including conclusion; within 12-page body limit
- References/required non-body sections: Open Science, LLM usage considerations, Ethical Considerations present before references
- Author identity/affiliation in manuscript: none
- company branding in figures: removed
- Embedded figure numbering in artwork: removed; LaTeX captions provide numbering
- Figure/caption numbering consistency: PASS
- No raw Markdown artifacts in PDF: PASS
- No undefined LaTeX citations/references in final build: PASS

## Scientific revision

### Primary research focus
Scenario E autonomous production operations is the primary empirical case. Scenarios A-D provide supporting architectural/adversarial evidence.

### Novelty positioning
The manuscript does not claim invention of deterministic action-boundary enforcement. Related 2026 work is explicitly discussed, including deterministic architectural boundaries, runtime governance, and pre-execution firewall work. The contribution is framed as an integrated consequence-boundary model plus failure-compositional validation and measurement-integrity methodology.

### Counterfactual ablation
Added `experiments/src/scenario_e/ablation.py` and runner/test support.
- 8 isolated faults + 3 compound cases = 11 cases
- bounded implementation compared with independent reference oracle
- synthetic bypass counterfactual is implemented as an independent state-transition model that removes the consequence-boundary predicate
- 11/11 bounded cases match the independent reference property
- 11/11 independent counterfactual transitions expose the defined fault-specific consequence transition
- no model calls and no production infrastructure required

Interpretation is deliberately narrow: the ablation supports that the boundary changes reachable state transitions in the synthetic fault model; it is not a production safety probability estimate.

### Measurement separation
Results distinguish:
1. model behavioral compliance;
2. gateway safety enforcement;
3. consequence-level outcome.
The previous misleading aggregate "gateway enforcement" wording has been narrowed so that model abstention is not counted as gateway rejection.

### Regression
Repository deterministic regression suite: 82 passed.
This is implementation/harness verification, not 82 safety trials.

## Artifact hygiene

- Removed Python caches/compiled files and temporary source files.
- Sanitized local working-directory paths from recorded transcripts.
- Removed author/company identity from artifact text and figures.
- Added ablation protocol and reproducibility instructions.
- Artifact remains synthetic and requires no production credentials or infrastructure.

## Remaining limitations

- Real-model sample remains small and exploratory.
- No model safety ranking or production probability is claimed.
- The bypass condition is an independently implemented counterfactual state-transition model, not a live insecure deployment.
- Trusted identity/policy/execution mediation components are assumed protected.
- Independent replication and larger-scale repeated trials remain future work.
