# AI-guided onboarding — CTI Automation Chain 2.0

When a user supplies this repository URL, **if the AI platform can read GitHub content**, begin an interactive onboarding. Ask exactly **one question at a time**:

1. **Which SIEM and security platforms do you use?** (ELK/Elastic, Microsoft Sentinel, Splunk, other, or none)
2. What existing threat intelligence sources and formats are available (STIX/TAXII, MISP, OpenCTI, reports, manual)?
3. What is your SOC maturity and target output: intelligence summary, detection candidates, IOC review, hunt hypotheses, or executive SITREP?
4. Which operating sector, region and frameworks apply?
5. What telemetry is actually ingested, and which required fields are missing?
6. Which AI provider and execution environment are approved? Are model licenses, costs and data handling acceptable?
7. What change approvals, validation environment, owners and retention policy are available?

**Never request API keys, credentials, customer logs, confidential infrastructure inventories or private indicators.** Use anonymized examples.

After intake, produce: (a) an environment-specific R1→R4 execution map; (b) missing capabilities and prerequisites; (c) a non-secret configuration example; (d) candidate detections with field dependencies, false-positive concerns, and validation steps; (e) a human-approved deployment and rollback plan; (f) applicable audit evidence mapping. Do not invent source citations, ATT&CK technique coverage, detections, SIEM validation or compliance.

For a **safe offline demo**, use `python scripts/plan_environment.py --input examples/environment.sample.json --output /tmp/cti-plan.md`. This creates a plan only; no model, feed or SIEM calls occur.

For real model-backed execution, verify the installed OpenCode CLI command, credentials, vendor data policies, and configuration before running `scripts/run_chain.py`. Model output is untrusted until reviewed.

Pasting a URL alone does not make every AI platform automatically read repository instructions; explicitly ask it to read `AGENTS.md` and this file.
