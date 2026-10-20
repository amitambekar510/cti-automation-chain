#!/usr/bin/env python3
"""Create an offline, non-sensitive environment-specific CTI planning document."""
import argparse, json
from pathlib import Path
REQUIRED=("siem","intel_sources","goal","sector","region","telemetry","ai_runtime","approval")
def build(data):
    if not isinstance(data,dict): raise ValueError("Expected object")
    missing=[k for k in REQUIRED if k not in data]
    if missing: raise ValueError("Missing: "+", ".join(missing))
    for k in ("intel_sources","telemetry"):
        if not isinstance(data[k],list) or not all(isinstance(x,str) for x in data[k]): raise ValueError(k+" must be a list of strings")
    for k in set(REQUIRED)-{"intel_sources","telemetry"}:
        if not isinstance(data[k],str) or not data[k].strip(): raise ValueError(k+" must be nonempty")
    def clean(v): return str(v).replace("\n"," ").replace("\r"," ").replace("|","\\|").replace("<","&lt;").replace(">","&gt;")
    lines=["# CTI Automation Chain 2.0 — Environment Plan","","**Planning artifact only — no external service accessed.**","","## Environment",""]
    for k in REQUIRED:
        val=", ".join(data[k]) if isinstance(data[k],list) else data[k]
        lines.append("- **"+clean(k.replace("_"," ").title())+":** "+clean(val))
    lines+=["","## Recommended chain","",
        "1. **R1 Intel:** Validate provenance, date, confidence and applicability of supplied intelligence.",
        "2. **R2 Detection:** Identify supported telemetry and propose SIEM-specific candidate detections.",
        "3. **R3 Automation:** Prepare draft Sigma/IOC/hunt artifacts; do not import or block automatically.",
        "4. **R4 Response:** Prepare analyst-reviewed SITREP and executive briefing with evidence links.",
        "","## Release gates","",
        "- [ ] Confirm lawful source usage and data handling.",
        "- [ ] Check source-to-claim traceability and mark unknowns.",
        "- [ ] Validate target SIEM schema and actual field availability.",
        "- [ ] Test detection candidates in nonproduction against benign and malicious fixtures.",
        "- [ ] Review false positives, tuning, owners and rollback.",
        "- [ ] Approve any production integration or enforcement through change control.",
        "- [ ] Preserve redacted evidence and applicable retention rules.",
        "","## Compliance note","","See docs/compliance-applicability.md. No framework certification or successful deployment is implied."]
    return "\n".join(lines)+"\n"
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    doc=build(json.loads(a.input.read_text(encoding="utf-8")))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(doc,encoding="utf-8")
    print("Wrote",a.output)
if __name__=="__main__":main()
