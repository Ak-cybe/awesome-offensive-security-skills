---
name: semgrep-custom-rule-writing
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Write custom Semgrep rules to identify organization-specific logic flaws, improper 
  cryptography usage, or missing authorization checks during source code review. 
  This skill focuses on moving beyond default rulesets to locate complex vulnerabilities.
domain: cybersecurity
subdomain: bug-hunting
category: Source Code Analysis
difficulty: intermediate
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0001, TA0007]
  techniques: [T1190]
platforms: [code]
tags: [semgrep, sast, source-code-review, static-analysis, custom-rules, bug-hunting]
tools: [semgrep, code-editor]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Semgrep Custom Rule Writing

## When to Use
- During a white-box penetration test or source code review when looking for bespoke vulnerabilities that generic SAST tools fail to detect.
- To codify and hunt for organization-specific anti-patterns (e.g., calling an internal API without passing the authentication context).

## Workflow

### Phase 1: Understanding Semgrep Patterns

```yaml
# Concept: Semgrep syntax rules:
  - id: simple-eval-detection
    pattern: eval(...)
    message: "Avoid using eval() as it can lead to code injection."
    languages: [javascript, python]
    severity: ERROR
```

### Phase 2: Utilizing Metavariables

```yaml
# rules:
  - id: python-exec-with-variable
    pattern: exec($X)
    message: "Using exec() on variable $X is dangerous."
    languages: [python]
    severity: WARNING
```

### Phase 3: Pattern-Inside and Pattern-Not (Contextual Matching)

```yaml
# rules:
  - id: missing-auth-check-flask
    patterns:
      - pattern-inside: |
          @app.route(...)
          def $FUNC(...):
            ...
      - pattern: return $RENDER(...)
      - pattern-not-inside: |
          @login_required
          def $FUNC(...):
            ...
      - pattern-not-inside: |
          if current_user.is_authenticated:
            ...
    message: "Flask route missing @login_required or explicit authentication check."
    languages: [python]
    severity: ERROR
```

### Phase 4: Testing Rules via Semgrep CLI

```bash
# # semgrep --config custom-rules.yml src/
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Identify Pattern ] --> B{Write Rule ]}
    B -->|Yes| C[Test Rule ]
    B -->|No| D[Refine Scope ]
    C --> E[Execute Scan ]
```

## 🔵 Blue Team Detection & Defense
- **CI/CD Integration Pipeline Validation**: **Centralized Rule Repositories**: **Developer Education**: Key Concepts
| Concept | Description |
|---------|-------------|
| Abstract Syntax Trees (AST) | |
| Taint Analysis | |

## References
- Semgrep: [Writing Rules Documentation](https://semgrep.dev/docs/writing-rules/rule-syntax/)
- GitHub Security Lab: [Using Semgrep to find vulnerabilities](https://securitylab.github.com/research/semgrep-rule-writing/)
