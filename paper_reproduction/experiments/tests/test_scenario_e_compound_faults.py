from scenario_e.compound_faults import run_all_compounds


def test_compound_closure_cases_are_bounded():
    results = run_all_compounds()
    assert len(results) == 3
    assert all(r.executed for r in results)
    assert all(r.follow_on_execution_blocked for r in results)
    assert all(not r.authority_expanded for r in results)
    assert all(r.requires_reconciliation for r in results)
    assert {r.expected_outcome for r in results} == {"ESCALATE", "FAIL_CLOSED"}


def test_c1_retry_pressure_does_not_expand_authority():
    r = next(x for x in run_all_compounds() if x.case_id == "C1")
    assert "additional_retry_blocked" in r.reasons
    assert "authority_not_expanded" in r.reasons


def test_c2_concurrent_change_blocks_follow_on_action():
    r = next(x for x in run_all_compounds() if x.case_id == "C2")
    assert "follow_on_execution_blocked" in r.reasons


def test_c3_control_plane_degradation_fails_closed():
    r = next(x for x in run_all_compounds() if x.case_id == "C3")
    assert r.expected_outcome == "FAIL_CLOSED"
    assert "fail_closed" in r.reasons
