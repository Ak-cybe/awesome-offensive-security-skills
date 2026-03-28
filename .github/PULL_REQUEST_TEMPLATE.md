## Description
<!-- Describe your changes -->

## Type of Change
- [ ] 🆕 New skill
- [ ] ✏️ Skill improvement
- [ ] 🐛 Bug fix
- [ ] 📖 Documentation
- [ ] 🔧 Tooling/infrastructure

## Skill Details (for new/improved skills)
- **Skill Name:** 
- **Category:** 
- **Difficulty:** beginner | intermediate | advanced | expert

## Quality Checklist

All skills must pass the 10-point binary evaluation:

- [ ] `yaml_frontmatter` — Complete YAML header with name, description, difficulty, tags
- [ ] `no_ai_fluff` — No "Certainly!", "Delve into", etc.
- [ ] `red_team_section` — Has 🔴 Red Team section
- [ ] `blue_team_section` — Has 🔵 Blue Team section
- [ ] `poc_payloads` — Concrete code blocks with real commands
- [ ] `mitigation_remediation` — Specific remediation strategies
- [ ] `elite_hunter_methodology` — Elite chaining / OPSEC advice
- [ ] `step_by_step_repro` — Step-by-step reproduction
- [ ] `cvss_severity` — CVSS or severity mentioned
- [ ] `references` — References with working URLs

## Validation

```bash
# I ran the evaluator and all checks pass:
python auto_research/evaluator.py skills/<path>/SKILL.md
```

- [ ] I ran the evaluator and all 10 checks pass
- [ ] I tested the skill with an AI agent
- [ ] I updated index.json (or it will be auto-generated)
