from scenario_e.ablation import run_all_ablations, reference_expectation


def test_reference_oracle_is_independent_and_complete():
    rows = run_all_ablations()
    assert len(rows) == 11
    assert {r.case_id for r in rows} == {f"F{i}" for i in range(1, 9)} | {"C1", "C2", "C3"}


def test_bounded_matches_reference_oracle_for_all_cases():
    rows = run_all_ablations()
    assert all(r.bounded_matches_oracle for r in rows)


def test_counterfactual_bypass_exposes_defined_consequence_for_all_cases():
    rows = run_all_ablations()
    assert all(r.bypass_exposes_consequence for r in rows)
    assert all(r.counterfactual_consequence == r.protected_event for r in rows)


def test_specific_high_value_cases():
    for cid, event in {
        "F3": "unverified_follow_on_execution",
        "F4": "authority_expanding_follow_on_execution",
        "F6": "stale_precondition_execution",
        "F8": "blind_duplicate_execution",
        "C3": "retry_without_trusted_control",
    }.items():
        assert reference_expectation(cid).protected_event == event
