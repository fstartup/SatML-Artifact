from scenario_e.stateful_faults import SyntheticState, ExecutionStatus, VerificationStatus, ReconciliationStatus, execute_allowed_restart


def test_f3_execution_then_verification_loss():
    s = SyntheticState()
    execute_allowed_restart(s, "a1", "t1", "F3")
    assert s.state_version == 2
    assert s.execution_status == ExecutionStatus.SUCCEEDED
    assert s.verification_status == VerificationStatus.UNAVAILABLE
    assert s.reconciliation_status == ReconciliationStatus.REQUIRED


def test_f8_unknown_execution_blocks_retry_state():
    s = SyntheticState()
    execute_allowed_restart(s, "a1", "t1", "F8")
    assert s.execution_status == ExecutionStatus.UNKNOWN
    assert s.verification_status == VerificationStatus.UNKNOWN
    assert s.reconciliation_status == ReconciliationStatus.REQUIRED


def test_f4_recovery_failure_does_not_expand_state():
    s = SyntheticState()
    execute_allowed_restart(s, "a1", "t1", "F4")
    assert s.recovery_status.value == "FAILED"
    assert s.reconciliation_status == ReconciliationStatus.REQUIRED


def test_f5_retry_budget_exhausted():
    s = SyntheticState()
    execute_allowed_restart(s, "a1", "t1", "F5")
    assert s.retry_count == s.max_retries
    assert s.reconciliation_status == ReconciliationStatus.REQUIRED
