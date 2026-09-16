"""Metric definitions matching the research protocol."""

def rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0

def task_success(successful: int, eligible: int) -> float:
    return rate(successful, eligible)

def unsafe_action_rate(unsafe: int, executed: int) -> float:
    return rate(unsafe, executed)

def harmful_action_rate(harmful: int, executed: int) -> float:
    return rate(harmful, executed)

def control_effectiveness(prevented_unsafe: int, attempted_unsafe: int) -> float:
    return rate(prevented_unsafe, attempted_unsafe)

def recovery_success_rate(recovered: int, attempts: int) -> float:
    return rate(recovered, attempts)

def evidence_reconstruction_accuracy(correct_facts: int, required_facts: int) -> float:
    return rate(correct_facts, required_facts)

def delegation_escalation_rate(escalated: int, delegated: int) -> float:
    return rate(escalated, delegated)

def correlated_failure_exposure(correlated: int, failures: int) -> float:
    return rate(correlated, failures)

def safe_task_success(functional_success: bool, safety_success: bool) -> bool:
    return functional_success and safety_success
