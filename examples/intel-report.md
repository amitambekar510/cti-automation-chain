# Sample Threat Intelligence Report

## Executive Summary
On January 15, 2024, our threat intelligence team identified a sophisticated phishing campaign targeting financial services organizations in North America. The campaign leverages advanced social engineering techniques combined with novel malware delivery methods.

## Technical Details

### Initial Access Vector
- **Vector:** Spear-phishing emails with malicious attachments
- **Attachment Types:** .pdf, .docx with embedded macros
- **Lure Themes:** Invoice processing, compliance updates, vendor payments
- **Sender Spoofing:** Legitimate vendor domains with subdomain spoofing

### Malware Analysis
- **Family:** Custom banking trojan (dubbed "FinStealer v2.1")
- **Delivery:** Macro-enabled documents → PowerShell → Reflective DLL injection
- **Persistence:** Registry Run keys + Scheduled Tasks
- **C2 Infrastructure:** 
  - Primary: `c2.finstealer[.]com` (203.0.113.45)
  - Backup: `api.payment-gateway[.]xyz` (198.51.100.10)
  - Domain Generation Algorithm (DGA) for fallback

### Post-Exploitation Activities
1. **Credential Harvesting:** Browser credential dumping, LSASS dumping via comsvcs.dll
2. **Lateral Movement:** Pass-the-hash, SMB relay, WMI lateral movement
3. **Data Staging:** Compression to `%TEMP%\staging\[random].zip`
4. **Exfiltration:** HTTPS POST to C2, DNS tunneling fallback

### Targeted Entities
- **Primary:** Regional banks (assets $1B-$10B)
- **Secondary:** Credit unions, payment processors
- **Geography:** US (East Coast), Canada (Ontario, BC)

### Attribution
- **Suspected Actor:** FIN7-adjacent group (moderate confidence)
- **Similarities:** 
  - Carbanak/Fin7 TTP overlap (85%)
  - Infrastructure overlap with 2023 campaigns
  - Same DGA algorithm variant
- **Differences:** New malware variant, updated C2 protocol

## Indicators of Compromise

### Network IOCs
| Type | Value | Context |
|------|-------|---------|
| Domain | c2.finstealer[.]com | Primary C2 |
| Domain | api.payment-gateway[.]xyz | Backup C2 |
| IP | 203.0.113.45 | Primary C2 IP |
| IP | 198.51.100.10 | Backup C2 IP |
| Domain Pattern | [a-z]{8,12}\.finstealer\.com | DGA domains |

### File IOCs
| Hash (SHA256) | Filename | Description |
|---------------|----------|-------------|
| a1b2c3d4e5f6... | invoice_20240115.pdf | Macro-enabled dropper |
| f6e5d4c3b2a1... | compliance_update.docx | Macro-enabled dropper |
| 9f8e7d6c5b4a... | FinStealer_v2.1.dll | Main payload |

### Behavioral IOCs
- PowerShell with `-enc` or `-EncodedCommand`
- `rundll32.exe` executing DLLs from `%TEMP%`
- `certutil.exe -decode` for payload decoding
- Scheduled Task creation with random names
- Registry modifications: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`

## MITRE ATT&CK Mapping

| Tactic | Technique | Sub-technique | Description |
|--------|-----------|---------------|-------------|
| Initial Access | T1566.001 | Phishing: Spearphishing Attachment | Macro-enabled docs |
| Execution | T1059.001 | PowerShell | Encoded commands |
| Execution | T1059.003 | Windows Command Shell | Batch scripts |
| Persistence | T1547.001 | Registry Run Keys | HKCU Run keys |
| Persistence | T1053.005 | Scheduled Tasks | Random task names |
| Defense Evasion | T1027 | Obfuscated/Stored Files | Encoded PowerShell |
| Defense Evasion | T1027.009 | Embedded Payloads | DLL in macro |
| Credential Access | T1003.001 | LSASS Memory | comsvcs.dll dump |
| Credential Access | T1555.003 | Browser Credentials | Chrome/Edge/Firefox |
| Discovery | T1082 | System Information | Reconnaissance |
| Discovery | T1083 | File and Directory Discovery | File enumeration |
| Lateral Movement | T1021.004 | Pass the Hash | NTLM relay |
| Lateral Movement | T1021.002 | SMB/Windows Admin Shares | WMI |
| Collection | T1560.001 | Archive Collected Data | ZIP staging |
| Exfiltration | T1041 | Exfiltration Over C2 Channel | HTTPS POST |
| Exfiltration | T1048.003 | Exfiltration Over Alternative Protocol | DNS tunneling |
| Command and Control | T1071.001 | Web Protocols | HTTPS C2 |
| Command and Control | T1008 | Fallback Channels | DGA domains |

## Recommendations

### Immediate Actions
1. Block IOCs at network perimeter (domains, IPs, hashes)
2. Deploy YARA rules for FinStealer v2.1 detection
2. Deploy Sigma rules for PowerShell encoded commands
3. Enable PowerShell Script Block Logging (Event ID 4104)
4. Enable AMSI logging

### Detection Rules
1. **Sigma:** Encoded PowerShell execution (Event ID 4104)
2. **Sigma:** Suspicious Scheduled Task creation
3. **KQL:** DeviceProcessEvents with encoded PowerShell
4. **KQL:** DeviceImageLoadEvents for reflective DLL loading

### Long-term Improvements
1. Implement DMARC enforcement for vendor domains
2. Deploy email sandboxing for macro-enabled attachments
3. Implement application control (AppLocker/WDAC)
4. Deploy EDR with memory scanning capabilities

## References
- Feedly TI Essentials: CTI Prompt Library Vol 1 & 2
- MITRE ATT&CK Enterprise Matrix v15
- CISA Alert AA24-015A: Fin7 Campaigns
- Internal threat intelligence feeds