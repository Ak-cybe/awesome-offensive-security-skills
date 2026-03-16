<div align="center">

# 🔥 CyberSkills Elite

### The Ultimate Cybersecurity Agent Skills Collection

**155+ battle-tested offensive security skills for AI coding agents**

[![Skills](https://img.shields.io/badge/Skills-155+-red?style=for-the-badge&logo=target&logoColor=white)](./skills)
[![Categories](https://img.shields.io/badge/Categories-8-blue?style=for-the-badge&logo=folder&logoColor=white)](./skills)
[![AI Red Team](https://img.shields.io/badge/AI_Red_Team-30_Skills-purple?style=for-the-badge&logo=robot&logoColor=white)](./skills/ai-red-teaming)
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE_ATT%26CK-Mapped-orange?style=for-the-badge&logo=shield&logoColor=white)](./mappings)
[![License](https://img.shields.io/badge/License-Apache_2.0-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./LICENSE)

*Bug Hunting • Penetration Testing • Red Teaming • AI Red Teaming*

**Compatible with: Claude Code | GitHub Copilot | Cursor | Gemini CLI | Codex CLI**

---

[**Quick Start**](#-quick-start) • [**Skill Catalog**](#-skill-catalog) • [**Why CyberSkills Elite?**](#-why-cyberskills-elite) • [**Contributing**](#-contributing)

</div>

---

## ⚡ Quick Start

### For Claude Code
```bash
# Clone the repository
git clone https://github.com/cyberskills-elite/cybersecurity-agent-skills.git

# Install as skills directory
cd cybersecurity-agent-skills
# Skills are automatically detected when placed in your project
```

### For Gemini CLI / Cursor / Any Agent
```bash
# Point your agent to the skills directory
# Each skill follows the agentskills.io standard format
```

### Use a Skill
```
# Simply describe what you want to do. The AI agent will automatically 
# select and use the relevant skill:

"Test this application for IDOR vulnerabilities"
"Perform a Kerberoasting attack on the Active Directory domain"  
"Test this chatbot for prompt injection vulnerabilities"
"Set up a Cobalt Strike beacon with malleable C2 profile"
```

---

## 🏆 Why CyberSkills Elite?

| Feature | CyberSkills Elite | Anthropic (734 skills) | SecOps CLI | VoltAgent |
|---------|:-----------------:|:---------------------:|:----------:|:---------:|
| **Offensive Security Depth** | ✅ 155+ deep skills | ❌ 24 Red Team, 23 Pentest | ⚠️ ~50 skills | ❌ Checklists only |
| **AI Red Teaming** | ✅ **30 unique skills** | ❌ None | ❌ None | ❌ None |
| **Working Commands** | ✅ Every phase | ⚠️ Many broken/empty | ✅ | ❌ No commands |
| **Real CVE Case Studies** | ✅ Per skill | ❌ | ❌ | ❌ |
| **Blue Team Detection** | ✅ Every skill | ❌ | ❌ | ❌ |
| **Decision Flowcharts** | ✅ Mermaid diagrams | ❌ | ❌ | ❌ |
| **Automation Scripts** | ✅ Python/Bash | ❌ | ⚠️ Some | ❌ |
| **MITRE ATT&CK Mapping** | ✅ Full mapping | ⚠️ Partial | ❌ | ❌ |
| **Difficulty Levels** | ✅ Beginner → Expert | ❌ | ❌ | ❌ |
| **Report Templates** | ✅ Professional | ❌ | ❌ | ❌ |
| **Multi-Agent Compatible** | ✅ All major agents | ⚠️ Claude only | ⚠️ Claude only | ⚠️ Claude only |

### 🎯 Our Unique Differentiators

1. **🤖 AI Red Teaming** — The only collection with dedicated LLM/ML/Agent security skills (30+)
2. **🔗 Attack Chain Playbooks** — Multi-skill sequences that mirror real-world kill chains
3. **🔀 Decision Flowcharts** — Mermaid diagrams for dynamic decision-making during assessments
4. **📋 Real CVE Case Studies** — Every skill references actual vulnerabilities with analysis
5. **🔵 Blue Team Detection** — Every attack skill includes defensive counterpart
6. **📊 Difficulty Progression** — Structured learning path from Beginner to Expert
7. **⚙️ Working Automation** — Python/Bash scripts that actually run (not placeholders)
8. **📝 Professional Reports** — Copy-paste-ready report templates for every finding type
9. **🔧 Tool Chaining** — Workflows showing how tools connect (Nmap → Nikto → SQLMap → Cobalt Strike)
10. **🌐 Multi-Platform** — Works with Claude Code, Copilot, Cursor, Gemini CLI, and more

---

## 📂 Skill Catalog

### 🐛 Bug Hunting (32 Skills)

<details>
<summary><b>Web Vulnerabilities (15)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| [IDOR Vulnerability Hunting](./skills/bug-hunting/web-vulnerabilities/idor-vulnerability-hunting) | Intermediate | T1530 |
| [XSS — Reflected, Stored, DOM](./skills/bug-hunting/web-vulnerabilities/xss-reflected-stored-dom) | Intermediate | T1189, T1059.007 |
| [SSRF — Server-Side Request Forgery](./skills/bug-hunting/web-vulnerabilities/ssrf-server-side-request-forgery) | Advanced | T1090, T1552.005 |
| [SQL Injection — Manual & Automated](./skills/bug-hunting/web-vulnerabilities/sqli-manual-and-automated) | Intermediate | T1190 |
| CSRF Token Bypass Techniques | Intermediate | T1185 |
| Race Condition Exploitation | Advanced | T1499.003 |
| File Upload Vulnerability Testing | Intermediate | T1608 |
| Template Injection (SSTI) | Advanced | T1059 |
| XXE — XML External Entity Injection | Intermediate | T1059 |
| Open Redirect & Header Injection | Beginner | T1036 |
| Deserialization Attacks | Expert | T1059 |
| CORS Misconfiguration Exploitation | Intermediate | T1557 |
| WebSocket Security Testing | Advanced | T1071 |
| Cache Poisoning Attacks | Advanced | T1557 |
| HTTP Request Smuggling | Expert | T1071 |

</details>

<details>
<summary><b>API Security (8)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| [API Authentication Bypass](./skills/bug-hunting/api-security/api-authentication-bypass) | Intermediate | T1078, T1550 |
| GraphQL Vulnerability Hunting | Intermediate | T1190 |
| REST API Mass Assignment | Intermediate | T1190 |
| API Rate Limiting & Business Logic | Intermediate | T1499 |
| BOLA/BFLA Detection | Intermediate | T1530 |
| API Versioning Exploitation | Beginner | T1190 |
| gRPC Security Testing | Advanced | T1190 |
| Webhook Security Assessment | Intermediate | T1071 |

</details>

<details>
<summary><b>Recon & Enumeration (5)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| [Web Application Recon & Enumeration](./skills/bug-hunting/recon-enumeration/web-application-recon-and-enumeration) | Beginner | T1595, T1592 |
| Bug Bounty Automation Pipeline | Advanced | T1595 |
| JavaScript Analysis & Secret Extraction | Intermediate | T1552 |
| GitHub Dorking & Secret Scanning | Beginner | T1552.004 |
| Cloud Asset Discovery & Enumeration | Intermediate | T1580 |

</details>

<details>
<summary><b>Methodology (4)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| Bug Bounty Report Writing | Beginner | — |
| CVSS Scoring & Severity Assessment | Beginner | — |
| Vulnerability Disclosure Best Practices | Beginner | — |
| Attack Surface Mapping Methodology | Intermediate | T1595 |

</details>

### 🔓 Penetration Testing (38 Skills)

<details>
<summary><b>Network (12)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| [Nmap Advanced Network Scanning](./skills/penetration-testing/network/nmap-advanced-network-scanning) | Beginner | T1046, T1595 |
| [Active Directory Full Attack Chain](./skills/penetration-testing/network/active-directory-full-attack-chain) | Expert | T1558, T1003 |
| SMB/NetBIOS Exploitation | Intermediate | T1021.002 |
| SNMP Enumeration & Exploitation | Intermediate | T1602 |
| DNS Zone Transfer & Poisoning | Intermediate | T1071.004 |
| LLMNR/NBT-NS Poisoning (Responder) | Intermediate | T1557.001 |
| Pivoting & Network Tunneling | Advanced | T1572 |
| VPN Security Assessment | Advanced | T1133 |
| ARP Spoofing & MitM Attacks | Intermediate | T1557.002 |
| IPv6 Attack Techniques | Advanced | T1557 |
| SSH Penetration Testing | Intermediate | T1021.004 |
| RDP Security Testing | Intermediate | T1021.001 |

</details>

<details>
<summary><b>Web Application (10)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| Burp Suite Advanced Methodology | Intermediate | T1190 |
| OWASP Testing Guide Execution | Intermediate | T1190 |
| WordPress Penetration Testing | Intermediate | T1190 |
| CMS Security Assessment | Intermediate | T1190 |
| Web Shell Deployment & Management | Advanced | T1505.003 |
| WAF Bypass Techniques | Advanced | T1190 |
| Authentication Mechanism Testing | Intermediate | T1078 |
| Session Management Testing | Intermediate | T1539 |
| Business Logic Testing | Intermediate | T1190 |
| File Inclusion (LFI/RFI) Exploitation | Intermediate | T1190 |

</details>

<details>
<summary><b>Infrastructure (10)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| Linux Privilege Escalation | Intermediate | T1068 |
| Windows Privilege Escalation | Intermediate | T1068 |
| Docker Container Escape | Advanced | T1610 |
| Kubernetes Cluster Exploitation | Expert | T1609 |
| AWS Cloud Penetration Testing | Advanced | T1580 |
| Azure & GCP Cloud Pentesting | Advanced | T1580 |
| CI/CD Pipeline Exploitation | Advanced | T1195 |
| Database Penetration Testing | Intermediate | T1190 |
| Email Server Exploitation | Intermediate | T1114 |
| Print Server & Printer Hacking | Intermediate | T1200 |

</details>

<details>
<summary><b>Wireless & IoT (4)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| WiFi Penetration Testing | Intermediate | T1557 |
| Bluetooth & BLE Security | Advanced | T1020 |
| IoT Device Security Assessment | Advanced | T1200 |
| RFID/NFC Exploitation | Expert | T1200 |

</details>

### 🎯 Red Teaming (35 Skills)

<details>
<summary><b>C2 Frameworks (6)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| [Cobalt Strike Beacon Operations](./skills/red-teaming/c2-frameworks/cobalt-strike-beacon-operations) | Expert | T1071, T1055 |
| Sliver C2 Implant Operations | Advanced | T1071 |
| Havoc C2 Demon Operations | Advanced | T1071 |
| Mythic C2 Framework Usage | Advanced | T1071 |
| Custom C2 Channel Development | Expert | T1071 |
| C2 Infrastructure Multi-Layer Setup | Expert | T1090 |

</details>

<details>
<summary><b>Initial Access (6)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| [Phishing & Social Engineering](./skills/red-teaming/initial-access/phishing-and-social-engineering-campaigns) | Intermediate | T1566 |
| Spearphishing Attachment Delivery | Intermediate | T1566.001 |
| Drive-by Compromise Setup | Advanced | T1189 |
| Supply Chain Attack Simulation | Expert | T1195 |
| Physical Social Engineering | Advanced | T1200 |
| Watering Hole Attack Planning | Advanced | T1189 |

</details>

<details>
<summary><b>Post-Exploitation (8)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| Data Exfiltration Techniques | Advanced | T1048 |
| Windows Persistence Mechanisms | Advanced | T1547 |
| Linux Persistence Mechanisms | Advanced | T1053 |
| Process Injection Techniques | Expert | T1055 |
| Memory Forensics Evasion | Expert | T1055 |
| Token Manipulation & Impersonation | Advanced | T1134 |
| Internal Reconnaissance Automation | Intermediate | T1087 |
| Situational Awareness Gathering | Intermediate | T1082 |

</details>

<details>
<summary><b>Evasion (8)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| AV/EDR Evasion Techniques | Expert | T1027 |
| AMSI Bypass Methods | Advanced | T1562.001 |
| Custom Shellcode Development | Expert | T1059 |
| Payload Obfuscation & Encoding | Advanced | T1027 |
| Living-off-the-Land (LOLBins) | Intermediate | T1218 |
| AppLocker & WDAC Bypass | Advanced | T1218 |
| Network Traffic Obfuscation | Advanced | T1573 |
| Log Evasion & Anti-Forensics | Advanced | T1070 |

</details>

<details>
<summary><b>Operations (7)</b></summary>

| Skill | Difficulty | MITRE |
|-------|-----------|-------|
| Red Team Planning & Scoping | Intermediate | — |
| OPSEC Principles & Practices | Advanced | T1480 |
| Threat Actor Emulation (APT) | Expert | — |
| Purple Team Collaboration | Intermediate | — |
| Red Team Report Writing | Intermediate | — |
| Attack Playbook Development | Advanced | — |
| Deconfliction & Safety Procedures | Intermediate | — |

</details>

### 🤖 AI Red Teaming (30 Skills) — **EXCLUSIVE**

<details>
<summary><b>LLM Attacks (10)</b></summary>

| Skill | Difficulty | MITRE ATLAS |
|-------|-----------|-------------|
| [LLM Direct Prompt Injection](./skills/ai-red-teaming/llm-attacks/llm-direct-prompt-injection) | Intermediate | AML.T0051 |
| LLM Indirect Prompt Injection | Advanced | AML.T0051.001 |
| System Prompt Extraction | Intermediate | AML.T0051 |
| LLM Jailbreaking Techniques | Intermediate | AML.T0051 |
| Multi-Turn Manipulation Attacks | Advanced | AML.T0051 |
| LLM Output Manipulation | Advanced | AML.T0051 |
| Training Data Extraction | Expert | AML.T0024 |
| Model Inversion Attacks | Expert | AML.T0024 |
| Token Smuggling & Encoding Bypass | Advanced | AML.T0051 |
| LLM Denial of Service | Intermediate | AML.T0034 |

</details>

<details>
<summary><b>ML Security (6)</b></summary>

| Skill | Difficulty | MITRE ATLAS |
|-------|-----------|-------------|
| [RAG Poisoning & Data Exfiltration](./skills/ai-red-teaming/ml-security/rag-poisoning-and-data-exfiltration) | Advanced | AML.T0051.001 |
| Adversarial Input Generation | Advanced | AML.T0043 |
| Model Evasion Attacks | Advanced | AML.T0015 |
| Data Poisoning in ML Pipelines | Expert | AML.T0020 |
| Model Supply Chain Attacks | Expert | AML.T0010 |
| Embedding Space Manipulation | Expert | AML.T0043 |

</details>

<details>
<summary><b>Agent Security (8)</b></summary>

| Skill | Difficulty | MITRE ATLAS |
|-------|-----------|-------------|
| [MCP Protocol Exploitation](./skills/ai-red-teaming/agent-security/mcp-protocol-exploitation) | Advanced | AML.T0051 |
| AI Agent Tool Abuse | Advanced | AML.T0051 |
| Function Calling Exploitation | Intermediate | AML.T0051 |
| Multi-Agent System Attacks | Expert | AML.T0051 |
| AutoGPT/CrewAI Security Testing | Advanced | AML.T0051 |
| AI Plugin Vulnerability Testing | Intermediate | AML.T0051 |
| AI Workflow Manipulation | Advanced | AML.T0051 |
| Custom GPT/Gem Security Assessment | Intermediate | AML.T0051 |

</details>

<details>
<summary><b>GenAI Threats (4)</b></summary>

| Skill | Difficulty | MITRE ATLAS |
|-------|-----------|-------------|
| Deepfake Detection & Analysis | Advanced | AML.T0048 |
| AI-Generated Phishing Analysis | Intermediate | AML.T0048 |
| Synthetic Media Forensics | Expert | AML.T0048 |
| AI Content Authentication | Intermediate | AML.T0048 |

</details>

<details>
<summary><b>Methodology (2)</b></summary>

| Skill | Difficulty |
|-------|-----------|
| AI Red Team Planning & Scoping | Intermediate |
| AI Security Assessment Reporting | Intermediate |

</details>

### 🧨 Bonus Categories (20 Skills)

<details>
<summary><b>Exploit Development (5) • OSINT (5) • Forensics/IR (5) • Malware Analysis (5)</b></summary>

#### Exploit Development
- Buffer Overflow (Stack) | Expert
- Return-Oriented Programming (ROP) | Expert
- Heap Exploitation Techniques | Expert
- Shellcode Development | Expert
- Exploit Weaponization | Expert

#### OSINT & Reconnaissance
- Open Source Intelligence Methodology | Beginner
- Social Media Investigation | Intermediate
- Dark Web Intelligence Gathering | Advanced
- Geolocation Intelligence (GEOINT) | Intermediate
- Corporate Intelligence Gathering | Intermediate

#### Forensics & Incident Response
- Memory Forensics with Volatility | Advanced
- Disk Forensics & Data Recovery | Advanced
- Network Traffic Analysis | Intermediate
- Malware Triage & Initial Analysis | Intermediate
- Incident Response Playbook Execution | Intermediate

#### Malware Analysis
- Static Malware Analysis | Intermediate
- Dynamic Malware Analysis (Sandboxing) | Advanced
- Reverse Engineering with Ghidra | Expert
- Malware Unpacking & Deobfuscation | Expert
- YARA Rule Development | Intermediate

</details>

---

## 🏗️ Skill Format

Every skill follows our enhanced format with **10 unique sections** that no competitor offers:

```
📄 SKILL.md
├── 📋 YAML Frontmatter
│   ├── name, description, domain, subdomain
│   ├── difficulty (Beginner → Expert)
│   ├── estimated_time
│   ├── mitre_attack (tactics, techniques)
│   ├── cve_references
│   ├── owasp_category
│   ├── platforms, tools, tags
│   └── version, author, license
├── 📖 Workflow (Multi-phase with commands)
│   ├── Phase 1-N with real commands
│   ├── Decision points (🔀 flowcharts)
│   └── Expected output examples
├── 🔵 Blue Team Detection
├── 📊 Real-World Case Studies (CVEs)
├── 📚 Key Concepts Table
├── 🔧 Tools & Systems Table
├── 💼 Common Scenarios
├── 📝 Professional Report Template
├── 🔍 Troubleshooting Guide
└── 📖 References
```

---

## 🗺️ MITRE ATT&CK Coverage

All skills are mapped to the MITRE ATT&CK framework (and MITRE ATLAS for AI skills):

- **14 Tactics** covered across all skills
- **85+ Techniques** mapped
- **AI-specific**: MITRE ATLAS mappings for all AI Red Teaming skills
- Full navigator layer available in `mappings/`

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Priority areas:**
- New skills (especially in AI Red Teaming and Exploit Development)
- Real-world case study additions
- Tool script contributions
- Translation to other languages

---

## ⚠️ Disclaimer

This project is intended for **authorized security testing and educational purposes only**. All skills assume you have **explicit written permission** to test the target systems. Unauthorized access to computer systems is illegal.

The authors are not responsible for misuse of these skills. Always follow:
- Applicable laws and regulations
- Your organization's security policies
- Bug bounty program rules and scope
- Penetration testing rules of engagement

---

## 📄 License

This project is licensed under the Apache License 2.0 — see [LICENSE](./LICENSE) for details.

---

<div align="center">

**Built with 💀 for the offensive security community**

⭐ Star this repo if it helps your security work ⭐

</div>
