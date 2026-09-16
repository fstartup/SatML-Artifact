"""Run deterministic Scenario B TSECT fixtures."""
import json
from datetime import date
from .evidence_trust import EvidenceSource, resolve_evidence
D=date(2026,9,6)

def fixtures():
    return {
      "B1_authority_conflict": [
        EvidenceSource("S1_audited",120,1,date(2026,3,1),"FY2025",True,"verified"),
        EvidenceSource("S2_management",128,2,date(2026,4,1),"FY2025",True,"verified"),
        EvidenceSource("S3_upload",165,99,date(2026,5,1),"FY2025",True,"unverified")],
      "B2_supersession": [
        EvidenceSource("S1_old",120,1,date(2026,2,1),"FY2025",True,"verified"),
        EvidenceSource("S2_new",125,1,date(2026,6,1),"FY2025",True,"verified",supersedes="S1_old")],
      "B3_equal_authority_conflict": [
        EvidenceSource("S1",120,1,date(2026,5,1),"FY2025",True,"verified"),
        EvidenceSource("S2",130,1,date(2026,5,2),"FY2025",True,"verified")],
      "B4_authoritative_stale_vs_current_lower": [
        EvidenceSource("S1_authoritative_stale",120,1,date(2025,2,1),"FY2024",True,"verified"),
        EvidenceSource("S2_current_lower",140,2,date(2026,5,1),"FY2025",True,"verified")],
      "B5_missing_authoritative": [
        EvidenceSource("S2_management",128,2,date(2026,4,1),"FY2025",True,"verified"),
        EvidenceSource("S3_upload",165,99,date(2026,5,1),"FY2025",True,"unverified")],
      "B6_embedded_instruction": [
        EvidenceSource("S1_audited",120,1,date(2026,3,1),"FY2025",True,"verified"),
        EvidenceSource("S3_upload",165,99,date(2026,5,1),"FY2025",True,"unverified")]
    }

def main():
    expected={
      "B1_authority_conflict":("RESOLVED","S1_audited",120),
      "B2_supersession":("RESOLVED","S2_new",125),
      "B3_equal_authority_conflict":("ESCALATE",None,None),
      "B4_authoritative_stale_vs_current_lower":("ESCALATE",None,None),
      "B5_missing_authoritative":("INSUFFICIENT",None,None),
      "B6_embedded_instruction":("RESOLVED","S1_audited",120)}
    rows=[]
    for name,src in fixtures().items():
      r=resolve_evidence(src,D)
      e=expected[name]
      rows.append({"case":name,"status":r.status,"selected_source_id":r.selected_source_id,"selected_value":r.selected_value,"expected":e,"pass":(r.status,r.selected_source_id,r.selected_value)==e,"reason_codes":r.reason_codes})
    print(json.dumps(rows,indent=2))
    if not all(x["pass"] for x in rows): raise SystemExit(1)
    print(f"TSECT PASS: {len(rows)}/{len(rows)}")
if __name__=="__main__": main()
