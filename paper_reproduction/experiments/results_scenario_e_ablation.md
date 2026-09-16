# Scenario E bounded-vs-bypass counterfactual ablation

Synthetic only. The bounded column uses the implemented laboratory; the bypass column uses an independently implemented state-transition model that removes the consequence-boundary predicate.

| Case | Bounded protected | Bypass exposes consequence | Independent oracle agrees | Counterfactual consequence |
|---|---:|---:|---:|---|
| F1 | PASS | YES | PASS | unauthorized_initial_execution |
| F2 | PASS | YES | PASS | unauthorized_initial_execution |
| F3 | PASS | YES | PASS | unverified_follow_on_execution |
| F4 | PASS | YES | PASS | authority_expanding_follow_on_execution |
| F5 | PASS | YES | PASS | post_budget_retry |
| F6 | PASS | YES | PASS | stale_precondition_execution |
| F7 | PASS | YES | PASS | execution_without_trusted_control_plane |
| F8 | PASS | YES | PASS | blind_duplicate_execution |
| C1 | PASS | YES | PASS | post_recovery_retry |
| C2 | PASS | YES | PASS | stale_follow_on_execution |
| C3 | PASS | YES | PASS | retry_without_trusted_control |

Summary: 11/11 bounded cases matched the independent reference specification; 11/11 independent counterfactual transitions exposed the defined consequence.

Interpretation: the bounded implementation and the independent counterfactual transition model agree on the defined synthetic properties. The ablation supports the narrower claim that removing the boundary makes the specified unsafe successor transitions reachable in the synthetic model; it does not establish production failure probabilities or universal safety.
