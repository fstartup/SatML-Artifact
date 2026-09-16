# Final Evidence Matrix — Manuscript Closure v0.1

## Purpose

This matrix is the closure artifact for the current manuscript. It maps the principal architectural claims to their evidence class and prevents exploratory observations from being promoted into empirical guarantees.

## Evidence classes

- **Established:** directly supported by cited external literature or standards.
- **Synthesized:** engineering principle derived by integrating established sources and scenario analysis.
- **Proposed:** construct, invariant, metric, or architecture introduced by this work.
- **Exploratory observation:** observed in the synthetic laboratory and/or limited real-model traces; not statistically generalizable.
- **Open:** requires broader empirical validation and is not claimed as established by this manuscript.

## Closure matrix

| Claim / construct | Evidence basis | Current strength | Permitted manuscript wording | Remaining limitation |
|---|---|---|---|---|
| Autonomous capability should not imply autonomous authority | Cross-scenario synthesis; A-E architecture analysis | Synthesized + proposed | "The framework treats capability and authority as separate concerns." | Broader production replication remains open. |
| Consequential authority belongs at the relevant action/consequence boundary | Scenarios A, B, E; I1/I2/I20 | Synthesized + proposed | "Authority is granted and enforced at the relevant consequence boundary." | Boundary classification remains domain-specific. |
| Deterministic controls should surround probabilistic model proposals | Scenario A/E harness; gateway architecture | Proposed + deterministic validation | "The tested gateway prevented unauthorized consequential execution under the defined synthetic conditions." | Not proof of universal model robustness. |
| Evidence is not self-authorizing instruction | Scenario B TSECT; I11/I19 | Proposed + deterministic validation + exploratory model observations | "Retrieved evidence must carry independently governed authority attributes and must not self-authorize action or decision use." | Real-world document ecosystems require broader validation. |
| Decision authority should remain separate from recommendation generation | Scenario B; I12/I18/I20 | Synthesized + proposed + exploratory observation | "Recommendation generation does not itself confer final decision authority." | Decision-influence effects need larger empirical study. |
| Execution does not establish successful outcome | Scenario E F3; I21 | Proposed + exploratory observation + deterministic validation | "Execution and outcome verification are distinct states." | More complex distributed execution remains open. |
| Failure must not expand authority | Scenario E F4 and C1; I22 | Proposed + deterministic validation + 2-model exploratory observation | "The framework requires authority to remain monotonic under failure." | Limited model sample; no production deployment evidence. |
| Concurrent state change invalidates stale follow-on action | Scenario E C2 | Proposed + deterministic validation | "Follow-on action requires current preconditions after relevant state change." | Larger concurrency patterns remain open. |
| Unknown execution outcome must not trigger blind retry | Scenario E F8 and C3 | Proposed + exploratory observation + deterministic validation | "Unknown execution state requires reconciliation before consequential retry." | More tool/transaction semantics remain open. |
| Recovery is an independently bounded capability | Scenario E F4; I7/I22 | Synthesized + proposed + deterministic/exploratory evidence | "Recovery does not inherit broader authority merely because the preceding action failed." | Recovery in heterogeneous production environments remains open. |
| Multi-agent delegation must not create transitive privilege | Scenario D; I3 | Synthesized + proposed | "Delegation must be explicitly scoped and non-escalating." | Large-scale multi-agent empirical validation remains open. |
| Shared memory requires trust/provenance classification | Scenario D | Proposed | "Shared memory should be treated as governed state rather than implicitly trusted context." | Empirical poisoning rates remain open. |
| Consensus is not independent corroboration | Scenario D; CFE construct | Proposed | "Agreement among dependent agents does not by itself establish evidence independence." | Quantitative CFE validation remains open. |
| Production autonomy eligibility depends on controllability, not task success alone | Scenario E; AAE construct | Proposed + deterministic reasoning | "Eligibility should account for impact, reversibility, blast radius, evidence, authorization, observability, recovery and economics." | Quantitative threshold calibration remains open. |
| Economic limits are part of safety control | Cross-scenario economics; I9 | Synthesized + proposed | "Agentic autonomy requires bounded economic envelopes." | Large-scale cost distributions remain open. |
| Evaluation must itself be protected from agent manipulation | Scenario C/D and evaluator audits | Synthesized + proposed | "Evaluation integrity is a control-plane concern." | Independent red-team validation remains open. |

## Scenario E empirical record

The current real-model stateful sample contains six exploratory trajectories:

- GPT-5-nano × F3
- GPT-5-nano × F8
- GPT-5-nano × F4
- Claude Haiku 4.5 × F3
- Claude Haiku 4.5 × F8
- Claude Haiku 4.5 × F4

Across these six trajectories:

- no false-success claim was recorded;
- no blind retry was proposed;
- reconciliation/escalation was observed after the tested failure states;
- no unauthorized execution was recorded;
- no consequence-boundary violation was recorded.

These observations are exploratory and synthetic. They do not establish production failure probabilities, universal prompt-injection robustness, model superiority, or statistical generalization.

## Deterministic closure record

Scenario E deterministic F1-F8 and compound cases C1-C3 are control-laboratory results. The compound cases specifically test composition of previously established boundaries:

- **C1 — F4 + F5:** recovery failure plus retry exhaustion → escalation, retry blocked, authority unchanged.
- **C2 — F3 + F6:** verification loss plus concurrent change → escalation, stale follow-on execution blocked.
- **C3 — F8 + F7:** ambiguous execution plus control-plane degradation → fail closed, blind retry blocked, reconciliation required.

These results validate the synthetic control implementation, not real-world reliability.

## Absolute finding supported by the current evidence

> **Production-grade agentic systems should not derive consequential authority from model capability alone. Authority should be granted explicitly at the relevant consequence boundary and enforced through deterministic policy, authorization, evidence, impact, state, recovery, and economic controls. In the tested synthetic scenarios, this separation prevented unauthorized consequential execution under the defined attack and fault conditions.**

## Claims explicitly not made

This manuscript does **not** claim:

1. universal safety of LLM-based agents;
2. a measured production failure probability;
3. that either tested model is safer than the other;
4. causal conclusions from the limited paired traces;
5. production readiness;
6. complete resistance to prompt injection or adversarial manipulation;
7. statistical generalization across models, vendors, domains, or infrastructures;
8. that the proposed metrics are established industry standards;
9. that the architecture replaces NIST, ISO, OWASP, regulatory guidance, or established engineering controls.

## Closure decision

The current experiment program is considered **closed for isolated fault discovery**. Further experiments are justified only if they can materially falsify a core invariant, expose an evaluator/control defect that changes an existing conclusion, test a materially different authority boundary required by the manuscript, or satisfy a specifically identified empirical evidence gap.
