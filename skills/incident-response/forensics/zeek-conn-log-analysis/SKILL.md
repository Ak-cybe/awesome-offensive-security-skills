---
name: zeek-conn-log-analysis
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Analyze Zeek (formerly Bro) `conn.log` files to hunt for malicious network behaviors, 
  including C2 beaconing, long-lived anomalous connections, and data exfiltration patterns.
domain: cybersecurity
subdomain: incident-response
category: Forensics
difficulty: intermediate
estimated_time: "2 hours"
mitre_attack:
  tactics: [TA0011, TA0010]
  techniques: [T1071, T1043]
platforms: [network, linux]
tags: [zeek, network-forensics, threat-hunting, dfir, c2-beaconing, packet-analysis]
tools: [zeek, awk, zeek-cut, jq]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Zeek conn.log Analysis

## When to Use
- During network forensics investigations or active threat hunting to identify compromised hosts communicating with Command and Control (C2) infrastructure.
- To detect unusual network baseline deviations without relying entirely on deep packet inspection or payload signatures.

## Workflow

### Phase 1: Understanding conn.log Structure

```bash
# head conn.log | zeek-cut -c ts uid id.orig_h id.orig_p id.resp_h id.resp_p proto service duration orig_bytes resp_bytes conn_state
```

### Phase 2: Hunting for C2 Beaconing (Frequency Analysis)

```bash
# cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p duration | \
awk '{print $1, $2, $3}' | sort | uniq -c | sort -nr | head -n 20
```

### Phase 3: Identifying Long-Connections (Data Exfil / Interactive Shells)

```bash
# cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p duration orig_bytes resp_bytes | \
awk '$4 > 3600 {print $0}' | sort -nrk 4
```

### Phase 4: Detecting Odd Port-Service Mismatches

```bash
# cat conn.log | zeek-cut id.resp_p service | grep -E '^443\s+http$' | less

# cat conn.log | zeek-cut id.resp_p service | grep -E '^80\s+ssl$' | less
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Parse conn.log ] --> B{Anomalies Found ]}
    B -->|Yes| C[Correlate Logs ]
    B -->|No| D[Tune Heuristics ]
    C --> E[Isolate Host ]
```

## 🔵 Blue Team Detection & Defense
- **Automate Beacon Tracking (RITA / Zeek Detect)**: **Threat Intelligence Feeds**: **Baseline Internal Traffic**: Key Concepts
| Concept | Description |
|---------|-------------|
| Zeek Logs | |
| Beacon Analysis | |

## References
- Zeek Documentation: [Logging Framework](https://docs.zeek.org/en/current/frameworks/logging.html)
- Active Countermeasures: [RITA (Real Intelligence Threat Analytics)](https://github.com/activecm/rita)
