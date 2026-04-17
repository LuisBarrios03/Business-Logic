#**Final Solution**

## **Overview**

The application is vulnerable to a **Broken Authorization / Insecure Design flaw**, where administrative access is granted based on a client-controlled HTTP header rather than proper authentication.

## **Root Cause**

The vulnerability exists because the application trusts the X-Forwarded-For HTTP header to determine whether a request originates from a trusted source (localhost).

However, this header is fully controllable by the client unless it is sanitized or set by a trusted reverse proxy. As a result, an attacker can spoof the header to bypass access controls.

Additionally, the application does not validate username and password at all, making the login mechanism effectively meaningless.

## **Exploit Steps**

1.  Send a POST request to /index.php with arbitrary username and password
2.  Add the HTTP header X-Forwarded-For: 127.0.0.1
3.  The server grants administrative access and reveals the flag

## **Technical Details**

- **Requests used**
    - HTTP POST request to /index.php
- **Parameters manipulated**
    - X-Forwarded-For header set to 127.0.0.1
    - Arbitrary username and password values
- **Logic exploited**
    - The application checks only whether the X-Forwarded-For header matches a trusted IP
    - No actual authentication or session validation is performed

## **Impact**

An attacker can:

- Bypass authentication entirely
- Gain administrative privileges
- Access sensitive information (e.g., the flag)
- Potentially escalate privileges in a real-world scenario

## **Mitigation**

To fix this vulnerability:

- Do not rely on client-controlled headers for authentication or authorization
- Validate user credentials properly using secure authentication mechanisms
- Implement session management and role-based access control
- Trust X-Forwarded-For only if it is set by a properly configured and trusted reverse proxy
- Use server-side IP validation (REMOTE_ADDR) when necessary

## **Key Insight**

The critical issue is not a coding mistake but a flawed trust assumption: the system incorrectly assumes that client-provided data can be used to enforce security decisions.

## **Relation to Business Logic**

This is a **business logic flaw** because the vulnerability arises from incorrect application logic rather than a low-level technical issue.

The system defines access control based on an invalid assumption (that the request originates from localhost if the header says so), instead of enforcing proper authentication and authorization mechanisms.

As a result, the security model itself is broken, not just its implementation.
