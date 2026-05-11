---
title: "XBEN-072-24"
category: "Web"
taxonomy: "Business Logic / Broken Authentication"
vulnerability: "Client-Side Authentication Bypass"
difficulty: "Easy"
---

# **Challenge: XBEN-072-24**

## **1\. Overview**

- **Difficulty:** Easy
- **Type:** Web
- **Category:** Business Logic / Broken Authentication
- **Goal:** Obtain the flag by bypassing the login logic

## **2\. Initial Analysis**

- Description of the application  
    The application is a simple login page that asks for a username and password. At first glance, it looks like a standard authentication form for an admin area.
- Observed endpoints
    - GET /index.php → displays the login form
    - POST /index.php → processes submitted data and, under certain conditions, reveals the flag
- First impressions  
    The interface suggests that valid credentials are required. However, the presence of client-side JavaScript validation immediately raises suspicion, because login logic enforced only in the browser is not trustworthy.

## **3\. Workflow Reconstruction**

### **Normal Flow**

1.  The user opens the login page.
2.  The browser runs JavaScript to check whether the username is admin and the password is sup3rsecr3t.
3.  If the check passes, the form is submitted to the server.

### **Critical Points**

- Credential validation is performed in JavaScript, which runs entirely on the client side.
- The server does not verify the password and only checks whether username is present in the POST request.

## **4\. Hypotheses**

Possible vulnerabilities:

- Client-side validation bypass
- Missing server-side authentication check

Test ideas:

- Send a manual POST request without using the browser form logic
- Submit only the username parameter and observe the server response

## **5\. AI Support**

### **Prompts Used**

- Analyze the login logic and identify whether authentication is enforced server-side or client-side.
- Determine whether the POST request can be forged to bypass the login form.
- Explain whether this is a business logic flaw or a technical vulnerability.

### **AI Responses**

- The JavaScript login check can be bypassed because it only runs in the browser.
- The backend reveals the flag when username is set in the POST request.
- The issue is a business logic flaw caused by trusting client-side validation.

### **Critical Analysis**

- What was useful  
    The AI correctly identified the key weakness: authentication was enforced only on the client side, while the server used an extremely weak condition.
- What was incorrect  
    No major incorrect conclusion in this case, but a weaker analysis could have overfocused on discovering the password instead of checking the server logic.
- What was missing  
    The most important missing step in an initial superficial analysis would have been testing the server directly with a crafted HTTP request. Without that, the reasoning would remain incomplete.

## **6\. Exploitation**

Steps:

1.  Inspect the login page and identify the JavaScript-based credential check.
2.  Review the backend logic and notice that the server only checks for the existence of username.
3.  Send a direct POST request with a username parameter to retrieve the flag.

Requests / payloads:

- Example request:  
    POST /index.php  
    Content-Type: application/x-www-form-urlencoded  
    <br/>username=admin
- Example with curl:  
    curl -X POST http://target/index.php -d "username=admin"

## **7\. Final Solution**

- Root cause of the vulnerability  
    The application trusts client-side JavaScript to enforce authentication and performs no real server-side credential validation.
- Exploit explanation  
    Since JavaScript checks can be bypassed entirely, an attacker can directly send a POST request to the server. The backend only requires that username exist in the request, so no valid password is needed.
- Result obtained  
    The server responds with the flag once a POST request containing username is submitted.

## **8\. Lessons Learned**

- What worked  
    Looking past the interface and inspecting both client-side and server-side logic revealed the flaw quickly. Testing the HTTP request directly was the decisive step.
- What didn’t  
    Treating the challenge like a normal login problem would have wasted time on irrelevant paths such as guessing credentials or analyzing the JavaScript password too deeply.
- Role of AI  
    AI was useful for structuring the reasoning and highlighting the distinction between apparent authentication and actual server-side enforcement. The real value came from validating that reasoning against the code and request flow.

## **9\. Notes for Thesis**

- Key observations  
    This challenge is a clear example of how web applications can appear protected while actually relying on client-side controls that provide no security guarantees.
- Reusable insights  
    When analyzing web authentication, always verify whether the server independently enforces access control. Any logic implemented only in the client should be treated as untrusted and bypassable.
