# Contributing to CyberSkills Elite

Thank you for your interest in contributing! We welcome contributions from the cybersecurity community.

---

## 🏆 Contribution Bounty Program

We reward high-quality skill contributions:

| Contribution Type | Reward | Requirements |
|---|---|---|
| **AI Red Teaming skill** | $100 | Passes all 10 evals, novel attack vector |
| **Standard skill** | $50 | Passes all 10 evals, includes CVE case study |
| **Bug fix / improvement** | $25 | Measurable quality improvement to existing skill |
| **Translation** | $25 | Complete translation of 10+ skills |

All rewards are paid via GitHub Sponsors or PayPal. To claim, open an issue with the `bounty` label after your PR is merged.

---

## How to Contribute

### Adding New Skills

1. **Fork** the repository
2. **Create a branch**: `git checkout -b add-skill/new-skill-name`
3. **Create the skill directory** in the appropriate category:
   ```
   skills/<domain>/<subcategory>/skill-name/
   ├── SKILL.md          # Required — main skill file
   ├── scripts/          # Optional — automation scripts
   ├── evals/
   │   └── evals.json    # Optional — test cases
   └── references/       # Optional — additional docs
   ```
4. **Write SKILL.md** following the format below
5. **Run validation**: 
   ```bash
   python auto_research/evaluator.py skills/<your-skill>/SKILL.md
   ```
6. **Ensure all 10 checks pass** (see Quality Requirements below)
7. **Submit a Pull Request** with a description of the skill and its use case

### Where to Add Your Skill

| If your skill is about... | Add it to... |
|---|---|
| Web vulnerabilities (XSS, SQLi, SSRF, etc.) | `skills/bug-hunting/web-vulnerabilities/` |
| API security (JWT, GraphQL, OAuth, etc.) | `skills/bug-hunting/api-security/` |
| Bug bounty methodology | `skills/bug-hunting/methodology/` |
| AI/LLM attacks | `skills/ai-red-teaming/` |
| Network pentesting | `skills/penetration-testing/network/` |
| Active Directory | `skills/penetration-testing/active-directory/` |
| Cloud security | `skills/penetration-testing/cloud-security/` |
| Red team operations | `skills/red-teaming/` |
| Incident response | `skills/incident-response/` |
| Other | Open an issue first to discuss placement |

---

## Skill Quality Requirements (10-Point Eval)

Every skill **MUST** pass all 10 automated evaluations:

| # | Check | Requirement |
|---|---|---|
| 1 | `yaml_frontmatter` | Complete YAML header with name, description (>20 chars), difficulty, tags |
| 2 | `no_ai_fluff` | Zero instances of "Certainly!", "Delve into", "I'd be happy to", etc. |
| 3 | `red_team_section` | 🔴 Red Team or Offensive operations section |
| 4 | `blue_team_section` | 🔵 Blue Team or Defensive detection section |
| 5 | `poc_payloads` | Concrete code blocks with real, tested commands |
| 6 | `mitigation_remediation` | Specific remediation/mitigation strategies |
| 7 | `elite_hunter_methodology` | Elite chaining strategy or OPSEC advice section |
| 8 | `step_by_step_repro` | Step-by-step reproduction instructions |
| 9 | `cvss_severity` | CVSS score or severity rating |
| 10 | `references` | References section with working URLs |

### Run the evaluator:
```bash
# Check a single skill
python auto_research/evaluator.py skills/your-category/your-skill/SKILL.md

# Check all skills and auto-fix failures
python auto_research_mutator.py
```

---

## YAML Frontmatter Template

```yaml
---
name: skill-name-here
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Multi-line description explaining WHAT the skill does and WHEN to use it.
  Must be at least 20 characters. Be specific about use cases and triggers.
domain: cybersecurity
subdomain: bug-hunting | penetration-testing | red-teaming | ai-red-teaming | exploit-development | osint-reconnaissance | forensics-ir | malware-analysis
category: Category Name
difficulty: beginner | intermediate | advanced | expert
estimated_time: "X-Y hours"
mitre_attack:
  tactics: [TA0001]
  techniques: [T1190]
cve_references: [CVE-XXXX-XXXXX]
owasp_category: "A01:2021-Category"
platforms: [linux, windows, macos]
tags: [tag1, tag2, tag3]
tools: [tool1, tool2]
version: "1.0"
author: Your Name
license: Apache-2.0
---
```

---

## Skill Body Structure

After the YAML frontmatter, include these sections:

```markdown
# Skill Name

## When to Use
[Trigger conditions — what scenarios should activate this skill]

## Prerequisites
[Required tools, access levels, knowledge]

## Workflow

### Phase 1: Reconnaissance
[Commands, expected outputs, decision points]

### Phase 2: Exploitation
[Concrete payloads, tools, techniques]

### Phase 3: Post-Exploitation
[Impact demonstration, data access proof]

## 🏆 Elite Chaining Strategy
[How top 1% hunters chain this with other vulns for max impact]
[The "$500 vs $50,000 report" methodology]

## 🔴 Red Team — Offensive Operations
[Attack techniques, OPSEC considerations]

## 🔵 Blue Team — Detection & Defense
[Detection rules, SIEM queries, IOCs]

## 🛡️ Remediation & Mitigation
[Specific fixes, configurations, patches]

## Key Concepts
| Term | Definition |
|---|---|

## Output Format
[Report template for bug bounty submission]

## Real-World Examples
[CVE case studies, real bounty examples]

## References
- [Source 1](https://url)
- [Source 2](https://url)
```

---

## What We're Looking For

### 🔥 High Priority
- **AI Red Teaming** — LLM attacks, agent security, ML adversarial techniques (new attack vectors emerge weekly)
- **Exploit Development** — Modern binary exploitation, browser exploits
- **Cloud Security** — AWS/GCP/Azure penetration testing, cross-account attacks
- **Container/K8s** — Escape techniques, cluster exploitation
- **Real CVE case studies** — Additions to existing skills with recent CVEs

### 📋 Medium Priority
- OSINT and reconnaissance skills
- Forensics and incident response
- Malware analysis
- Wireless/IoT security
- Mobile application testing

### 🔗 Attack Chain Contributions
If you discover a novel attack chain, add it to the [Attack Chain Composer](./tools/attack-chain-composer/SKILL.md)!

---

## Code of Conduct

- Be respectful and constructive in all interactions
- All skills are for **authorized testing and education only**
- No malware, no exploit code targeting unauthorized systems
- Follow responsible disclosure practices
- Credit original researchers in your References section

---

## Recognition

All contributors are recognized in:
- [CONTRIBUTORS.md](./CONTRIBUTORS.md) — with contribution details
- [LEADERBOARD.md](./LEADERBOARD.md) — skills you contribute appear on the quality leaderboard

---

## Questions?

Open an issue with the `question` label or start a discussion.
