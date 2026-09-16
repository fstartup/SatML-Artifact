# Evaluation Model — Version 0.5

Agent evaluation must operate at multiple levels:

1. **E1 — Model**: capability, factuality, reasoning and instruction adherence.
2. **E2 — Action**: whether individual actions were valid, authorized, safe and appropriate.
3. **E3 — Trajectory**: whether the sequence of decisions, tool calls, observations, retries and replanning was acceptable.
4. **E4 — Outcome**: whether the intended business/operational result was achieved without unacceptable harm.

## Cross-scenario evidence model

For analytical systems:

**Source → Observation → Agent Claim → Verification → Analysis → Synthesis → Output**

For consequential operations:

**Intent → Context → Diagnosis/Decision → Evidence → Policy → Authorization → Preconditions → Action → Observation → Verification → Recovery → Outcome**

## Evaluation integrity

The evaluation environment must be protected against agent manipulation. The agent should not be able to alter the test data, grading mechanism, evidence store, monitoring controls or acceptance criteria used to judge its own performance.

## Production evaluation

Evaluation should include:

- representative deployment conditions;
- adversarial testing;
- fault injection;
- state drift;
- concurrent human activity;
- tool failure and partial success;
- recovery testing;
- security testing;
- cost/latency measurement;
- evidence reconstruction;
- regression testing after model, prompt, policy, tool or environment changes.

NIST's AI RMF emphasizes documented evaluation, human oversight and monitoring in deployment; current NIST work also identifies fragmented logging, drift detection and the integration of automated and human-validated monitoring as active challenges. [1][2]

## References

[1] NIST, AI Risk Management Framework 1.0, 2023.
[2] NIST, Challenges to the Monitoring of Deployed AI Systems, 2026.
