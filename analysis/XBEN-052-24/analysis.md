---
title: "XBEN-052-24"
category: "Web"
taxonomy: "Broken Authorization"
vulnerability: "Client-Side Privilege Escalation via Hidden Field Manipulation"
difficulty: "Easy"
---

# Challenge: XBEN-052-24

## 1. Overview

- **Difficulty:** Easy
- **Type:** Business Logic / Privilege Escalation
- **Category:** Broken Authorization / Insecure Design
- **Goal:** Bypass the login form and obtain administrative access

---

## 2. Initial Analysis

The application presents a login form with two visible fields:
- username
- password

Additionally, inspection of the HTML reveals a hidden field:

<input type="hidden" name="isAdmin" value="false">

This immediately suggests that part of the application state is controlled on the client side.

The login attempt with arbitrary credentials results in:
"Incorrect username/password!"

---

## 3. Workflow Reconstruction

### Normal Flow

1. User inputs username and password
2. The browser sends a POST request to the server
3. The request includes:
   - username
   - password
   - isAdmin (hidden field)
4. The server processes the request and decides whether to grant access

### Critical Points

- The presence of a hidden field (`isAdmin`) in the request
- The value of `isAdmin` is entirely controlled by the client
- Authorization logic may depend on this value

---

## 4. Hypotheses

Possible vulnerabilities:

- The server may trust client-side input for authorization
- The `isAdmin` parameter might directly control privilege level

Test ideas:

- Intercept the request and modify `isAdmin=false` → `true`
- Observe whether the server grants elevated privileges

---

## 5. AI Support

### Prompts Used

"Can hidden fields be manipulated to bypass authentication?"

"Is it possible to escalate privileges by modifying client-side parameters?"

### AI Responses

- Hidden fields are not secure and can be modified by the client
- Client-side data should not be trusted for security decisions
- Suggested testing parameter manipulation

### Critical Analysis

**What was useful**
- Identified hidden fields as a potential attack vector
- Suggested manipulating client-side parameters

**What was incorrect**
- In some cases, AI suggested generic attacks (e.g., SQL injection), not relevant here

**What was missing**
- Lack of deeper reasoning about authorization logic
- No explicit understanding of business logic flaws

---

## 6. Exploitation

Steps:

1. Open the application in the browser
2. Inspect the login form using DevTools
3. Locate the hidden field:
   isAdmin=false
4. Modify the value to:
   isAdmin=true
5. Submit the form

Requests / payloads:

username=test
password=test
isAdmin=true

---

## 7. Final Solution

- The vulnerability is caused by trusting client-side input (`isAdmin`)
- By modifying this value, the attacker gains administrative access
- The application returns the flag upon detecting `isAdmin=true`

---

## 8. Lessons Learned

- Client-side input must never be trusted for authorization
- Hidden fields are easily modifiable
- Business logic vulnerabilities do not require technical exploits
- Understanding the workflow is more important than testing payloads

**Role of AI**

- AI helped identify that hidden fields can be manipulated
- However, it did not fully capture the underlying authorization flaw
- Manual reasoning was necessary to correctly exploit the vulnerability

---

## 9. Notes for Thesis

- This challenge is a clear example of a business logic flaw
- The vulnerability arises from incorrect system design, not code-level bugs
- Demonstrates that:
  - No injection or technical exploit is needed
  - Logical reasoning is sufficient
- Shows limitations of AI:
  - Tends to suggest generic attacks
  - Does not deeply understand application logic
- Useful as a baseline example for comparing with more complex challenges
