<div align="center">

# 🔥 CyberSkills Elite

### 191 Battle-Tested Skills to Turn Your AI Agent into a Red Team Co-Pilot

[![Skills](https://img.shields.io/badge/Skills-191-red?style=for-the-badge&logo=target&logoColor=white)](./skills)
[![AI Red Team](https://img.shields.io/badge/AI_Red_Team-25_Skills-purple?style=for-the-badge&logo=robot&logoColor=white)](./skills/ai-red-teaming)
[![PortSwigger](https://img.shields.io/badge/PortSwigger-31_Deep_Dives-orange?style=for-the-badge&logo=firefox&logoColor=white)](./skills/bug-hunting/deep-dive-labs)
[![Eval Score](https://img.shields.io/badge/Quality-191%2F191_Passing-brightgreen?style=for-the-badge&logo=checkmarx&logoColor=white)](./LEADERBOARD.md)
[![MITRE](https://img.shields.io/badge/MITRE_ATT%26CK-Mapped-yellow?style=for-the-badge&logo=shield&logoColor=white)](./mappings)
[![License](https://img.shields.io/badge/License-Apache_2.0-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./LICENSE)

*Bug Bounty • Pentesting • Red Team • AI Security • Incident Response • Cloud • AD Attacks*

**Works with:** Claude Code | Gemini CLI | Cursor | Windsurf | Codex CLI | GitHub Copilot | Any MCP Agent

---

[**⚡ Quick Start**](#-60-second-quick-start) · [**🎯 Why Us?**](#-why-were-different) · [**📂 Skills**](#-full-skill-catalog) · [**🔗 Attack Chains**](#-attack-chain-composer) · [**✅ Quality**](#-quality-assurance) · [**🤝 Contribute**](#-contributing)

</div>

---

## ⚡ 60-Second Quick Start

### Linux / macOS
```bash
# One-command install (auto-detects your AI agent)
curl -sS https://raw.githubusercontent.com/Ak-cybe/awesome-offensive-security-skills/main/install.sh | bash
```

### Windows (PowerShell)
```powershell
# Clone and install
git clone https://github.com/Ak-cybe/awesome-offensive-security-skills.git
Copy-Item -Recurse awesome-offensive-security-skills\skills\ $env:USERPROFILE\.gemini\skills\cyberskills-elite\
```

### Manual (any agent)
```bash
git clone https://github.com/Ak-cybe/awesome-offensive-security-skills.git

# Claude Code
cp -r awesome-offensive-security-skills/skills/ ./.claude/skills/

# Gemini CLI
cp -r awesome-offensive-security-skills/skills/ ~/.gemini/skills/cyberskills-elite/

# Any agent — skills use the universal SKILL.md standard
```

### Install by category (pick what you need)
```bash
./install.sh --category ai        # AI Red Teaming (25 skills)
./install.sh --category web       # Web App Security (28 skills)
./install.sh --category labs      # PortSwigger Labs (31 skills)
./install.sh --list               # See all categories
```

### Use (zero config)
```
# Just describe what you want. The agent auto-selects the right skill:

"Test this JWT for algorithm confusion attacks"
→ Loads: jwt-forgery-algorithm-confusion

"Perform Kerberoasting on the AD domain controller at 10.10.10.1"
→ Loads: active-directory-kerberoasting

"Test this chatbot for prompt injection bypasses"
→ Loads: llm-direct-prompt-injection

"Chain this SSRF into RCE on the cloud backend"
→ Loads: attack-chain-composer → ssrf + cloud-metadata + iam-exploitation
```

**Done.** No configuration. No plugins to enable. Just describe your task.

---

## 🎯 Why We're Different

> **We're not "another skill collection." We're the only offensive security-first collection built for AI agents.**

### Head-to-Head: CyberSkills Elite vs. The Competition

| Feature | **CyberSkills Elite** | VoltAgent (13K⭐) | Other Repos |
|---|:---:|:---:|:---:|
| **Total Skills** | **191** | ~5 security | ~50 mixed |
| **Offensive Security Depth** | ✅ Full kill chains | ❌ Checklists | ⚠️ Surface |
| **AI Red Teaming** | ✅ **25 dedicated** | ❌ Zero | ❌ Zero |
| **PortSwigger Lab Walkthroughs** | ✅ **31 deep dives** | ❌ Zero | ❌ Zero |
| **Working Payloads & Commands** | ✅ Every phase | ❌ None | ⚠️ Some |
| **Real CVE Case Studies** | ✅ Per skill | ❌ | ❌ |
| **🔴 Red + 🔵 Blue Team** | ✅ Every skill | ❌ | ❌ |
| **Decision Flowcharts** | ✅ Mermaid diagrams | ❌ | ❌ |
| **MITRE ATT&CK Mapping** | ✅ Full coverage | ❌ | ⚠️ Partial |
| **Attack Chain Composer** | ✅ **EXCLUSIVE** | ❌ | ❌ |
| **Quality Framework** | ✅ 10 automated checks | ❌ None | ❌ None |
| **Elite Chaining Strategy** | ✅ $50K report methodology | ❌ | ❌ |
| **Multi-Agent Compatible** | ✅ All platforms | ⚠️ Single | ⚠️ Single |

**VoltAgent wins for general development. We own offensive security.** They have ~5 security skills. We have 191, with 38x more coverage and capabilities they can't match.

### 🏆 What Makes Us #1 for Security

1. **🔗 Attack Chain Composer** — Not just vulnerability lists. A dedicated agent that chains skills into multi-step kill chains. Turn an SSRF into RCE. Turn XSS into account takeover. This is the **$500 vs $50,000 report** differentiator. [→ See Attack Chains](#-attack-chain-composer)

2. **🤖 AI Red Teaming (25 skills)** — The *only* collection with LLM jailbreaking, RAG poisoning, MCP exploitation, agent tool abuse, and adversarial ML skills. Nobody else covers this.

3. **🎓 PortSwigger Deep Dives (31 labs)** — Every lab with exact payloads, bypass techniques, and zero-day extensions. BSCP certification ready.

4. **🏆 Elite Hunter Methods** — Every skill includes the "Top 1%" chaining strategies used by hunters earning $50K+ per report.

5. **🔵 Dual Perspective** — Every offensive skill includes detection rules, SIEM queries, and remediation. Red + Blue in one file.

6. **📊 191/191 Quality Score** — Every skill passes 10 automated binary evaluations. Zero AI hallucination. [→ See Leaderboard](./LEADERBOARD.md)

7. **⚙️ Self-Improving** — Built-in auto-research framework that evaluates, mutates, and perfects skills autonomously.

---

## 🔗 Attack Chain Composer

> **Unique to CyberSkills Elite.** No other skill collection offers this.

The Attack Chain Composer takes a single vulnerability finding and maps it to multi-step attack paths for maximum impact:

```
You: "I found an open redirect on target.com"

Agent (using Attack Chain Composer):
┌─────────────────────────────────────────────┐
│ 🔗 Attack Chain: Open Redirect → ATO       │
│                                             │
│ Step 1: Craft redirect → OAuth callback     │
│   └→ Skill: open-redirect-exploitation      │
│                                             │
│ Step 2: Steal authorization code            │
│   └→ Skill: oauth-flow-exploitation         │
│                                             │
│ Step 3: Full account takeover               │
│                                             │
│ Impact: Low → Critical                      │
│ Estimated Bounty: $5,000 — $25,000          │
└─────────────────────────────────────────────┘
```

**Built-in chains include:**
- XSS → Session Theft → Account Takeover
- SSRF → Cloud Metadata → IAM → RCE
- SQL Injection → Data Dump → Network Pivot
- JWT Confusion → Admin Token → Full Takeover
- Kerberoasting → Lateral Movement → Domain Admin → Golden Ticket
- Prompt Injection → System Prompt Leak → SSRF → Data Exfiltration

[→ Full attack chain documentation](./tools/attack-chain-composer/SKILL.md)

---

## 📂 Full Skill Catalog

<table>
<tr><td>

### Overview — 191 Skills, 10 Domains

| Domain | Skills | Coverage |
|---|---|---|
| 🐛 **Bug Hunting** | 90 | Web vulns, API security, deep-dive labs, methodology |
| 🔓 **Penetration Testing** | 40 | Network, web app, cloud, AD, mobile, wireless |
| 🤖 **AI Red Teaming** | 25 | LLM attacks, ML security, agent exploitation |
| 🎯 **Red Teaming** | 21 | C2, evasion, persistence, priv esc, lateral movement |
| 🔍 **Incident Response** | 10 | Forensics, threat hunting, malware analysis |
| 🕵️ **OSINT** | 1 | Reconnaissance methodology |
| 💀 **Exploit Dev** | 1 | Binary exploitation |
| 🧬 **Malware Analysis** | 1 | Reverse engineering |
| 🔎 **Forensics** | 1 | Digital forensics |
| 📡 **Recon** | 1 | Attack surface mapping |
| | **191** | |

</td></tr>
</table>

---

### 🐛 Bug Hunting (90 Skills)

<details>
<summary><b>Web Vulnerabilities (28)</b> — IDOR, XSS, SSRF, SQLi, SSTI, XXE, CSRF, and more</summary>

| Skill | Difficulty | Key Techniques |
|---|---|---|
| [IDOR Vulnerability Hunting](./skills/bug-hunting/web-vulnerabilities/idor-vulnerability-hunting) | Intermediate | UUID prediction, parameter tampering, BOLA |
| [XSS — Reflected, Stored, DOM](./skills/bug-hunting/web-vulnerabilities/xss-reflected-stored-dom) | Intermediate | Polyglot payloads, WAF bypass, CSP evasion |
| [SSRF — Server-Side Request Forgery](./skills/bug-hunting/web-vulnerabilities/ssrf-server-side-request-forgery) | Advanced | Cloud metadata, DNS rebinding, protocol smuggling |
| [SQL Injection — Manual & Automated](./skills/bug-hunting/web-vulnerabilities/sqli-manual-and-automated) | Intermediate | Union, blind, time-based, SQLMap mastery |
| SSTI — Server-Side Template Injection | Advanced | Jinja2, Twig, Freemarker exploitation |
| XXE — XML External Entity Injection | Intermediate | OOB exfiltration, blind XXE |
| CSRF Token Bypass Techniques | Intermediate | Double submit, referer validation bypass |
| Race Condition Exploitation | Advanced | Time-of-check/time-of-use, limit bypass |
| File Upload Vulnerability Testing | Intermediate | Extension bypass, magic bytes, polyglots |
| Open Redirect & Header Injection | Beginner | OAuth token theft chaining |
| Deserialization Attacks | Expert | Java, PHP, .NET gadget chains |
| CORS Misconfiguration Exploitation | Intermediate | Origin reflection, null origin |
| WebSocket Security Testing | Advanced | CSWSH, hijacking, injection |
| Cache Poisoning Attacks | Advanced | Keyed/unkeyed headers, web cache deception |
| HTTP Request Smuggling | Expert | CL.TE, TE.CL, TE.TE variations |
| + 13 more specialized web vuln skills | | |

</details>

<details>
<summary><b>API Security (9)</b> — JWT, GraphQL, OAuth, BOLA, mass assignment</summary>

| Skill | Difficulty | Key Techniques |
|---|---|---|
| [JWT Forgery & Algorithm Confusion](./skills/bug-hunting/api-security/jwt-forgery-algorithm-confusion) | Advanced | RS256→HS256, none algorithm, key cracking |
| [API Authentication Bypass](./skills/bug-hunting/api-security/api-authentication-bypass) | Intermediate | Token manipulation, auth header abuse |
| [GraphQL Injection & Introspection](./skills/bug-hunting/api-security/graphql-injection-introspection) | Intermediate | Depth attacks, batching, field fuzzing |
| [GraphQL Batching Attacks](./skills/bug-hunting/api-security/graphql-batching-attacks) | Intermediate | Rate limit bypass via batched queries |
| [OAuth Flow Exploitation](./skills/bug-hunting/api-security/oauth-flow-exploitation) | Advanced | Code interception, PKCE bypass |
| [BOLA/BFLA Detection](./skills/bug-hunting/api-security/broken-object-level-authorization) | Intermediate | Horizontal/vertical access control |
| [API Mass Assignment](./skills/bug-hunting/api-security/api-mass-assignment-exploitation) | Intermediate | Hidden parameter injection |
| [API Rate Limit Bypass](./skills/bug-hunting/api-security/api-rate-limit-bypass-techniques) | Intermediate | Header rotation, IP rotation |
| [API Enumeration & Fuzzing](./skills/bug-hunting/api-security/api-enumeration-fuzzing-discovery) | Intermediate | Wordlist-based endpoint discovery |

</details>

<details>
<summary><b>PortSwigger Deep-Dive Labs (31)</b> — Every lab variant with exact payloads</summary>

Complete walkthroughs for every PortSwigger Web Security Academy category:

| Lab Category | Labs | Levels |
|---|---|---|
| Access Control | 13 labs | 🟢🟡🔴 |
| SQL Injection | All variants | 🟢🟡🔴 |
| XSS | Reflected, Stored, DOM | 🟢🟡🔴 |
| SSRF | Basic + Blind | 🟡🔴 |
| SSTI | All engines | 🟡🔴 |
| XXE | In-band + OOB | 🟢🟡 |
| Authentication | Multi-factor bypass | 🟢🟡🔴 |
| Business Logic | All scenarios | 🟡 |
| JWT Labs | None alg, confusion | 🟡🔴 |
| Host Header | Routing attacks | 🟡🔴 |
| WebSockets | CSWSH, injection | 🟡 |
| Web Cache Poisoning | Keyed/unkeyed | 🟡🔴 |
| API Testing | REST + GraphQL | 🟡🔴 |

Each deep-dive includes:
- ✅ Exact payloads (copy-paste ready)
- ✅ Zero-day extension techniques
- ✅ WAF bypass alternatives
- ✅ 🟢 Apprentice 🟡 Practitioner 🔴 Expert markers

</details>

<details>
<summary><b>Methodology (9)</b> — AI pair hunting, report writing, workflow automation</summary>

| Skill | Focus |
|---|---|
| AI Pair Hunting with Claude | Agent-assisted vulnerability discovery |
| Bug Bounty Workflow Funnel | End-to-end hunting process |
| AI Report Writing Guardrails | Hallucination-free report generation |
| Zero-Day Research Methodology | Novel vulnerability discovery |
| HackerOne Brain MCP | Platform integration |
| Kaido Proxy Integration | Burp alternative workflow |
| Remote Hunting Workflow | Cloud-based hunting setup |
| Session Search Tool | Multi-session reconnaissance |
| Claude Skills for Bug Bounty | Skill-powered hunting |

</details>

<details>
<summary><b>Other Bug Hunting Categories</b> — Deserialization, logic flaws, source code, recon</summary>

- **Deserialization (2)** — Java/PHP/Python gadget chains
- **Logic Flaws (2)** — Business logic bypass, payment manipulation
- **Source Code Analysis (1)** — Static analysis for vulns
- **Recon & Enumeration (5)** — Subdomain, JS analysis, cloud asset discovery
- **APIs (5)** — REST, SOAP, gRPC testing patterns

</details>

---

### 🔓 Penetration Testing (40 Skills)

<details>
<summary><b>Network (9)</b> — Nmap, AD attacks, SMB, DNS, MitM</summary>

| Skill | Difficulty | MITRE |
|---|---|---|
| Nmap Advanced Scanning | Beginner | T1046 |
| Active Directory Full Chain | Expert | T1558 |
| AD Kerberoasting | Advanced | T1558.003 |
| AD AS-REP Roasting | Advanced | T1558.004 |
| SMB/NetBIOS Exploitation | Intermediate | T1021.002 |
| DNS Zone Transfer & Poisoning | Intermediate | T1071.004 |
| LLMNR/NBT-NS Poisoning | Intermediate | T1557.001 |
| Pivoting & Tunneling | Advanced | T1572 |
| ARP Spoofing & MitM | Intermediate | T1557.002 |

</details>

<details>
<summary><b>Cloud (10)</b> — AWS, Azure, GCP, Kubernetes, Docker</summary>

| Skill | Difficulty |
|---|---|
| AWS Penetration Testing | Advanced |
| Azure Security Assessment | Advanced |
| GCP Security Testing | Advanced |
| Kubernetes Cluster Exploitation | Expert |
| Docker Container Escape | Advanced |
| Cloud IAM Exploitation | Advanced |
| S3 Bucket Misconfiguration | Intermediate |
| Serverless Function Exploitation | Advanced |
| Cloud Metadata Service Abuse | Intermediate |
| Multi-Cloud Attack Paths | Expert |

</details>

<details>
<summary><b>Active Directory (6)</b> — Full domain takeover chains</summary>

| Skill | Difficulty |
|---|---|
| AD Full Attack Chain | Expert |
| Kerberoasting | Advanced |
| AS-REP Roasting | Advanced |
| DCSync Attack | Expert |
| Golden/Silver Ticket | Expert |
| BloodHound Enumeration | Intermediate |

</details>

<details>
<summary><b>Web App, Mobile, Wireless, Infrastructure</b></summary>

- **Web Application (4)** — Burp methodology, CMS testing, WAF bypass
- **Mobile Security (2)** — Android/iOS app testing
- **Wireless & IoT (2)** — WiFi pentesting, IoT assessment
- **Infrastructure (4)** — Linux/Windows privesc, CI/CD exploitation
- **Network Security (3)** — Additional network attack vectors

</details>

---

### 🤖 AI Red Teaming (25 Skills) — **EXCLUSIVE**

> **No other skill collection covers AI security.** We have 25 dedicated skills across 5 categories.

<details>
<summary><b>Prompt Engineering & LLM Attacks (7)</b></summary>

| Skill | Difficulty | MITRE ATLAS |
|---|---|---|
| LLM Direct Prompt Injection | Intermediate | AML.T0051 |
| LLM Jailbreaking Personas | Advanced | AML.T0051 |
| System Prompt Extraction | Intermediate | AML.T0051 |
| Multi-Turn Manipulation | Advanced | AML.T0051 |
| Token Smuggling | Advanced | AML.T0051 |
| LLM Output Manipulation | Advanced | AML.T0051 |
| LLM Denial of Service | Intermediate | AML.T0034 |

</details>

<details>
<summary><b>Model Exploitation (8)</b></summary>

| Skill | Difficulty |
|---|---|
| Training Data Extraction | Expert |
| Model Inversion Attacks | Expert |
| Adversarial Input Generation | Advanced |
| Model Evasion Attacks | Advanced |
| Data Poisoning in ML Pipelines | Expert |
| Model Supply Chain Attacks | Expert |
| Embedding Space Manipulation | Expert |
| AI Data Poisoning & Model Skewing | Advanced |

</details>

<details>
<summary><b>Agent Security (2) + ML Security (2) + GenAI (1) + Supply Chain (1) + Others</b></summary>

| Skill | Focus |
|---|---|
| MCP Protocol Exploitation | Model Context Protocol attack vectors |
| AI Agent Tool Abuse | Function calling & tool manipulation |
| RAG Poisoning & Data Exfiltration | Retrieval-Augmented Generation attacks |
| Adversarial ML Attacks | Classical ML evasion |
| Deepfake Detection & Analysis | Synthetic media forensics |
| AI Supply Chain Analysis | Model provenance & integrity |

</details>

---

### 🎯 Red Teaming (21 Skills)

<details>
<summary><b>Full red team lifecycle: C2, initial access, evasion, persistence, lateral movement, priv esc</b></summary>

| Category | Skills | Highlights |
|---|---|---|
| **C2 Frameworks** | 2 | Cobalt Strike, Malleable C2 profiles |
| **Evasion** | 4 | AMSI bypass, AV/EDR evasion, custom shellcode, LOLBins |
| **Persistence** | 4 | WMI subscriptions, scheduled tasks, registry, DLL hijack |
| **Privilege Escalation** | 4 | Token impersonation, UAC bypass, kernel exploits |
| **Lateral Movement** | 2 | Pass-the-hash, WMI/SMB pivoting |
| **Credential Access** | 2 | LSASS dump, credential harvesting |
| **Initial Access** | 2 | Phishing campaigns, payload delivery |
| **Execution** | 1 | PowerShell/macro execution |

</details>

---

### 🔍 Incident Response & Forensics (10 Skills)

<details>
<summary><b>Forensics, threat hunting, malware analysis, threat intelligence</b></summary>

| Skill | Focus |
|---|---|
| Windows Event Log Analysis | Event ID correlation, lateral movement detection |
| Memory Forensics with Volatility | Process injection, rootkit detection |
| Disk Forensics & Recovery | File carving, timeline analysis |
| Network Traffic Analysis | Wireshark, Zeek, anomaly detection |
| Malware Triage & Analysis | Static + dynamic analysis |
| Incident Response Playbooks | Containment, eradication, recovery |
| Threat Hunting Methodology | Hypothesis-driven hunting |
| Threat Intelligence Integration | IOC enrichment, STIX/TAXII |
| YARA Rule Development | Pattern matching for malware |
| Cloud Forensics | AWS/Azure log analysis |

</details>

---

## 🏗️ Skill Architecture

Every skill follows a consistent structure and passes **10 automated quality checks**:

```
skill-name/
├── SKILL.md                          # Main skill file
│   ├── YAML Frontmatter
│   │   ├── name, description (aggressive trigger)
│   │   ├── difficulty: beginner|intermediate|advanced|expert
│   │   ├── mitre_attack: tactics + techniques
│   │   ├── tags, tools, platforms
│   │   └── version, author, license
│   ├── When to Use (trigger conditions)
│   ├── Prerequisites
│   ├── Workflow (Phase 1-N with real commands)
│   │   ├── Decision flowcharts (Mermaid)
│   │   └── Expected output examples
│   ├── 🏆 Elite Chaining Strategy (Top 1% methodology)
│   ├── 🔴 Red Team (offensive operations)
│   ├── 🔵 Blue Team (detection & defense)
│   ├── 🛡️ Remediation & Mitigation
│   ├── Key Concepts Table
│   ├── Output Format (report template)
│   ├── Real-World Bounty Examples
│   └── References (with URLs)
├── scripts/
│   └── process.py                    # Automation script
├── evals/
│   └── evals.json                    # Test assertions
└── references/
    └── standards.md                  # Additional docs
```

---

## 🔍 Skill Browser

Can't find what you need? Use the **Skill Browser** agent:

```
"Show me all AI red teaming skills"
→ Lists all 25 skills with descriptions

"Find a skill for JWT testing"
→ Returns jwt-forgery-algorithm-confusion and related

"What's your hardest skill?"
→ Lists all 34 expert-level skills

"Search for cloud exploitation"
→ Shows AWS, Azure, GCP, K8s, Docker skills
```

The Skill Browser searches across names, descriptions, tags, and categories. See [`tools/skill-browser/`](./tools/skill-browser/) for details.

---

## ✅ Quality Assurance

Every skill is validated with our **binary eval framework** — no subjective scoring, only pass/fail:

| Eval | What It Checks | Score |
|---|---|---|
| `yaml_frontmatter` | Has description, difficulty, tags in YAML | 191/191 ✅ |
| `no_ai_fluff` | Free of "Certainly!", "Delve into", etc. | 191/191 ✅ |
| `red_team_section` | Has 🔴 Red Team or Offensive section | 191/191 ✅ |
| `blue_team_section` | Has 🔵 Blue Team or Defensive section | 191/191 ✅ |
| `poc_payloads` | Includes concrete code blocks | 191/191 ✅ |
| `mitigation_remediation` | Has remediation/mitigation strategy | 191/191 ✅ |
| `elite_hunter_methodology` | Includes elite chaining / OPSEC advice | 191/191 ✅ |
| `step_by_step_repro` | Has step-by-step reproduction | 191/191 ✅ |
| `cvss_severity` | Mentions CVSS or severity level | 191/191 ✅ |
| `references` | Ends with References + URLs | 191/191 ✅ |

**[→ View Full Leaderboard](./LEADERBOARD.md)**

### Run evaluations yourself:
```bash
# Single skill
python auto_research/evaluator.py skills/bug-hunting/api-security/jwt-forgery-algorithm-confusion/SKILL.md

# All skills (with auto-fix)
python auto_research_mutator.py
```

### Self-Improvement Loop

The repo includes a complete **auto-research framework** that autonomously improves skills:

```
Select Skill → Evaluate (10 checks) → Mutate (fix failures) → Re-evaluate → Repeat (max 5x)
```

See [`auto_research/`](./auto_research) for the eval criteria, evaluator, and optimization loop.

---

## 🗺️ MITRE ATT&CK Coverage

| Framework | Coverage |
|---|---|
| **MITRE ATT&CK** | 14 tactics, 85+ techniques |
| **MITRE ATLAS** | AI/ML-specific mappings for all 25 AI red teaming skills |
| **OWASP Top 10** | Full coverage across web vulnerability skills |
| **OWASP API Top 10** | Covered in API security skills |

Full navigator layer available in [`mappings/`](./mappings).

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**High-priority areas:**
- 🤖 AI Red Teaming (new attack vectors emerge weekly)
- 🔓 Cloud Security (multi-cloud attack paths)
- 🧬 Exploit Development (modern binary exploitation)
- 📡 IoT/Hardware Security
- 🌍 Translations

**Quality bar:** All contributions must pass the 10-point binary eval. Run `python auto_research/evaluator.py your-skill/SKILL.md` before submitting.

---

## ⚠️ Legal Disclaimer

This project is intended for **authorized security testing, education, and research only**.

- All skills assume **explicit written authorization** to test target systems
- Unauthorized access to computer systems is **illegal** under CFAA, CMA, and equivalent laws
- Always follow bug bounty program rules, scope definitions, and rules of engagement
- The authors accept **no liability** for misuse of these materials

---

## 📄 License

Apache License 2.0 — see [LICENSE](./LICENSE) for details.

---

<div align="center">

**Built for the offensive security community by hunters, for hunters.**

**191 skills · 10 domains · 25 AI red team skills · 31 PortSwigger labs · 10-point quality framework**

⭐ **Star this repo if it makes your security work better** ⭐

[Report Bug](https://github.com/Ak-cybe/awesome-offensive-security-skills/issues) · [Request Skill](https://github.com/Ak-cybe/awesome-offensive-security-skills/issues) · [Contributing](./CONTRIBUTING.md)

</div>
