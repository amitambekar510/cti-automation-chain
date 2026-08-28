# Troubleshooting Guide

## Common Issues & Solutions

---

## 1. OpenCode Issues

### "opencode: command not found"
```bash
# Install OpenCode
npm install -g opencode-ai

# Verify installation
opencode --version
```

### "OpenCode timeout"
- Increase timeout in `scripts/run_chain.py`: `timeout=600` (10 minutes)
- Check network connectivity to NVIDIA API
- Reduce prompt complexity

### "OpenCode authentication failed"
```bash
# Re-authenticate
opencode
/connect NVIDIA nvapi-YOUR_KEY
```

### "Model not found"
```bash
# List available models
opencode
/models

# Select correct model
# nvidia/nemotron-3-ultra-550b-a55b
```

---

## 2. Chain Execution Issues

### "Chain config not found"
```
Error: Chain config not found: r1_intel
```
**Fix:** Ensure chain directory exists with `chain.yaml`:
```
chains/
└── r1_intel/
    └── chain.yaml
```

### "Prompt file not found"
```
Error: Prompt not found: prompts/r1/R1-01-...
```
**Fix:** Check file exists in `prompts/r1/` with correct naming.

### "Variable not substituted"
**Symptom:** Output contains `[job role]` literally.
**Fix:** Ensure variables dict includes all required keys:
```python
variables = {
    "job_role": "CTI Analyst",
    "sector_name": "financial-services",
    "country_region": "global",
    "stakeholder_team_names": "SOC,Fraud",
    "data": input_data
}
```

### "Dependency not met"
**Symptom:** Prompt runs before dependency completes.
**Fix:** Add `depends_on` in chain config:
```yaml
prompts:
  - id: "r1-05"
    depends_on: ["diamond_model"]
```

---

## 3. OpenCode API Issues

### "401 Unauthorized"
```
Error: 401 Unauthorized - NVIDIA API key invalid
```
**Fix:**
1. Check API key in config.yaml or env var
2. Verify key at https://build.nvidia.com
3. Check key scopes: `read`, `write`

### "Rate limited"
```
Error: 429 Too Many Requests
```
**Fix:**
- Add delay between prompts
- Reduce concurrent requests
- Check NVIDIA rate limits

### "Context length exceeded"
```
Error: Context window exceeded
```
**Fix:**
- Reduce input size
- Split large inputs
- Use `--loop` mode for iterative processing

---

## 4. Output Validation Issues

### "Sigma rule validation failed"
```
Error: Sigma rule missing 'id' field
```
**Fix:** Ensure Sigma rules have all required fields:
```yaml
title: "Rule Title"
id: "uuid-v4"
status: experimental
logsource:
  product: windows
  category: process_creation
detection:
  selection: ...
  condition: selection
```

### "KQL query syntax error"
```
Error: KQL syntax error
```
**Fix:** Validate KQL in Kusto Explorer or Sentinel before deployment.

### "SPL query syntax error"
```
Error: SPL syntax error
```
**Fix:** Test in Splunk Search before deployment.

### "Schema validation failed"
```
Error: Field 'DeviceProcessEvents' (verify against schema)
```
**Fix:** Tag unverified fields with `(verify against schema)` as per prompt guidelines.

---

## 5. Chain Execution Issues

### "Stage output not passed to next stage"
**Symptom:** Next stage receives empty input.
**Fix:** Ensure stage outputs are combined:
```python
combined = "\n\n---\n\n".join(outputs.values())
current_input = combined
```

### "Variables not persisting between stages"
**Fix:** Ensure stage outputs are added to variables dict:
```python
for key, output in outputs.items():
    variables[key] = output
```

### "Memory/timeout on large inputs"
**Fix:**
- Split large inputs into chunks
- Use `--loop` mode for iterative processing
- Increase timeout: `timeout=600`

---

## 6. Configuration Issues

### "Config file not found"
```
Error: Config file not found: config/config.yaml
```
**Fix:** Copy example config:
```bash
cp config/config.yaml.example config/config.yaml
```

### "Environment variable not expanded"
**Symptom:** `${NVIDIA_API_KEY}` appears literally.
**Fix:** Use `os.path.expandvars()` or set in shell:
```bash
export NVIDIA_API_KEY=your_key
python3 scripts/run_chain.py ...
```

### "YAML parsing error"
```
Error: YAML parsing error
```
**Fix:** Check YAML syntax:
```bash
python3 -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

---

## 7. ELK/SOAR Integration Issues

### "ELK connection failed"
```
Error: Connection refused
```
**Fix:**
- Check host URL and port
- Verify network connectivity
- Check firewall rules

### "ELK authentication failed"
```
Error: 401 Unauthorized
```
**Fix:**
- Verify API key
- Check key permissions
- Check key expiration

### "Index mapping errors"
```
Error: mapper_parsing_exception
```
**Fix:** Create index templates before import:
```bash
PUT /sigma-rules
{
  "mappings": {
    "properties": {
      "title": {"type": "keyword"},
      "id": {"type": "keyword"},
      "tags": {"type": "keyword"},
      "level": {"type": "keyword"}
    }
  }
}
```

---

## 8. Performance Optimization

### Slow Chain Execution
- Reduce prompt complexity
- Use `--stage-only` for testing
- Enable caching for repeated runs
- Use `--stage-only` for debugging single stages

### High API Costs
- Monitor token usage
- Use smaller models for simple tasks
- Cache repeated prompts
- Batch similar requests

### Memory Issues
- Process in batches
- Stream large files
- Clear variables between stages

---

## 9. Debugging Tips

### Enable Debug Logging
```bash
export LOG_LEVEL=DEBUG
python3 scripts/run_chain.py --chain full --input ./intel.md
```

### Save Intermediate Outputs
```bash
# Each stage saves to output/
ls -la output/
```

### Inspect Prompt Rendering
Add debug in `run_chain.py`:
```python
def _render_prompt(self, prompt_text, variables):
    rendered = ...
    print(f"--- Rendered Prompt ---\n{rendered[:500]}...")
    return rendered
```

### Test Single Prompt
```bash
# Test via OpenCode directly
opencode "Your prompt here"
```

---

## 9. Getting Help

### Check Logs
```bash
# OpenCode logs
tail -f ~/.opencode/logs/*.log

# Chain logs
python3 scripts/run_chain.py --chain full --input ./intel.md 2>&1 | tee chain.log
```

### Common Commands
```bash
# Test OpenCode
opencode --version
opencode "Test prompt"

# Test config
python3 -c "import yaml; print(yaml.safe_load(open('config/config.yaml')))"

# Validate outputs
python3 scripts/validate_output.py --path ./output

# Test single stage
python3 scripts/run_stage.py r1 --input ./intel.md
```

### Report Issues
Include:
1. Error message (full)
2. Command run
3. Config (sanitized)
4. Input sample (sanitized)
5. Expected vs actual behavior