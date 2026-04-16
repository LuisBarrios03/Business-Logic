# **Final Solution**

## **Overview**

The challenge contains a **broken authentication mechanism** where access to sensitive data (the flag) is granted without proper server-side validation. The application relies on client-side checks that can be easily bypassed.

## **Root Cause**

The vulnerability exists because the application:

- Performs credential validation only in **client-side JavaScript**
- Does **not enforce authentication on the server**
- Uses a weak condition:  
    <br/>isset($\_POST\['username'\])  
    <br/>instead of verifying actual credentials  
    

This creates a situation where **any request containing a username parameter is treated as authenticated**.

## **Exploit Steps**

1.  Analyze the login page and identify that validation is done via JavaScript.
2.  Inspect the backend code and observe that it only checks for the existence of username.
3.  Send a crafted POST request directly to the server with a username parameter to retrieve the flag.

## **Technical Details**

- Requests used  
    <br/>POST /index.php  
    Content-Type: application/x-www-form-urlencoded  
    <br/>username=admin  
    
- Parameters manipulated
    - username → injected manually in the POST request
- Logic exploited
    - The server assumes that if username is present, the user is authenticated
    - No password or session validation is performed

## **Impact**

An attacker can:

- Bypass the login mechanism completely
- Gain unauthorized access to protected functionality
- Retrieve sensitive information (the flag)

In a real-world scenario, this could lead to full account compromise or data leakage.

## **Mitigation**

To fix the vulnerability:

- Implement **server-side authentication checks**
- Validate both username and password on the server:  
    <br/>if($\_POST\['username'\] === 'admin' && $\_POST\['password'\] === '...'){  
    
- Use secure password handling (hashing, verification)
- Introduce session management to track authenticated users
- Never rely on client-side validation for security decisions

## **Key Insight**

**Client-side validation is not security.  
**Any logic enforced in the browser can be bypassed by directly interacting with the server.

## **Relation to Business Logic**

This is a **business logic flaw** because:

- The issue is not due to a low-level technical bug (e.g. buffer overflow, SQL injection)
- The application’s **intended authentication flow is incorrectly designed**
- The system incorrectly assumes that the client enforces rules reliably

The vulnerability arises from **incorrect trust assumptions and flawed application logic**, not from improper use of a specific technology.
