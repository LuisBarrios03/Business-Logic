#**Final Solution**

## **Overview**

The application contains a flawed authentication mechanism that allows an attacker to bypass the login process and gain administrative access without knowing a valid password.

## **Root Cause**

The vulnerability exists because the application compares the user-supplied password against an **uninitialized variable ($password)**.

Since $password is never defined, the authentication logic does not verify credentials against any real or stored value. This results in a comparison against a null or empty value, making the check unreliable and bypassable.

## **Exploit Steps**

1.  Analyze the source code and identify that $password is not initialized
2.  Understand that the strcmp comparison is performed against an undefined value
3.  Send a request with:
    - username=admin
    - an empty password

## **Technical Details**

- **Requests used:**

GET /index.php?username=admin&password=

- **Parameters manipulated:**
    - username → set to admin
    - password → set to empty value
- **Logic exploited:**
    - The condition:  
        <br/>strcmp($\_GET\['password'\], $password) == 0  
        <br/>is evaluated with $password undefined, allowing the comparison to succeed with an empty input.  
        

## **Impact**

An attacker can:

- Bypass authentication entirely
- Gain administrative access
- Retrieve sensitive information (the flag)

In a real-world scenario, this could lead to full account compromise and unauthorized access to protected resources.

## **Mitigation**

To fix this vulnerability:

- Properly initialize and store passwords (e.g., database or configuration)
- Use secure password handling:
    - password_hash()
    - password_verify()
- Avoid using GET for sensitive data
- Implement strict input validation
- Enable error handling to detect undefined variables

## **Key Insight**

Authentication mechanisms must rely on **well-defined and trusted data sources**. Any comparison against undefined or implicit values can completely break the security model.

## **Relation to Business Logic**

This is a **business logic flaw**, not just a technical vulnerability, because:

- The issue is not caused by PHP itself or by a low-level bug
- The system fails at the **design level of authentication**
- The application assumes a valid password exists but never defines or enforces it

Even if implemented in another language, the same flawed logic (comparing against a non-existent credential) would still result in an authentication bypass.
