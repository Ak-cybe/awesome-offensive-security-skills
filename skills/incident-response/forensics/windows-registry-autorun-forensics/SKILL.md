---
name: windows-registry-autorun-forensics
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Analyze the Windows Registry to uncover malicious persistence mechanisms. This skill details 
  how to investigate Run keys, Services, Scheduled Tasks registry keys, and Image File Execution 
  Options (IFEO) to locate hidden backdoors.
domain: cybersecurity
subdomain: incident-response
category: Forensics
difficulty: intermediate
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0003]
  techniques: [T1547.001, T1546.012]
platforms: [windows]
tags: [registry, forensics, incident-response, autoruns, dfir, persistence, ifeo]
tools: [regedit, autoruns, regripper]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Windows Registry Autorun Forensics

## When to Use
- During triage of a potentially compromised Windows system to identify how malware survives reboots.
- After extracting the registry hives (SAM, SYSTEM, SOFTWARE, NTUSER.DAT) from a forensic disk image for offline analysis.

## Workflow

### Phase 1: Identifying Run / RunOnce Keys

```powershell
# Concept: Windows Registry Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"
Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
```

### Phase 2: Detecting IFEO (Image File Execution Options) Injection

```powershell
# Get-ChildItem -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options" | Select-Object Name | Where-Object { $_.Name -match "sethc.exe|utilman.exe" }
# ```

### Phase 3: Inspecting Services Registry Keys

```powershell
# Get-ChildItem -Path "HKLM:\SYSTEM\CurrentControlSet\Services" | Where-Object { (Get-ItemProperty $_.PSPath).ImagePath -match "C:\\Users\\|C:\\ProgramData\\" } | Select-Object Name, @{Name="ImagePath"; Expression={(Get-ItemProperty $_.PSPath).ImagePath}}
```

### Phase 4: Offline Analysis using RegRipper

```bash
# # rip.pl -r /mnt/evidence/Windows/System32/config/SOFTWARE -p run
rip.pl -r /mnt/evidence/Users/Bob/NTUSER.DAT -p userinit
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Extract Hives ] --> B{Parse Keys ]}
    B -->|Yes| C[Identify Anomalies ]
    B -->|No| D[Check Alternate ]
    C --> E[Extract Artifacts ]
```

## 🔵 Blue Team Detection & Defense
- **Sysinternals Autoruns**: **Registry Key Auditing (GPO)**: **Registry Activity Monitoring (Sysmon Event ID 12, 13, 14)**: Key Concepts
| Concept | Description |
|---------|-------------|
| Windows Registry Hives | |
| IFEO Backdoors | |

## References
- SANS: [Windows Registry Forensics](https://www.sans.org/posters/windows-forensic-analysis/)
- Microsoft Sysinternals: [Autoruns](https://docs.microsoft.com/en-us/sysinternals/downloads/autoruns)
