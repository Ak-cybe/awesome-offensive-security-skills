---
name: business-logic-bypass
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and exploit flaws in the core business rules and logic of web applications. This skill
  focuses on manipulation of application workflows, pricing, inventory limitations, and multi-step
  processes. Use this skill when bug hunting or testing e-commerce, banking, or SaaS platforms
  where standard technical vulnerabilities (e.g., XSS/SQLi) are not present but the application's
  logic is flawed.
domain: cybersecurity
subdomain: bug-hunting
category: Logic Flaws
difficulty: advanced
estimated_time: "4-8 hours"
mitre_attack:
  tactics: [TA0040]
  techniques: [T1499, T1565]
platforms: [linux, windows, macos]
tags: [business-logic, bug-bounty, e-commerce, race-conditions, parameter-tampering, order-manipulation]
tools: [burpsuite, python]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Business Logic Flaws & Bypasses

## When to Use
- When testing critical business functions (Checkout carts, Fund transfers, Password resets, Subscription tiers).
- During deep manual penetration tests and Bug Bounty programs (logic bugs yield very high bounties and cannot be found by automated scanners).
- When standard input validation tools (SQLmap, XSS payloads) yield no results.

## Workflow

### Phase 1: Application Mapping & Rule Identification

```text
# 1. Map the 'Happy Path'
# Use the application exactly as intended. Buy an item, apply a coupon, check out, track shipping.
# Intercept all traffic using Burp Suite and send it to the Proxy History.

# 2. Identify Business Rules (The Assumptions)
# What is the application assuming you will do?
# Examples:
# - A user will a coupon once.
# - A user will not put a negative quantity in the shopping cart.
# - A user must pay step 3 before jumping to step 4 (download).
# - A user will only transfer funds from an account they own.
```

### Phase 2: Price and Parameter Tampering

```python
# Focus: Tampering with invisible parameters or data types during transit.

# 1. Negative Values & Integer Overflow
# Send POST /cart/add
# {"item_id": 12, "quantity": -10}
# Try negative quantities to reduce the total cart price.
# Try MAX_INT (2147483647 + 1) to roll over prices to negative values.

# 2. Price Manipulation directly
# Send POST /checkout
# Does the client decide the price instead of the DB?
# {"item_id": 12, "price": 0.01}

# 3. Currency / Type Mismatch
# Send POST /transfer
# {"amount": "100.00USD", "to": "attacker"}
# What if you change currency? {"amount": "100.00JPY"}
# What if you pass an Array instead of a String? {"amount": [1000]}
```

### Phase 3: Workflow Order Circumvention (Skipping Steps)

```text
# Focus: Skipping mandatory steps in a multi-step process.

# Example Process:
# Step 1: /cart (Add items)
# Step 2: /shipping (Add address)
# Step 3: /payment (Enter credit card -> validation -> True)
# Step 4: /download_digital_goods (Provide items based on session)

# Attack:
# Put items in cart (Step 1).
# Completely skip Step 2 and Step 3.
# Directly request POST /download_digital_goods
# Flaw: The backend assumes if you reach Step 4, you must have paid at Step 3, without actually verifying the payment status in the database.
```

### Phase 4: Coupon & Discount Abuse (Race Conditions)

```text
# Focus: Applying single-use limitations multiple times.

# 1. Discount Stacking
# If you can apply a 10% coupon, can you apply it 10 times?
# Intercept the coupon submission request. Send it to Burp Intruder.
# Set payloads to Null Payloads (Generate 50).
# Fire all 50 requests. Did the total price drop to 0%?

# 2. Race Conditions (Turbo Intruder required)
# If the backend checks if a coupon is valid AND THEN consumes it, a microsecond race condition exists.
# Send 30 identical requests applying a single-use $50 gift card simultaneously using Burp Turbo Intruder.
# If the DB locks are poorly implemented, 5 requests might pass the "IS VALID?" check before the first one sets it to "CONSUMED". Total discount: $250.
```

### Phase 5: Account/Trust Boundary Manipulation

```text
# Focus: Mixing objects belonging to different users.
# User A: Premium Account. User B: Free Account.

# 1. Cross-Session Object References
# Log in as User A. Get the session token.
# Log in as User B. Attempt to access Premium features using User B's token but User A's object references.

# 2. The Transfer Trust Flaw
# POST /transfer {"from_account": "VictimAccount", "to_account": "AttackerAccount", "amount": 100}
# The backend assumes "from_account" implicitly belongs to the logged-in user and fails to verify ownership.
```

## 🔵 Blue Team Detection & Defense
- **Server-Side Truth**: NEVER trust the client to dictate prices, quantities, payment status, or access levels. Calculate prices exclusively on the backend based on item IDs.
- **Workflow State Machines**: Ensure multi-step processes rely on strict strict server-side state machines. Step D cannot execute unless the DB confirms Step C completed successfully.
- **Database Locks (Mutexes)**: Prevent Race Conditions (Time-of-Check to Time-of-Use flaws) by utilizing row-level database locks (e.g., `SELECT ... FOR UPDATE`) during crucial transactions like coupon application or fund transfers.
- **Type Casting & Validation**: Strictly type-cast input. Validate that quantities are whole numbers greater than zero.

## Key Concepts
| Concept | Description |
|---------|-------------|
| Business Logic | The custom rules governing how a specific application operates, independent of standard technical code |
| Parameter Tampering | Changing hidden form fields, cookies, or API data strings in transit |
| TOCTOU | Time-of-Check to Time-of-Use; a race condition where data is modified between checking permission and executing the action |
| State Validation | Confirming a user has completed prerequisites before allowing subsequent actions |

## Output Format
```
Bug Bounty Submission Report
============================
Vulnerability: Critical Business Logic Flaw (Price Manipulation via Integer Overflow)
Target: https://shop.target.com/api/cart

Summary:
The shopping cart API suffers from a severe logic flaw involving integer overflows. By adding an item to the cart with a quantity exceeding the 32-bit signed integer capacity (e.g., 2,147,483,648), the calculated total price rolls over into a massive negative value.

Reproduction Steps:
1. Add any expensive item (e.g., a $1,000 Laptop) to the cart.
2. Intercept the request. Modify the quantity parameter: `{"itemId": "123", "quantity": 2147483648}`.
3. Observe the cart total displays `- $2,147,483.00`.
4. Add another expensive item to bring the total slightly above $0 to satisfy payment gateway validation.
5. Successfully check out acquiring thousands of dollars of equipment for $1.00.

Impact: Total compromise of store revenue model and massive potential financial loss.
```

## References
- PortSwigger: [Business Logic Vulnerabilities](https://portswigger.net/web-security/logic-flaws)
- OWASP: [Testing for Business Logic](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/README)
