# Candidate Reference Architecture — Version 0.5

Status: **Strengthened candidate architecture; not yet canonical or empirically validated.**

## Architecture

The cross-scenario architecture consists of:

1. **Execution Plane** — context, retrieval, memory, planning, model runtime, state, action selection, tool gateway, agent coordination and sandboxed execution.
2. **Control Plane** — identity, authorization, policy, action risk classification, autonomy, delegation, approvals, budgets, rate limits, lifecycle, emergency stop and containment controls.
3. **Evidence Plane** — traces, evaluation, security telemetry, provenance, cost, audit and operational/business outcomes.
4. **Recovery Capability** — detect, contain, rollback/compensate, verify, escalate and learn. Recovery is a cross-cutting capability and must not bypass authorization.

## Consequential action path

**Agent → Action Proposal → Policy Evaluation → Identity/Authorization → Action Risk Classification → Preconditions → Execution Broker → Enterprise/Production System → Verification → Recovery/Escalation**

The agent does not directly convert probabilistic reasoning into unrestricted authority.

## Core invariants

- Autonomous capability does not imply autonomous authority.
- Authority is granted at the action boundary.
- Delegation does not automatically propagate authority.
- Model confidence is not an authorization primitive.
- Evidence must connect intent, authorization, execution and outcome.
- Failure impact must be bounded, not merely made less probable.
- Recovery requires its own authority boundary.
- Evaluation conditions must be protected from manipulation.
- Autonomy must be economically bounded.

## Action authorization tuple

**AA = (Actor, Action, Resource, Purpose, Context, Policy, Impact, Reversibility, Evidence, Time-Bound, Budget-Bound)**

## Autonomous Action Eligibility

An action is eligible for autonomous execution only when:

**Authorization ∧ Policy Compliance ∧ Preconditions ∧ Evidence Sufficiency ∧ Blast-Radius Bound ∧ Observability ∧ Recovery Adequacy ∧ Economic Bound**

are satisfied.

This is a proposed research construct.

## Trust boundaries

TB1 User→Agent; TB2 Agent→Model; TB3 Agent→Tool Gateway; TB4 Tool Gateway→Enterprise System; TB5 Tool/Data Result→Agent; TB6 Agent→Agent; TB7 Agent→Human/Approval; TB8 Agent→Execution Sandbox; TB9 Agent/Build→Credential Broker; TB10 Agent→Repository/Source Control; TB11 Build→Artifact Registry; TB12 Artifact→Deployment Environment; TB13 Agent→Evaluation/Test Control Plane; TB14 Agent→Production Autonomy Control Boundary; TB15 Production Action→Recovery/Containment; TB16 Coordinator→Delegated Agent Authority Context.

## Canonicalization status

Scenarios A–E provide conceptual adversarial support for the model. Canonicalization requires empirical testing, including adversarial evaluation, fault injection, recovery testing, evidence reconstruction, security testing, economic analysis and comparative baselines.
