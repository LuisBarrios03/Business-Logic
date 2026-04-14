# Final Solution

## Overview

The challenge consists of a login form that includes a hidden field named `isAdmin`.  
This field is submitted together with user credentials during authentication.

The vulnerability arises from improper handling of this parameter.

---

## Root Cause

The application relies on a client-controlled parameter (`isAdmin`) to determine the user's privilege level.

Instead of validating the user's role on the server side, the application directly trusts the value provided by the client.

This violates a fundamental security principle:  
**client-side data must never be trusted for authorization decisions.**

---

## Exploit Steps

1. Open the login page in the browser
2. Inspect the HTML form using developer tools
3. Locate the hidden field: isAdmin=false
4. Modify its value to: isAdmin=true
5. Submit the form

---

## Technical Details

- **Request type:** POST  
- **Parameters:**
- `username`
- `password`
- `isAdmin`

Modified request:
username=test
password=test
isAdmin=true


- **Logic exploited:**
  The server checks the value of `isAdmin` directly from the request without validating it against a trusted source (such as a session or database).

---

## Result

The exploit successfully grants administrative access.

The application returns the following flag:

FLAG{46c3ef043123012aa7ed0ab5a0c6a7e40a53a624ce3ae406f52e7301a8033a9b}

---

## Impact

An attacker can gain administrative access without valid credentials.

This enables:
- Privilege escalation
- Unauthorized access to restricted functionality
- Exposure of sensitive data

---

## Mitigation

- Do not trust client-side parameters for authorization
- Remove sensitive logic from the client
- Implement server-side role validation (e.g., session-based authentication)
- Ensure privilege levels are determined using trusted sources

---

## Key Insight

The vulnerability is not caused by a low-level technical flaw, but by incorrect system design.

The application assumes that the client provides trustworthy input for a security-critical parameter.

---

## Relation to Business Logic

This is a **business logic vulnerability** because:

- The application behaves correctly at a technical level
- The flaw lies in how authorization is modeled and enforced
- No technical exploit (e.g., injection or memory corruption) is required

The attack succeeds purely by violating implicit assumptions in the application logic.
