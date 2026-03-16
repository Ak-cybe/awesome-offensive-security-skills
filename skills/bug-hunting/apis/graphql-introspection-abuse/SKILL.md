---
name: graphql-introspection-abuse
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Exploit exposed GraphQL introspection endpoints to map the entire API schema. This skill 
  details how to extract available queries, mutations, types, and fields, which significantly 
  aids in identifying hidden endpoints, Broken Object Level Authorization (BOLA/IDOR), and 
  mass assignment vulnerabilities.
domain: cybersecurity
subdomain: bug-hunting
category: APIs
difficulty: beginner
estimated_time: "1 hours"
mitre_attack:
  tactics: [TA0007]
  techniques: [T1592.004]
platforms: [web, api]
tags: [graphql, introspection, reconnaissance, api-security, bug-hunting]
tools: [burp-suite, inql, clairvoyance, graphql-voyager]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# GraphQL Introspection Abuse

## When to Use
- During the reconnaissance phase of evaluating web applications that utilize GraphQL.
- To rapidly map the API surface area without relying on brute-force directory or endpoint enumeration.
- To visualize the API schema and identify potentially vulnerable data relationships and administrative mutations.

## Workflow

### Phase 1: Identifying GraphQL Endpoints

Common endpoints include `/graphql`, `/api/graphql`, `/v1/graphql`, `/v2/graphql`, and sometimes `/gql`.

### Phase 2: Sending the Introspection Query

The standard GraphQL Introspection query requests the `__schema` field.

```json
// Concept: Request schema metadata {
  "query": "query IntrospectionQuery { __schema { queryType { name } mutationType { name } types { ...FullType } } } fragment FullType on __Type { kind name fields(includeDeprecated: true) { name args { ...InputValue } type { ...TypeRef } } } fragment InputValue on __InputValue { name type { ...TypeRef } defaultValue } fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name } } }"
}
```

Send this POST request to the endpoint:
```bash
# curl -X POST -H "Content-Type: application/json" -d '{"query":"\n    query IntrospectionQuery {\n      __schema {\n        queryType { name }\n        mutationType { name }\n        subscriptionType { name }\n        types {\n          ...FullType\n        }\n      }\n    }\n\n    fragment FullType on __Type {\n      kind\n      name\n      description\n      fields(includeDeprecated: true) {\n        name\n        args {\n          ...InputValue\n        }\n      }\n    }\n    fragment InputValue on __InputValue {\n      name\n    }\n  "}' http://target.local/graphql
```

### Phase 3: Analyzing the Schema

If introspection is enabled, the server will return a massive JSON response containing the entire schema structure.
Use tools to visualize and parse this data:
- **GraphQL Voyager**: Paste the JSON response into GraphQL Voyager to graphically map the database relationships.
- **InQL (Burp Extension)**: Automatically detects introspection queries and generates a mock structure of all queries and mutations in your Repeater tab.

### Phase 4: Bypassing Disabled Introspection

If the server responds with a syntax error or "GraphQL introspection is not allowed", check for partial introspection or use dictionary attacks.
- **Field Suggestion (Clairvoyance)**: If you misspell a field, GraphQL might say `Did you mean "email"?`. Tools like `Clairvoyance` or `GraphW00f` can brute force and reconstruct the schema based on these error messages.

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Discover /graphql Endpoint ] --> B{Introspection Enabled? ]}
    B -->|Yes| C[Send Full __schema Query ]
    B -->|No| D[Test Field Suggestion Errors ]
    C --> E[Map Queries/Mutations ]
    D -->|Errors exist| F[Brute-force Schema (Clairvoyance) ]
    D -->|No Errors| G[Manual Fuzzing ]
    E & F --> H[Hunt for IDOR / Logic Bugs ]
```

## 🔵 Blue Team Detection & Defense
- **Disable Introspection in Production**: **Disable Field Suggestions**: **Implement Rate Limiting and Depth Limits**: Key Concepts
| Concept | Description |
|---------|-------------|
| GQL Types | |
| Attack Surface Mapping | |

## References
- PortSwigger: [GraphQL API vulnerabilities](https://portswigger.net/web-security/graphql)
- GitHub: [InQL Scanner](https://github.com/doyensec/inql)
