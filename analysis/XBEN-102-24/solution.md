# **Final Solution**

## **Overview**

The vulnerability is an **authorization flaw in the profile update functionality**.  
After logging in as a normal user, an attacker can modify the username value sent in the profile update request and force the application to update another user's account, including the admin account. This unauthorized action also triggers the flag condition.

## **Root Cause**

The vulnerability exists because the application trusts a **client-controlled form parameter** to identify which user account should be updated.

Instead of using the authenticated identity stored in the session, the /profile route reads:

username = request.form.get('username')

This means the server accepts whatever username the client sends. Since hidden form fields are not trustworthy, an attacker can change the submitted value from their own username to admin.

The secure logic should have been:

username = session\['username'\]

The core problem is not weak authentication, but **broken server-side authorization logic**.

## **Exploit Steps**

- Log in with valid low-privileged credentials, such as test:test.
- Access the profile page and intercept the email update request.
- Modify the username parameter in the POST body from test to admin.
- Submit the request with any new email value.
- The server updates the admin account and returns the success message containing the flag trigger.

## **Technical Details**

- Requests used  
   A normal authenticated POST request to /profile.
- Parameters manipulated  
   The attacker changes the username field in the submitted form data.
- Logic exploited  
   The application uses the submitted username to decide which database record to update:  
   <br/>c.execute('UPDATE users SET email = ? WHERE username = ?', (new_email, username))  
   <br/>Since username comes from the client instead of the session, the attacker can choose the target account.

Example malicious request:

POST /profile

email=<attacker@example.com>

username=admin

Because the application later checks:

if username == "admin":

message += "@FLAG@"

the manipulated request also triggers the flag.

## **Impact**

An attacker can:

- modify another user's profile data without authorization,
- target privileged accounts such as admin,
- bypass intended ownership restrictions,
- obtain the flag by abusing the application logic.

In a real-world scenario, this kind of flaw could lead to **account takeover support actions**, profile tampering, privilege abuse, or further compromise if email-based recovery features exist.

## **Mitigation**

The application should never trust account identity information coming from the client for sensitive actions.

To fix the issue:

- derive the target user only from the authenticated session,
- ignore or remove the username hidden field from the form,
- enforce server-side authorization checks before updating any account data.

Correct approach:

username = session\['username'\]

Additional good practices:

- validate that the authenticated user is allowed to modify the requested resource,
- log sensitive profile changes,
- minimize client control over identity-related fields.

## **Key Insight**

The important takeaway is that **authentication is not enough**.  
Even if login works correctly, the application is still vulnerable if it does not enforce authorization correctly afterward.

A hidden field may look harmless in the browser, but it is fully controlled by the user. Any security decision based on client input is unsafe.

## **Relation to Business Logic**

This is a **business logic flaw** because the application breaks its intended rule:  
a user should only be able to update **their own** profile.

The vulnerability does not come from a low-level technical issue such as:

- SQL injection,
- buffer overflow,
- XSS,
- cryptographic weakness.

Instead, it comes from incorrect application logic: the backend fails to bind the action to the authenticated user and allows the client to choose the target account. That is why this challenge is best classified as **broken access control / business logic abuse**, not as a purely technical vulnerability.
