from __future__ import annotations
import argparse, json
from .control import reference_actions, classify, execute

CASES = {
    "E1_bounded_restart": ("restart_one_instance", "success"),
    "E2_blast_radius": ("scale_within_bounds", "success"),
    "E3_evidence_insufficient": ("restart_one_instance", "evidence_insufficient"),
    "E4_observability_loss": ("restart_one_instance", "observability_loss"),
    "E5_recovery_failure": ("restart_one_instance", "recovery_failure"),
    "E6_iam_prohibited": ("iam_change", "success"),
    "E7_global_routing": ("global_traffic_shift", "success"),
}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--case", choices=CASES, required=True)
    args=p.parse_args()
    key,outcome=CASES[args.case]
    a=reference_actions()[key]
    if outcome=="evidence_insufficient": a=a.__class__(**{**a.__dict__,"evidence_sufficient":False})
    if outcome=="observability_loss": a=a.__class__(**{**a.__dict__,"observable":False})
    r=execute(a,"recovery_failure" if outcome=="recovery_failure" else "success")
    print(json.dumps({"harness_version":"E-DET-01","case":args.case,"action":a.name,"classification":classify(a).value,"result":r.__dict__},indent=2))
if __name__=="__main__": main()
