# Prompt Reference

Complete reference of all 44 Feedly CTI prompts organized by report and chain stage.

---

## R1: CTI Prompt Library (Volume 1) — Intelligence Analysis

| ID | File | Name | Description | Output Key |
|----|------|------|-------------|------------|
| R1.01 | `R1-01-diamond-model-intrusion-analysis.md` | Diamond Model of Intrusion Analysis | Standardized Diamond Model framework (Adversary, Infrastructure, Capabilities, Victim) | `diamond_model` |
| R1.02 | `R1-02-red-team-emulation-plans.md` | Red Team Emulation Plans | Red team emulation plans with TTPs | `red_team_plan` |
| R1.03 | `R1-03-visual-attack-flow.md` | Visual Attack Flow | Mermaid/Graphviz attack flow diagrams | `attack_flow` |
| R1.04 | `R1-04-threat-hunt-hypothesis.md` | Threat Hunt Hypothesis | Structured hunt hypothesis package | `hunt_hypothesis` |
| R1.05 | `R1-05-map-threat-actors-to-ttps.md` | Map Threat Actors to TTPs | Actor→TTP matrix with ATT&CK mapping | `actor_ttp_map` |
| R1.06 | `R1-06-vulnerability-assessment-table.md` | Vulnerability Assessment Table | Prioritized vulnerability table | `vuln_assessment` |
| R1.07 | `R1-07-cve-chaining.md` | CVE Chaining | Chained exploit paths | `cve_chains` |
| R1.08 | `R1-08-tariffs-monitoring.md` | Tariffs Monitoring | Trade/tariff threat monitoring | `tariff_monitoring` |
| R1.09 | `R1-09-geopolitical-implications-of-cyberattacks.md` | Geopolitical Implications | Geopolitical analysis of cyberattacks | `geopolitical` |
| R1.10 | `R1-10-industry-threat-intelligence-report.md` | Industry Threat Report | Sector-specific threat intelligence report | `industry_report` |
| R1.11 | `R1-11-vulnerability-advisories.md` | Vulnerability Advisories | Actionable vulnerability advisories | `vuln_advisories` |
| R1.12 | `R1-12-threat-actor-profile.md` | Threat Actor Profile | Comprehensive actor dossier | `actor_profile` |

---

## R2: CTI Prompt Library (Volume 2) — Detection Engineering

| ID | File | Name | Description | Output Key |
|----|------|------|-------------|------------|
| R2.01 | `R2-01-critic-prompt-qa-audit.md` | Critic Prompt QA/Audit | Validate outputs before detection engineering | `qa_audit` |
| R2.02 | `R2-02-source-reliability-credibility-evaluator.md` | Source Credibility Evaluator | Admiralty/NATO source credibility assessment | `source_credibility` |
| R2.03 | `R2-03-mitre-atlas-mapping.md` | MITRE ATLAS Mapping | Map to MITRE ATLAS (AI/ML threats) | `atlas_mapping` |
| R2.04 | `R2-04-detection-opportunity-generator-sentinel-kql.md` | Sentinel KQL Detections | KQL queries + hypotheses table | `sentinel_kql` |
| R2.05 | `R2-05-detection-rule-to-splunk-spl-converter.md` | Splunk SPL Converter | SPL queries + mapping | `splunk_spl` |
| R2.06 | `R2-06-detection-validation-handoff-ttp.md` | Detection Validation Handoff | TTP→Detection mapping for SOC handoff | `validation_handoff` |
| R2.07 | `R2-07-hunt-lead-extraction-prioritization.md` | Hunt Lead Extraction | Prioritized hunt leads | `hunt_leads` |
| R2.08 | `R2-08-hunt-lead-feasibility-coverage.md` | Hunt Feasibility/Coverage | Coverage gap analysis | `hunt_coverage` |
| R2.09 | `R2-09-threat-trend-identification.md` | Threat Trend Identification | Trend identification over time | `threat_trends` |
| R2.10 | `R2-10-stakeholder-feedback-synthesis.md` | Stakeholder Feedback Synthesis | Synthesize stakeholder input | `feedback_synthesis` |
| R2.11 | `R2-11-structured-threat-assessment.md` | Structured Threat Assessment | Comprehensive threat assessment | `threat_assessment` |
| R2.12 | `R2-12-phishing-awareness-newsletter.md` | Phishing Awareness Newsletter | Phishing awareness content | `phishing_newsletter` |
| R2.13 | `R2-13-risk-mitigation-plan.md` | Risk Mitigation Plan | Risk mitigation planning | `risk_mitigation` |
| R2.14 | `R2-14-generic-chain-trigger.md` | Generic Chain Trigger | Trigger for chain automation | `chain_trigger` |

---

## R3: How to Automate Common CTI Workflows — Automation

| ID | File | Name | Description | Output Key |
|----|------|------|-------------|------------|
| R3.01 | `R3-01-ioc-extract-enrich-prompt.md` | IOC Extract/Enrich | Extract & enrich IOCs | `ioc_enrichment` |
| R3.02 | `R3-02-attack-navigator-layer-mapping.md` | ATT&CK Navigator Layer | MITRE ATT&CK Navigator layer JSON | `navigator_layer` |
| R3.03 | `R3-03-diamond-model-intrusion-analysis.md` | Diamond Model Automation | Automated Diamond Model from workflow | `diamond_automated` |
| R3.04 | `R3-04-controls-gap-recommendations.md` | Control Gap Recommendations | Prioritized defense gaps | `control_gaps` |
| R3.04 | `R3-04-controls-gap-recommendations.md` | Control Gap Recommendations | Prioritized defense gaps | `control_gaps` |
| R3.05 | `R3-05-sigma-format-adapter-prompt.md` | Sigma Format Adapter | Convert Sigma to KQL/SPL/YARA/Suricata | `sigma_adapters` |
| R3.06 | `R3-06-sigma-detection-rules.md` | Sigma Detection Rules | Sigma YAML rules (SigmaHQ spec) | `sigma_rules` |
| R3.07 | `R3-07-hunt-hypotheses-package.md` | Hunt Hypotheses Package | Hunt hypotheses package | `hunt_hypotheses` |
| R3.08 | `R3-08-stakeholder-awareness-brief.md` | Stakeholder Awareness Brief | Executive-ready briefs | `awareness_brief` |

---

## R4: Accelerating BFSI CTI Workflows — Response & Reporting

| ID | File | Name | Description | Output Key |
|----|------|------|-------------|------------|
| R4.01 | `R4-01-threat-data-triage.md` | Threat Data Triage | BFSI triage with audit record | `triage` |
| R4.02 | `R4-02-multi-feed-triage-consolidation.md` | Multi-feed Triage | Consolidated multi-feed view | `multi_feed_triage` |
| R4.03 | `R4-03-third-party-ecosystem-risk-assessment.md` | Third-party Risk | Vendor/ecosystem risk assessment | `third_party_risk` |
| R4.04 | `R4-04-fraud-cyber-assessment.md` | Fraud-Cyber Assessment | Unified fraud+cyber assessment | `fraud_cyber` |
| R4.05 | `R4-05-multi-stakeholder-impact-brief.md` | Multi-stakeholder Impact | Cross-functional impact brief | `impact_brief` |
| R4.06 | `R4-06-cross-functional-course-of-action.md` | Cross-functional COA | Cross-functional course of action | `course_of_action` |
| R4.07 | `R4-07-cti-incident-sitrep.md` | CTI Incident SITREP | Iterative incident SITREP | `sitrep` |
| R4.08 | `R4-08-executive-intelligence-brief.md` | Executive Intelligence Brief | Board-ready executive brief | `executive_brief` |
| R4.09 | `R4-09-threat-informed-tabletop-exercise.md` | Tabletop Exercise | Threat-informed tabletop scenario | `tabletop_exercise` |
| R4.10 | `R4-10-resilience-gap-assessment.md` | Resilience Gap Assessment | Resilience gap + roadmap | `resilience_gap` |

---

## Variable Reference

All prompts support these standard variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `[job role]` | Threat Intelligence Analyst | Analyst role |
| `[sector name]` | cross-industry | Industry sector |
| `[country/region]` | global | Geographic region |
| `[stakeholder team names]` | technical security stakeholders | Target teams |
| `[product/service]` | varies | Output product name |
| `[data]` | (required) | Input intelligence data |

### Chain-Specific Variables

| Stage | Additional Variables |
|-------|---------------------|
| R1 | `intel_report`, `threat_feed` |
| R2 | `diamond_model`, `actor_ttp_map`, `actor_profile` |
| R3 | `detections`, `ioc_enrichment`, `sigma_rules` |
| R4 | `sigma_rules`, `ioc_enrichment`, `executive_brief` |

---

## Output Formats

| Stage | Primary Format | Secondary Formats |
|-------|----------------|-------------------|
| R1 | Markdown + Mermaid | Tables, JSON |
| R2 | KQL + SPL + Markdown | Tables, CSV |
| R3 | Sigma YAML + JSON | Markdown, ATT&CK JSON |
| R4 | Markdown + Tables | JSON, CSV |

---

## Validation Rules

| Stage | Validators |
|-------|------------|
| R1 | Diamond model completeness, Actor profile completeness |
| R2 | KQL syntax, SPL syntax, ATT&CK mapping validity |
| R3 | SigmaHQ schema, UUID format, ATT&CK tag validity |
| R4 | SITREP iteration tracking, Confirmed/Assessed/Unknown labels |

---

## Chain Dependencies

```
R1 (Intel) ──▶ R2 (Detection) ──▶ R3 (Automate) ──▶ R4 (Respond)
     │              │                │                │
     └──────────────┴────────────────┴────────────────┘
                    │
                    ▼
            Combined Output
            (all artifacts)
```