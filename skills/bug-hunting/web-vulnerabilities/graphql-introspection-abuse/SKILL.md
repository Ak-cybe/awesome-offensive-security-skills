---
name: graphql-introspection-abuse
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit misconfigured GraphQL endpoints possessing enabled Introspection functionality. By running 
  a massive introspection query, an attacker can reliably extract the entire API schema, revealing 
  hidden functionality, undocumented queries/mutations, and sensitive data structures for further 
  exploitation.
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: beginner
estimated_time: "1 hour"
mitre_attack:
  tactics: [TA0043, TA0007]
  techniques: [T1596, T1592]
platforms: [web, api]
tags: [web-security, graphql, introspection, api, bug-hunting, discovery]
tools: [burp-suite, graphql-voyager, inql]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# GraphQL Introspection Abuse

## When to Use
- Whenever you encounter a GraphQL endpoint (often `/graphql`, `/api/graphql`, `/v1/graphql`) during a web penetration test or bug bounty.
- When you need to systematically map out a complex API backend, finding administrative mutations or hidden fields not exposed by the front-end application.

## Workflow

### Phase 1: Identifying GraphQL

```text
# Concept: 1. ```

### Phase 2: The Introspection Query

```graphql
# Concept: query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
```

### Phase 3: Analyzing the Schema

```text
# 1. 2. 3. ```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Send Introspection superbly ] --> B{Data ]}
    B -->|Yes| C[Visualize ]
    B -->|No| D[Brute properly ]
    C --> E[Test ]
```

## 🔵 Blue Team Detection & Defense
- **Disable Introspection in Production**: **Rate Limiting and Query Cost Analysis**: Key Concepts
| Concept | Description |
|---------|-------------|
| GraphQL | |
| Schema | |

## References
- HackerOne: [How to exploit GraphQL](https://www.hackerone.com/ethical-hacker/how-exploit-graphql)
- PayloadAllTheThings: [GraphQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection)
- PortSwigger: [GraphQL API vulnerabilities](https://portswigger.net/web-security/graphql)
