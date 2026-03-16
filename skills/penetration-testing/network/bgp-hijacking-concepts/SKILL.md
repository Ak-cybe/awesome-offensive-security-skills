---
name: bgp-hijacking-concepts
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Understand the mechanics of Border Gateway Protocol (BGP) Hijacking, where an attacker creatively 
  manipulates Internet routing tables to intercept, monitor, or drop massive volumes of network 
  traffic destined for legitimate Autonomous Systems (AS).
domain: cybersecurity
subdomain: penetration-testing
category: Network
difficulty: expert
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0006, TA0040]
  techniques: [T1095, T1650] # Conceptual mapping for generic network intercepts
platforms: [network, hardware]
tags: [network, bgp, physical-layer, infrastructure, penetration-testing, spoofing]
tools: [quagga, bgpstream]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Border Gateway Protocol (BGP) Hijacking

## When to Use
- When conducting highly advanced Red Team engagements involving physical infrastructure attacks, ISP-level threat simulation, or Nation-State adversary emulation.
- To demonstrate how an attacker can maliciously reroute entire blocks of IP addresses (subnets) globally by advertising false routing updates to internet backbone routers.
- *Note: True BGP hijacking requires access to a peered BGP router. This skill primarily focuses on the conceptual understanding, simulation, and defensive modeling of the attack.*

## Workflow

### Phase 1: Understanding BGP (The Concept)

```text
# Concept: The Internet is essentially a network of interconnecting networks (Autonomous Systems or AS).
# Border Gateway Protocol (BGP) is the "postal service" of the internet. It dynamically figures out 
# the most efficient path for data to travel from AS1 to AS99.

# Vulnerability: BGP was designed in the 1980s ```

### Phase 2: The Attack (Route Advertisement Spoofing)

```text
# Concept: An attacker controls a BGP router (e.g., AS666). They want to steal traffic destined 
# for a target bank (AS777) which owns the IP block 104.20.0.0/16.

# Step 1: The False Broadcast
# The attacker configures their router to announce to the world: "I am the best, quickest path to 104.20.0.0/24!"
# (Notice they announce a /24, which is a *more specific* route than the legitimate /16).

# Step 2: The Propagation
# BGP routers Step 3: The Intercept Global traffic ```

### Phase 3: Exploitation Techniques (What happens to the traffic?)

```text
# Strategy 1: The Blackhole (Denial of Service)
# The attacker Strategy 2: Man-in-the-Middle (Traffic Inspection)
# Strategy 3: DNS Hijacking ```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Attacker gains access ] --> B[Attacker ]
    B --> C{Does }
    C -->|Yes| D[Traffic ]
    C -->|No| E[Spoofed ]
    D --> F[Execute ]
```

## 🔵 Blue Team Detection & Defense
- **RPKI (Resource Public Key Infrastructure)**: Implement **BGP Route Monitoring**: Utilize **Prefix Filtering**: ISPS Key Concepts
| Concept | Description |
|---------|-------------|
| BGP | |
| AS (Autonomous System) | |
| RPKI | |

## References
- Cloudflare: [What is BGP Hijacking?](https://www.cloudflare.com/learning/security/glossary/bgp-hijacking/)
- MANRS (Mutually Agreed Norms for Routing Security): [https://www.manrs.org/](https://www.manrs.org/)
- Internet Society: [BGP Security](https://www.internetsociety.org/issues/routing-security/)
