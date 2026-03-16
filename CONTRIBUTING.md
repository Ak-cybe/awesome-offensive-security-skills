# Contributing to CyberSkills Elite

Thank you for your interest in contributing! We welcome contributions from the cybersecurity community.

## How to Contribute

### Adding New Skills

1. **Fork** the repository
2. **Create a branch**: `git checkout -b add-skill/new-skill-name`
3. **Create the skill directory**: `skills/<category>/<subcategory>/skill-name/`
4. **Write SKILL.md** following our enhanced format (see below)
5. **Run validation**: `node generate-index.js --validate`
6. **Submit a Pull Request**

### Skill Quality Requirements

Every skill MUST include:

- [ ] **Complete YAML frontmatter** with all required fields
- [ ] **Description > 20 characters** (no empty/broken descriptions)
- [ ] **Multi-phase workflow** with real, tested commands
- [ ] **Decision points** where applicable
- [ ] **Blue Team Detection section** (offensive skills must include defensive counterpart)
- [ ] **At least 1 real CVE case study** (for vulnerability/exploit skills)
- [ ] **Professional report template** in Output Format section
- [ ] **Key Concepts table** defining all technical terms
- [ ] **Tools & Systems table** with installation instructions
- [ ] **Troubleshooting section** with common problems and solutions
- [ ] **References section** with working links

### YAML Frontmatter Template

```yaml
---
name: skill-name-here
description: >
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

### What We're Looking For

**High Priority:**
- AI Red Teaming skills (LLM attacks, agent security, ML security)
- Exploit Development skills
- Cloud security (AWS/GCP/Azure) penetration testing
- Container/Kubernetes security
- Real CVE case study additions to existing skills

**Medium Priority:**
- OSINT and reconnaissance skills
- Forensics and incident response
- Malware analysis
- Wireless/IoT security

### Code of Conduct

- Be respectful and constructive in all interactions
- All skills are for **authorized testing and education only**
- No malware, no exploit code for unauthorized access
- Follow responsible disclosure practices

## Questions?

Open an issue with the `question` label or start a discussion.
