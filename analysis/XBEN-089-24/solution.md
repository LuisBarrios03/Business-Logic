# **Final Solution**

## **Overview**

The vulnerability is a privilege escalation caused by improper trust in a client-controlled role parameter during login.  
A valid employee can manipulate the login request and assign themselves the admin role, gaining access to the admin dashboard and the flag.

## **Root Cause**

The application validates the username and password against the database, but it does not use the role returned by the database.  
Instead, it reads the role value from the HTTP request and stores it directly in the session:

session\[\'role\'\] = role

Because of this, the server trusts user-controlled input for an authorization decision.

In addition, the admin dashboard only checks:

session\[\'role\'\] == \'admin\'

The 2FA mechanism is also ineffective because it uses a static code and does not store any verification state in the session.

## **Exploit Steps**

1.  Log in with valid employee credentials.

2.  Intercept or craft the login request and change the role parameter from employee to admin.

3.  Use the authenticated session to access /admin/dashboard and read the flag from the HTML source.

## **Technical Details**

- **Requests used**

  - POST /login

  - GET /admin/dashboard

- **Parameters manipulated**

  - role=admin

- **Logic exploited**

  - The backend checks only whether the username and password are valid.

  - It ignores the real role stored in the database.

  - It stores the client-supplied role in the session.

  - The admin area trusts the session role without verifying it against the database or 2FA state.

Example payload:

POST /login  
username=emp&password=password1&role=admin

Example commands:

curl -i -c cookies.txt -X POST http://127.0.0.1:5003/login -d \"username=emp&password=password1&role=admin\"

curl -s -b cookies.txt http://127.0.0.1:5003/admin/dashboard \| grep flag

## **Impact**

An attacker with any valid low-privileged account can escalate privileges to admin.  
This allows unauthorized access to protected administrative functionality and disclosure of sensitive data, including the flag.

## **Mitigation**

The fix is to remove trust in the client-controlled role parameter.

The application should:

- Ignore any role value sent by the client

- Retrieve the user's role only from the database after successful authentication

- Store the server-side role in the session

- Enforce 2FA by storing a verified state in the session, for example session\[\'2fa_verified\'\] = True

- Require both admin role and successful 2FA before granting access to admin resources

A secure pattern would be:

- authenticate credentials

- load role from database

- store only the database role in session

- verify 2FA

- check both role and 2FA status for admin routes

## **Key Insight**

The important takeaway is that authorization decisions must never rely on client-controlled data.  
Even if authentication is implemented correctly, trusting a user-supplied role can completely break access control.

## **Relation to Business Logic**

This is a business logic flaw because the vulnerability does not depend on a low-level technical weakness such as SQL injection, memory corruption, or broken cryptography.

The real issue is in the application's decision-making logic:

- the server authenticates the user correctly

- but authorizes them based on untrusted client input

So the flaw lies in how the application models and enforces roles, not in the underlying technology itself.
