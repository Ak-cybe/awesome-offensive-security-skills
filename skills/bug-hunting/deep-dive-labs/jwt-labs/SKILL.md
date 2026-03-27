---
name: "JWT Authentication — Complete Deep Dive"
description: "Complete PortSwigger deep-dive with exact payloads for every lab variant including zero-day techniques"
domain: cybersecurity
subdomain: bug-hunting
version: "1.0.0"
category: "bug-hunting/deep-dive-labs"
tags: [portswigger, deep-dive, exploitation, zero-day, lab-solutions]
mitre_attack: ["T1078"]
tools: [burp-suite, curl, sqlmap, ffuf, python, hashcat, ysoserial]
difficulty: "advanced"
---

# JWT Authentication — Complete Deep Dive

> **Deep-Dive Lab Playbook** — Every PortSwigger lab variant with exact payloads,
> bypass techniques, and zero-day extensions. 🟢 Apprentice 🟡 Practitioner 🔴 Expert

## When to Use
- BSCP certification prep
- Real-world bug bounty hunting
- Building exploitation chains
- Understanding bypass techniques

## Prerequisites
- Burp Suite Professional
- Burp Collaborator / interactsh
- Browser with proxy configured


## Workflow
### Phase 1: Reconnaissance
- Identify input vectors, parameters, and application behavior.
### Phase 2: Exploitation
- Apply standard lab payloads.
### Phase 3: Zero-Day Escalation
- Fuzz filters, bypass WAFs, and chain with other vulns.

## Lab Playbooks

### Lab 1: Unverified signature 🟢 APPRENTICE
Decode JWT, change `sub` to `administrator`, re-encode (no signing needed — server doesn't verify).
---

### Lab 2: Flawed signature verification 🟢 APPRENTICE
Remove the signature portion entirely. Server checks signature only if present.
---

### Lab 3: Weak signing key 🟡 PRACTITIONER
```bash
hashcat -a 0 -m 16500 JWT_TOKEN /usr/share/wordlists/rockyou.txt
```
Crack HS256 secret → forge any token.
---

### Lab 4: jwk header injection 🟡 PRACTITIONER
Generate RSA key, sign token with it, embed public key in `jwk` header parameter. Server uses embedded key to verify.
---

### Lab 5: jku header injection 🟡 PRACTITIONER
Host JWK Set on exploit server, set `jku` header to your URL. Server fetches your keys.
---

### Lab 6: kid header path traversal 🟡 PRACTITIONER
```json
{"kid":"../../../dev/null","alg":"HS256"}
```
Sign with empty string (content of `/dev/null`). Server uses file content as verification key.
---

### Lab 7: Algorithm confusion 🔴 EXPERT
Get server's RSA public key → change `alg` to `HS256` → sign with public key as HMAC secret.
```bash
openssl s_client -connect TARGET:443 | openssl x509 -pubkey -noout > public.pem
# Use public.pem as HS256 key to sign forged JWT
```
---

### Lab 8: Algorithm confusion no exposed key 🔴 EXPERT
Get two valid JWTs → derive RSA public key using `rsa_sign2n` tool → then do alg confusion attack.
---



## Blue Team Detection
- Monitor access logs for anomalous payloads.
- Implement strict input validation and parameterized queries where applicable.
- Create WAF rules masking generic attack patterns.

## Zero-Day Research
When standard technique fails:
1. Identify the filter/WAF
2. Fuzz with Burp Intruder custom wordlists
3. Search GitHub/Twitter for new bypasses
4. Chain with other vulns for escalation
5. Try encoding variants: URL, double-URL, unicode, hex


## Key Concepts
| Concept | Description |
|---------|-------------|
| PortSwigger Vectors | Standardized approaches to vulnerability classes. |
| Payload Encoding | Modifying payloads to bypass basic string matching WAFs. |


## Output Format
```
Vulnerability Deep-Dive Report
==============================
Target Vector: [Endpoint]
Bypass Technique: [Explanation of bypass]
Payload Used: [Payload]
Impact Explanation: [Impact]
```

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## 🔵 Blue Team
- Deploy robust WAF rules to detect anomalies.
- Monitor logs for unusual access patterns.

## 🛡️ Remediation & Mitigation Strategy
- **Input Validation:** Sanitize and strictly type-check all inputs.
- **Least Privilege:** Constrain component execution bounds.

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
- [PortSwigger Labs](https://portswigger.net/web-security/all-labs)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [HackTricks](https://book.hacktricks.xyz/)
