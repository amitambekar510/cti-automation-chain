# CTI Automation Chain Architecture

## Overview

The CTI Automation Chain implements the Feedly CTI Prompt Library as an executable, chained automation pipeline. Each stage consumes the previous stage's output and produces structured artifacts for the next stage.

## Chain Flow

```
R1: Intelligence Analysis
    │
    ├── Diamond Model (R1.01) ──▶ Core analysis framework
    ├── Actor-TTP Mapping (R1.05) ──▶ Actor→TTP relationships
    ├── Actor Profiles (R1.12) ──▶ Comprehensive actor dossiers
    ├── Red Team Plans (R1.02) ──▶ Emulation plans
    ├── Attack Flows (R1.03) ──▶ Visual attack chains
    ├── Hunt Hypotheses (R1.04) ──▶ Threat hunting kickoff
    ├── Vuln Assessment (R1.06) ──▶ Prioritized vulnerabilities
    ├── CVE Chaining (R1.07) ──▶ Exploit chains
    ├── Industry Reports (R1.10) ──▶ Sector-specific briefs
    ├── Vuln Advisories (R1.11) ──▶ Actionable advisories
    └── Actor Profiles (R1.12) ──▶ Comprehensive dossiers
            │
            ▼
R2: Detection Engineering
    │
    ├── QA/Audit (R2.01) ──▶ Validate R1 outputs
    ├── Sentinel KQL (R2.04) ──▶ Microsoft Sentinel queries
    ├── Splunk SPL (R2.05) ──▶ Splunk queries
    ├── Validation Handoff (R2.06) ──▶ TTP→Detection mapping
    ├── Hunt Leads (R2.07) ──▶ Prioritized hunt leads
    ├── Hunt Coverage (R2.08) ──▶ Coverage gap analysis
    ├── Threat Trends (R2.09) ──▶ Trend identification
    └── Threat Assessment (R2.11) ──▶ Structured assessment
            │
            ▼
R3: Workflow Automation
    │
    ├── IOC Extract/Enrich (R3.01) ──▶ Structured IOCs
    ├── ATT&CK Navigator (R3.02) ──▶ Navigator layers
    ├── Sigma Rules (R3.06) ──▶ Sigma YAML rules
    ├── Sigma Adapter (R3.05) ──▶ Multi-SIEM formats
    ├── Hunt Hypotheses (R3.07) ──▶ Hunt packages
    ├── Control Gaps (R3.04) ──▶ Defense gaps
    └── Awareness Briefs (R3.08) ──▶ Stakeholder comms
            │
            ▼
R4: Response & Reporting
    │
    ├── Triage (R4.01) ──▶ Priority + audit record
    ├── Multi-feed Consolidation (R4.02) ──▶ Consolidated view
    ├── SITREP (R4.07) ──▶ Iterative incident reports
    ├── Executive Brief (R4.08) ──▶ Board-ready briefs
    ├── Tabletop Exercise (R4.09) ──▶ Training scenarios
    └── Resilience Gap (R4.10) ──▶ Gap assessment
```

## Data Flow

Each stage:
1. **Consumes** previous stage's combined output
2. **Executes** multiple prompts in dependency order
3. **Produces** structured artifacts (markdown, YAML, JSON, KQL, SPL)
4. **Validates** outputs against schemas
5. **Passes** combined output to next stage

## Prompt Chaining

Each prompt receives:
- **Static variables**: sector, region, stakeholders, job_role
- **Dynamic variables**: outputs from previous prompts in same chain
- **Chain inputs**: outputs from previous chain stages

Variables are rendered into prompt templates before execution.

## Validation

Each stage validates:
- Required outputs present
- Confidence thresholds met
- Schema compliance (Sigma, KQL, SPL)
- No hallucination indicators

## Extensibility

- Add new prompts to `prompts/r{1-4}/`
- Define new chains in `chains/{name}/chain.yaml`
- Add custom validators in `chains/{name}/validators/`
- Extend output formats in stage configs