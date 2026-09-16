import sys
from datetime import date
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from scenario_b.evidence_trust import EvidenceSource,resolve_evidence
D=date(2026,9,6)

def test_authority_beats_untrusted_conflict():
 r=resolve_evidence([EvidenceSource("audited",120,1,date(2026,3,1),"FY2025",True,"verified"),EvidenceSource("upload",165,99,date(2026,5,1),"FY2025",True,"unverified")],D)
 assert (r.status,r.selected_source_id,r.selected_value)==("RESOLVED","audited",120)

def test_explicit_supersession():
 r=resolve_evidence([EvidenceSource("old",120,1,date(2026,2,1),"FY2025",True,"verified"),EvidenceSource("new",125,1,date(2026,6,1),"FY2025",True,"verified",supersedes="old")],D)
 assert (r.status,r.selected_source_id)==("RESOLVED","new")

def test_equal_authority_conflict_escalates():
 r=resolve_evidence([EvidenceSource("a",120,1,date(2026,5,1),"FY2025",True,"verified"),EvidenceSource("b",130,1,date(2026,5,2),"FY2025",True,"verified")],D)
 assert r.status=="ESCALATE"

def test_high_authority_stale_source_does_not_control_new_period():
 r=resolve_evidence([EvidenceSource("stale",120,1,date(2025,2,1),"FY2024",True,"verified"),EvidenceSource("current_lower",140,2,date(2026,5,1),"FY2025",True,"verified")],D)
 assert r.status=="ESCALATE" and "AUTHORITY_FRESHNESS_CONFLICT" in r.reason_codes

def test_missing_authoritative_is_insufficient():
 r=resolve_evidence([EvidenceSource("management",128,2,date(2026,4,1),"FY2025",True,"verified"),EvidenceSource("upload",165,99,date(2026,5,1),"FY2025",True,"unverified")],D)
 assert (r.status,r.selected_source_id)==("INSUFFICIENT",None)

def test_future_effective_source_is_not_current():
 r=resolve_evidence([EvidenceSource("future",150,1,date(2026,10,1),"FY2025",True,"verified")],D)
 assert r.status=="INSUFFICIENT"
