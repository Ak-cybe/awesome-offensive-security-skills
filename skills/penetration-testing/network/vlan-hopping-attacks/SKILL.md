---
name: vlan-hopping-attacks
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Execute VLAN Hopping attacks to bypass Layer 2 network segmentation constraints. Exploit 
  misconfigured switch ports utilizing Switch Spoofing natively via Dynamic Trunking Protocol (DTP) 
  and specifically Double Tagging (802.1Q) inherently to unconditionally access isolated networks natively.
domain: cybersecurity
subdomain: penetration-testing
category: Network
difficulty: intermediate
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0008, TA0006]
  techniques: [T1090.001]
platforms: [network, linux]
tags: [network, vlan, vlan-hopping, dtp, yersinia, 802.1q, penetration-testing]
tools: [yersinia, scapy, wireshark]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# VLAN Hopping Attacks

## When to Use
- When conducting Internal Network Penetration Testing to comprehensively validate precisely if explicitly implemented VLAN segmentation restricts intrinsically network traffic To access sensitive segmented specifically networks (e.g., Workflow

### Phase 1: Understanding VLAN Hopping (The Concepts)

```text
# Concept: Virtual Local Area Networks (VLANs) isolate network traffic Attack ```

### Phase 2: Switch Spoofing (Dynamic Trunking Protocol)

```bash
# Concept: Cisco 1. Start specifically Yersinia GUI yersinia -G

# 2. Select ```

### Phase 3: Double Tagging (The 802.1Q Exploit)

```text
# Concept: If 1. Packet ```

### Phase 4: Validating the Hop

```bash
# Concept: Validate ```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Locate Target Switch Port ] --> B[Test DTP Negotiation ]
    B --> C{Switch accepts ```

## 🔵 Blue Team Detection & Defense
- **Explicit Access Ports**: The **VLAN Pruning and Security**: The Key Concepts
| Concept | Description |
|---------|-------------|
| DTP | Dynamic Trunking Protocol |
| 802.1Q | The |
| Switch Spoofing | |

## Output Format
```
Red Team Execution Protocol: VLAN Security Evasion
==================================================
Target Infrastructure: `Access Switch 04`
Vulnerability: Dynamic Trunking Protocol (DTP) Enabled
Severity: High (CVSS 7.2)

Description:
During Action :
```bash
yersinia dtp -attack 1 -interface eth1
```

Impact :
The ```

## References
- Cisco: [VLAN Security White Paper](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/10558-21.html)
- Yersinia Project: [Yersinia Network Tool](https://github.com/tomac/yersinia)
- SANS: [VLAN Hopping Explained](https://www.sans.org/white-papers/1149/)
