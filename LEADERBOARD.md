# 🏆 Skill Quality Leaderboard

> Every skill in CyberSkills Elite passes **10 automated binary evaluations**. No subjective scoring — only pass/fail.

**Last Updated:** 2026-03-28

---

## Overall Score

| Metric | Value |
|--------|-------|
| **Total Skills** | 191 |
| **Skills Passing All Checks** | 191/191 ✅ |
| **Overall Pass Rate** | 100% |
| **Evaluation Checks Per Skill** | 10 |
| **Total Assertions Validated** | 1,910 |

---

## Top-Rated Skills by Category

### 🤖 AI Red Teaming (25/25 passing)

| Rank | Skill | Score | Difficulty |
|------|-------|-------|------------|
| 1 | llm-direct-prompt-injection | 10/10 ✅ | Intermediate |
| 2 | ai-jailbreak-prompt-injection | 10/10 ✅ | Intermediate |
| 3 | ai-agent-tool-abuse-and-privilege-escalation | 10/10 ✅ | Advanced |
| 4 | rag-poisoning-data-exfiltration | 10/10 ✅ | Advanced |
| 5 | mcp-protocol-exploitation | 10/10 ✅ | Advanced |
| 6 | ai-jailbreak-obfuscation-ciphers | 10/10 ✅ | Intermediate |
| 7 | ai-prompt-leaking | 10/10 ✅ | Beginner |
| 8 | ai-data-poisoning | 10/10 ✅ | Advanced |
| 9 | ai-data-extraction-via-ssrf | 10/10 ✅ | Advanced |
| 10 | ai-jailbreak-system-prompts | 10/10 ✅ | Advanced |
| ... | *15 more AI red teaming skills* | 10/10 ✅ | Various |

### 🐛 Bug Hunting — Web Vulnerabilities (28/28 passing)

| Rank | Skill | Score | Difficulty |
|------|-------|-------|------------|
| 1 | xss-reflected-stored-dom | 10/10 ✅ | Intermediate |
| 2 | ssrf-server-side-request-forgery | 10/10 ✅ | Advanced |
| 3 | sqli-manual-and-automated | 10/10 ✅ | Intermediate |
| 4 | idor-vulnerability-hunting | 10/10 ✅ | Intermediate |
| 5 | http-request-smuggling | 10/10 ✅ | Expert |
| ... | *23 more web vuln skills* | 10/10 ✅ | Various |

### 🔑 API Security (9/9 passing)

| Rank | Skill | Score | Difficulty |
|------|-------|-------|------------|
| 1 | jwt-forgery-algorithm-confusion | 10/10 ✅ | Advanced |
| 2 | graphql-injection-introspection | 10/10 ✅ | Intermediate |
| 3 | oauth-flow-exploitation | 10/10 ✅ | Advanced |
| ... | *6 more API security skills* | 10/10 ✅ | Various |

### 🎯 Red Teaming (21/21 passing)

| Rank | Skill | Score | Difficulty |
|------|-------|-------|------------|
| 1 | amsi-bypass | 10/10 ✅ | Expert |
| 2 | active-directory-golden-ticket | 10/10 ✅ | Expert |
| 3 | active-directory-dcsync-attack | 10/10 ✅ | Expert |
| ... | *18 more red teaming skills* | 10/10 ✅ | Various |

### 🔓 Penetration Testing (40/40 passing)

| Rank | Skill | Score | Difficulty |
|------|-------|-------|------------|
| 1 | active-directory-full-attack-chain | 10/10 ✅ | Expert |
| 2 | kubernetes-cluster-exploitation | 10/10 ✅ | Expert |
| 3 | aws-penetration-testing | 10/10 ✅ | Advanced |
| ... | *37 more pentesting skills* | 10/10 ✅ | Various |

---

## Evaluation Criteria

Each skill is checked against these 10 binary evaluations:

| # | Check | What It Validates |
|---|-------|-------------------|
| 1 | `yaml_frontmatter` | Has description, difficulty, tags in YAML header |
| 2 | `no_ai_fluff` | Free of "Certainly!", "Delve into", hallucination markers |
| 3 | `red_team_section` | Contains 🔴 Red Team / Offensive operations section |
| 4 | `blue_team_section` | Contains 🔵 Blue Team / Defensive detection section |
| 5 | `poc_payloads` | Includes concrete code blocks with real commands |
| 6 | `mitigation_remediation` | Has remediation/mitigation strategy |
| 7 | `elite_hunter_methodology` | Includes elite chaining / OPSEC advice |
| 8 | `step_by_step_repro` | Has step-by-step reproduction instructions |
| 9 | `cvss_severity` | Mentions CVSS or severity level |
| 10 | `references` | Ends with References section containing URLs |

---

## Difficulty Distribution

```
Expert:       ████████████████████ 34 skills (18%)
Advanced:     ████████████████████████████████████ 71 skills (37%)
Intermediate: ███████████████████████████████████ 70 skills (37%)
Beginner:     ████████ 15 skills (8%)
```

---

## Run Evaluations Yourself

```bash
# Single skill evaluation
python auto_research/evaluator.py skills/bug-hunting/api-security/jwt-forgery-algorithm-confusion/SKILL.md

# All skills (with auto-fix for failures)
python auto_research_mutator.py

# Generate fresh index
node generate-index.js
```

---

## How to Contribute High-Scoring Skills

See [CONTRIBUTING.md](./CONTRIBUTING.md) for full guidelines. Every contribution must:

1. Pass all 10 binary evaluations
2. Include at least 1 real CVE case study
3. Contain both 🔴 Red Team and 🔵 Blue Team sections
4. Provide working payloads/commands (not theoretical)
5. Include an Elite Chaining Strategy section

---

<div align="center">

**191/191 skills passing all quality checks**

**Zero AI hallucination. Zero fluff. Pure attack knowledge.**

</div>
