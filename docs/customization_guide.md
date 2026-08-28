# Customization Guide

## Overview

The CTI Automation Chain is designed to be highly customizable. This guide covers common customization patterns.

---

## 1. Adding New Prompts

### Step 1: Add Prompt File

Create a new markdown file in the appropriate prompts directory:

```
prompts/
├── r1/
│   └── R1-13-new-prompt.md
├── r2/
│   └── R2-15-new-prompt.md
├── r3/
│   └── R3-09-new-prompt.md
└── r4/
    └── R4-11-new-prompt.md
```

Follow the standard prompt format:
```markdown
# Prompt Title

**Source report:** Source Name
**Source URL:** https://...
**Section / workflow:** Section Name

## What this prompt does
Description of what this prompt does.

## Prompt
```
<variables>
[job role]:
[sector name]:
...
</variables>

<context>
...
</context>

<task>
...
</task>

<output_format>
...
</output_format>

<guidelines>
...
</guidelines>
```
```

### Step 2: Add to Chain Configuration

Edit the appropriate chain YAML:

```yaml
# chains/r1_intel/chain.yaml
prompts:
  - id: "r1-13"
    file: "prompts/r1/R1-13-new-prompt.md"
    name: "New Prompt Name"
    output_key: "new_output"
    depends_on: ["diamond_model"]  # optional dependencies
```

### Step 3: Add Validator (Optional)

Create a validator in `chains/r1_intel/validators/new_validator.py`:

```python
def validate_new_output(output: str) -> Tuple[bool, List[str]]:
    """Validate new prompt output"""
    errors = []
    if "required_section" not in output:
        errors.append("Missing required section")
    return len(errors) == 0, errors
```

Register in chain config:
```yaml
validation:
  custom_validators:
    - "chains.r1_intel.validators.new_validator.validate_new_output"
```

---

## 2. Customizing Variables

### Global Variables (config.yaml)

```yaml
chain:
  default_sector: "healthcare"
  default_region: "us"
  default_stakeholders: "SOC, IR, Legal, Compliance"
  default_job_role: "Senior CTI Analyst"
```

### Per-Run Variables

Pass via CLI:
```bash
python3 scripts/run_chain.py \
  --sector healthcare \
  --region us \
  --stakeholders "SOC,IR,Legal" \
  --input ./intel.md
```

### Per-Stage Variables

Override in chain config:
```yaml
prompts:
  - id: "r1-01"
    variables:
      job_role: "Senior Threat Analyst"
      sector_name: "healthcare"
```

---

## 3. Custom Output Formats

### Modify Output Format

In chain config:
```yaml
output:
  combined: false  # Separate files per prompt
  format: "json"   # or "yaml", "markdown"
  filename: "custom_output_{timestamp}.json"
```

### Custom Output Templates

Create template in `chains/r1_intel/templates/custom_output.j2`:

```jinja2
# {{ chain_name }} Output

## Generated: {{ timestamp }}

{% for key, value in outputs.items() %}
## {{ key }}
{{ value }}
---
{% endfor %}
```

Reference in chain config:
```yaml
output:
  template: "templates/custom_output.j2"
```

---

## 4. Adding New Chain Stages

### Step 1: Create Chain Directory

```
chains/
└── r5_custom/
    ├── chain.yaml
    ├── prompts/
    ├── templates/
    └── validators/
```

### Step 2: Define Chain

```yaml
# chains/r5_custom/chain.yaml
chain:
  name: "r5_custom"
  description: "Custom analysis stage"
  stage: 5
  depends_on: ["r4_respond"]
  prompts:
    - id: "custom-01"
      file: "prompts/custom/R5-01-custom.md"
      name: "Custom Analysis"
      output_key: "custom_analysis"
```

### Step 3: Add to Chain Order

In `scripts/run_chain.py`:
```python
self.chain_order = [
    "r1_intel",
    "r2_detection", 
    "r3_automate",
    "r4_respond",
    "r5_custom"  # Add here
]
```

---

## 5. Sector-Specific Customization

### Sector-Specific Variables

Create sector configs in `config/sectors/`:

```yaml
# config/sectors/healthcare.yaml
sector: "healthcare"
region: "us"
stakeholders: "SOC, IR, Compliance, Privacy, Clinical"
job_role: "Healthcare CTI Analyst"
product_service: "Healthcare Threat Intelligence Report"
regulatory_flags:
  - "HIPAA"
  - "HITECH"
  - "HITRUST"
audit_required: true
```

### Load Sector Config

```bash
python3 scripts/run_chain.py \
  --config config/sectors/healthcare.yaml \
  --input ./intel.md
```

### Sector-Specific Prompts

Add sector-specific prompts:
```
prompts/
├── sectors/
│   ├── healthcare/
│   │   ├── R1-01-diamond-model-healthcare.md
│   │   └── R4-01-triage-hipaa.md
│   └── finance/
│       ├── R1-01-diamond-model-finance.md
│       └── R4-01-triage-sec.md
```

---

## 5. SIEM-Specific Customization

### Custom SIEM Targets

Add new SIEM targets in R2 chain:

```yaml
# chains/r2_detection/chain.yaml
prompts:
  - id: "r2-06"
    file: "prompts/r2/R2-06-custom-siem.md"
    name: "Custom SIEM Converter"
    output_key: "custom_siem"
    siem: "custom-siem"
    format: "custom-query-language"
```

### Custom Query Templates

Create templates in `chains/r2_detection/templates/`:

```
templates/
├── kql_template.j2
├── spl_template.j2
├── custom_siem_template.j2
```

---

## 6. Validation Customization

### Custom Validators

Create in `chains/{chain}/validators/`:

```python
# chains/r3_automate/validators/custom_sigma_validator.py
import uuid

def validate_custom_sigma(output: str) -> Tuple[bool, List[str]]:
    errors = []
    
    # Check for required Sigma fields
    required = ['title', 'id', 'status', 'logsource', 'detection']
    for field in required:
        if field + ':' not in output:
            errors.append(f"Missing required Sigma field: {field}")
    
    # Validate UUID format
    import re
    uuid_match = re.search(r'id:\s*([a-f0-9-]{36})', output)
    if uuid_match:
        try:
            uuid.UUID(uuid_match.group(1))
        except ValueError:
            errors.append("Invalid UUID format in id field")
    
    return len(errors) == 0, errors
```

Register:
```yaml
validation:
  custom_validators:
    - "chains.r3_automate.validators.custom_sigma_validator.validate_custom_sigma"
```

---

## 7. Integration Customization

### ELK Customization

```yaml
# config/config.yaml
elk:
  host: "https://elk.company.com:9200"
  api_key: "${ELK_API_KEY}"
  indices:
    sigma: "custom-sigma-rules"
    kql: "custom-kql-queries"
    playbooks: "custom-playbooks"
  pipeline: "cti-enrichment-pipeline"
```

### SOAR Customization

```yaml
soar:
  enabled: true
  platform: "cortex-xsoar"
  playbook_mapping:
    phishing: "Phishing - Generic v2.1"
    malware: "Malware Investigation"
    c2: "C2 Beaconing Response"
  custom_fields:
    incident_type: "CTI Chain Generated"
    source: "cti-automation-chain"
```

---

## 8. Testing Customizations

### Test New Prompts

```bash
# Test single prompt
python3 scripts/run_chain.py --stage r1 --input ./test.md --output ./test_out/

# Validate outputs
python3 scripts/validate_output.py --path ./test_out/
```

### Run Tests

```bash
# Add test in tests/
pytest tests/test_custom_prompt.py -v
```

---

## 9. Environment-Specific Configs

### Development
```yaml
# config/env/development.yaml
chain:
  auto_validate: false
  max_retries: 1
elk:
  import_on_complete: false
log_level: "DEBUG"
```

### Production
```yaml
# config/env/production.yaml
chain:
  auto_validate: true
  max_retries: 3
elk:
  import_on_complete: true
log_level: "INFO"
```

### Load Environment Config
```bash
python3 scripts/run_chain.py \
  --config config/env/production.yaml \
  --input ./intel.md
```

---

## 10. Best Practices

1. **Keep prompts focused** - One prompt, one clear output
2. **Use dependencies** - Explicit `depends_on` prevents race conditions
3. **Validate early** - Add validators for critical outputs
4. **Version control prompts** - Track prompt changes in git
5. **Test incrementally** - Test each stage before chaining
5. **Document assumptions** - Note any environment-specific requirements
6. **Monitor costs** - Track API usage for budget planning