# CTI Automation Chain

[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-orange)](https://opencode.ai)
[![Feedly](https://img.shields.io/badge/Feedly-CTI%20Prompts-green)](https://feedly.com/ti-essentials)

---

<p align="center">
  <img src="assets/hero-banner.png" alt="CTI Automation Chain: R1→R2→R3→R4 Feedly CTI Prompt Chaining" width="100%" />
</p>

<p align="center">
  <strong>End-to-End CTI Automation: Feedly Prompt Chaining from Raw Intel to Deployable Detections & SITREPs</strong><br />
  Powered by <strong>Feedly CTI Prompts</strong> + <strong>OpenCode CLI</strong> + <strong>Nemotron 3 Ultra</strong>
</p>

---

## 🎯 Overview

**CTI Automation Chain** implements the complete Feedly CTI Prompt Library as an executable automation pipeline:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    R1       │───▶│    R2       │───▶│    R3       │───▶│    R4       │
│  INTEL      │    │  DETECTION  │    │  AUTOMATE   │    │  RESPOND    │
│  ANALYSIS   │    │  ENGINEERING│    │  WORKFLOWS  │    │  & REPORT   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
  Diamond Model    Sentinel KQL     Sigma Rules        SITREP
  Actor Profiles   Splunk SPL       Hunt Hypotheses    Executive Brief
  Actor-TTP Map    Hunt Leads       ATT&CK Navigator   Resilience Gap
```

---

## 🚀 Quick Start

```bash
# 1. Clone & setup
git clone https://github.com/amitambekar510/cti-automation-chain.git
cd cti-automation-chain
pip install -r requirements.txt

# 2. Configure (copy and edit)
cp config/config.yaml.example config/config.yaml
# Edit config.yaml with your:
#   - OpenCode/NVIDIA API keys
#   - ELK/SOAR endpoints
#   - Sector/region/stakeholders

# 3. Run a chain
python3 scripts/run_chain.py --chain full --input intel-report.md --output ./output/

# 4. Or run individual stages
python3 scripts/run_chain.py --stage r1 --input intel-report.md
python3 scripts/run_chain.py --stage r2 --input ./output/r1_diamond.md
python3 scripts/run_chain.py --stage r3 --input ./output/r2_detections.md
python3 scripts/run_chain.py --stage r4 --input ./output/r3_sigma.md
```

---

## 🔗 Chain Architecture

### **Stage R1: Intelligence Analysis** (`chains/r1_intel/`)
| Prompt | Output | Use Case |
|--------|--------|----------|
| R1.01 Diamond Model | Structured diamond diagram + analysis | Incident analysis, threat assessments |
| R1.02 Red Team Emulation | Emulation plan with TTPs | Red team planning, purple team |
| R1.03 Visual Attack Flow | Mermaid/Graphviz attack flow | Briefings, documentation |
| R1.04 Hunt Hypothesis | Structured hypothesis package | Threat hunting kickoff |
| R1.05 Actor→TTP Map | Actor→TTP matrix | Threat actor tracking |
| R1.06 Vuln Assessment | Prioritized vuln table | Patch prioritization |
| R1.07 CVE Chaining | Chained exploit paths | Exploit chain analysis |
| R1.10 Industry Report | Sector-specific threat report | Board briefings |
| R1.11 Vuln Advisories | Actionable advisory format | Vuln management |
| R1.12 Actor Profile | Comprehensive actor dossier | Threat actor tracking |

### **Stage R2: Detection Engineering** (`chains/r2_detection/`)
| Prompt | Output | SIEM Target |
|--------|--------|-------------|
| R2.04 Sentinel KQL | KQL queries + hypotheses table | Microsoft Sentinel |
| R2.05 Splunk SPL | SPL queries + mapping | Splunk |
| R2.06 Validation Handoff | TTP→Detection mapping | Any SIEM |
| R2.07 Hunt Lead Extraction | Prioritized hunt leads | Threat hunting |
| R2.08 Feasibility/Coverage | Coverage gap analysis | Detection coverage |

### **Stage R3: Workflow Automation** (`chains/r3_automate/`)
| Prompt | Output | Use Case |
|--------|--------|----------|
| R3.01 IOC Extract/Enrich | Structured IOCs + enrichment | IOC management |
| R3.02 ATT&CK Navigator | Navigator layer JSON | Visualization |
| R3.04 Control Gaps | Prioritized gap table | Defense planning |
| R3.05 Sigma Adapter | Format converter | Multi-SIEM |
| R3.06 Sigma Rules | Sigma YAML rules | Any SIEM |
| R3.07 Hunt Hypotheses | Hypothesis package | Threat hunting |
| R3.08 Stakeholder Brief | Executive-ready brief | Leadership comms |

### **Stage R4: Response & Reporting** (`chains/r4_respond/`)
| Prompt | Output | Audience |
|--------|--------|----------|
| R4.01 Triage | Priority + audit record | SOC/Fraud |
| R4.02 Multi-feed Consolidation | Consolidated threat view | CTI team |
| R4.03 Third-party Risk | Vendor risk assessment | Vendor mgmt |
| R4.04 Fraud-Cyber | Unified fraud+cyber view | Fraud+SOC |
| R4.07 SITREP | Iterative incident report | IR/Compliance |
| R4.08 Executive Brief | Board-ready brief | C-suite/Board |
| R4.09 Tabletop Exercise | Exercise scenario + injects | Training |
| R4.10 Resilience Gap | Gap assessment + roadmap | CISO/Leadership |

---

## ⚙️ Configuration

```yaml
# config/config.yaml
openai:
  api_key: "${NVIDIA_API_KEY}"
  base_url: "https://integrate.api.nvidia.com/v1"
  model: "nvidia/nemotron-3-ultra-550b-a55b"

opencode:
  config_path: "~/.config/opencode/opencode.json"

chain:
  default_sector: "financial-services"
  default_region: "global"
  default_stakeholders: "SOC, Fraud, Compliance, Risk"
  auto_validate: true
  max_retries: 3

elk:
  host: "https://your-elk.com"
  api_key: "${ELK_API_KEY}"
  import_on_complete: false

soar:
  enabled: false
  platform: "cortex-xsoar"  # cortex-xsoar | splunk-soar | phantom
```

---

## 📁 Repository Structure

```
cti-automation-chain/
├── README.md
├── LICENSE
├── requirements.txt
├── config/
│   ├── config.yaml.example
│   └── config.yaml
├── chains/
│   ├── r1_intel/
│   │   ├── prompts/
│   │   ├── templates/
│   │   └── validators/
│   ├── r2_detection/
│   │   ├── prompts/
│   │   ├── templates/
│   │   └── validators/
│   ├── r3_automate/
│   │   ├── prompts/
│   │   ├── templates/
│   │   └── validators/
│   └── r4_respond/
│       ├── prompts/
│       ├── templates/
│       └── validators/
├── scripts/
│   ├── run_chain.py
│   ├── run_stage.py
│   ├── validate_output.py
│   └── import_to_elk.py
├── prompts/              # Feedly source prompts (44 total)
│   ├── r1/
│   ├── r2/
│   ├── r3/
│   └── r4/
├── docs/
│   ├── chain_architecture.md
│   ├── prompt_reference.md
│   ├── customization_guide.md
│   └── troubleshooting.md
├── assets/
│   ├── chain-diagram.png
│   └── hero-banner.png
├── tests/
│   ├── test_chains.py
│   └── test_prompts.py
└── examples/
    ├── intel-report.md
    └── output/
```

---

## 🛠️ Requirements

```txt
pyyaml>=6.0
pytest>=7.0
opencode-ai>=0.1.0
pyyaml>=6.0
requests>=2.31
jinja2>=3.1
elasticsearch>=8.0
```

---

## 🎯 Usage Examples

### Full Chain (R1→R2→R3→R4)
```bash
python3 scripts/run_chain.py \
  --chain full \
  --input ./examples/intel-report.md \
  --output ./output/ \
  --sector financial-services \
  --region us \
  --stakeholders "SOC,Fraud,Compliance,Risk"
```

### Single Stage
```bash
# R1 only: Intel report → Diamond Model + Actor Profiles
python3 scripts/run_chain.py --stage r1 --input ./intel.md --output ./r1/

# R2 only: Diamond output → Sentinel KQL + Splunk SPL
python3 scripts/run_chain.py --stage r2 --input ./r1/diamond.md --output ./r2/

# R3 only: Detections → Sigma Rules + Hunt Hypotheses
python3 scripts/run_chain.py --stage r3 --input ./r2/detections.md --output ./r3/

# R4 only: Sigma output → SITREP + Executive Brief
python3 scripts/run_chain.py --stage r4 --input ./r3/sigma.md --output ./r4/
```

### With Custom Input
```bash
python3 scripts/run_chain.py \
  --chain full \
  --input ./my-threat-report.pdf \
  --output ./results/ \
  --config ./config/prod.yaml
```

---

## 📊 Output Artifacts

Each stage produces structured, validated outputs:

| Stage | Artifacts | Format |
|-------|-----------|--------|
| R1 | Diamond model, actor profiles, attack flows | Markdown + Mermaid |
| R2 | KQL/SPL queries, hypotheses table | KQL/SPL + Markdown |
| R3 | Sigma YAML, hunt hypotheses, ATT&CK layers | YAML + JSON |
| R4 | SITREP, Executive brief, Tabletop | Markdown + Tables |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Test specific chain
pytest tests/test_chains.py::test_r1_chain -v

# Validate prompts
python3 scripts/validate_prompts.py --all
```

---

## 🔗 Integration with ELK/SOAR

```bash
# Import all detections to ELK
python3 scripts/import_to_elk.py --host $ELK --key $KEY --all

# Generate Kibana dashboards
python3 scripts/generate_dashboards.py --all

# Export to SOAR
python3 scripts/export_soar.py --platform cortex-xsoar
```

---

## 📚 Documentation

- [Chain Architecture](docs/chain_architecture.md)
- [Prompt Reference](docs/prompt_reference.md)
- [Customization Guide](docs/customization_guide.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Adding new prompts
- Extending chains
- Custom validators
- Testing requirements

---

## 📜 License

MIT License — Free for commercial and non-commercial use.

---

## 👤 Author

**Amit Ambekar**  
🔗 GitHub — [@amitambekar510](https://github.com/amitambekar510)  
🔗 LinkedIn — [Amit Milind Ambekar](https://linkedin.com/in/amitmilindambekar/)  

---

## 🙏 Acknowledgments

- [Feedly](https://feedly.com) for the CTI Prompt Library (Volumes 1-2, Workflows, BFSI)
- [NVIDIA](https://www.nvidia.com/) for Nemotron 3 Ultra
- [OpenCode](https://opencode.ai/) for the agentic CLI
- Security community for feedback and contributions