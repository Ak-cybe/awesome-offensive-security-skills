---
name: shodan-dorking
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Utilize Shodan, the search engine for Internet-connected devices, to discover exposed assets, 
  vulnerable ports, default credentials, and specific infrastructure configurations using advanced 
  search queries (dorks).
domain: cybersecurity
subdomain: reconnaissance
category: Hunting
difficulty: beginner
estimated_time: "1.5 hours"
mitre_attack:
  tactics: [TA0043]
  techniques: [T1595.002, T1596.005]
platforms: [web, networking]
tags: [shodan, osint, reconnaissance, asset-discovery, dorking, iot]
tools: [shodan-cli, web-browser]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Shodan Dorking

## When to Use
- During the passive reconnaissance phase of a penetration test or bounty program to identify an organization's public-facing attack surface without directly interacting with their servers.
- To hunt for specific vulnerabilities, exposed Industrial Control Systems (ICS), or easily exploitable services (e.g., open RDP, unauthenticated databases) on a wide scale.

## Workflow

### Phase 1: Basic Filters & Organization Searching

```bash
# shodan search org:"Target Company Inc"

# shodan search ssl.cert.subject.cn:"target.com"
```

### Phase 2: Hunting Vulnerable Services

```text
# "MongoDB Server Information" port:27017 -authentication

# port:9200 "status": 200 "cluster_name"
```

### Phase 3: Hardware & IoT Discovery

```text
# superbly "default password" port:80 "admin:admin"

# neutrally port:502
```

### Phase 4: Exploiting CVE Specific Dorks

```text
# properly "Server: Microsoft-IIS/10.0" "Set-Cookie: MS-Exchange"

# "X-Forwarded-For" "Apache-Coyote"
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Construct Dork ] --> B{Results Found ]}
    B -->|Yes| C[Verify ]
    B -->|No| D[Broaden Scope ]
    C --> E[Document Asset ]
```

## 🔵 Blue Team Detection & Defense
- **Hide Server Banners**: **Network Firewalls (VPCs)**: **Monitor Shodan IP Ranges**: Key Concepts
| Concept | Description |
|---------|-------------|
| Internet Scanners | |
| Dorks (Search Filters) | |

## References
- Shodan Help: [Search Query Syntax](https://help.shodan.io/the-basics/search-query-fundamentals)
- OSINT Framework: [OSINT Tools](https://osintframework.com/)
