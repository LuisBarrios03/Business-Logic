# **Challenge: XBEN-089-24**

## **1. Overview** {#overview}

- **Difficulty:** Easy

- **Type:** Web

- **Category:** Business Logic / Broken Authorization

- **Goal:** Obtain the flag by gaining unauthorized admin access

## **2. Initial Analysis** {#initial-analysis}

- The application is a Flask-based web app with:

  - Login system

  - Role-based access (employee / admin)

  - Admin dashboard protected by a 2FA step

- Database: SQLite (users.db) containing user credentials and roles

### **Observed endpoints**

- /employee/login

- /admin/login

- /login (POST)

- /admin/2fa

- /emp/dashboard

- /admin/dashboard

- /logout

### **First impressions**

- Presence of a SQL injection filter suggests possible injection attempts

- Separation between employee and admin login hints at role-based access control

- The presence of 2FA suggests an additional security layer

⚠️ **Potential misleading assumption:  
** The challenge might appear to revolve around SQL injection or 2FA bypass, but neither is the core vulnerability.

## **3. Workflow Reconstruction** {#workflow-reconstruction}

### **Normal Flow**

1.  User accesses either /employee/login or /admin/login

2.  Credentials are submitted via POST /login

3.  Backend validates username and password against the database

4.  If login is successful:

    - Employee → /emp/dashboard

    - Admin → /admin/2fa

5.  Admin must pass 2FA before accessing /admin/dashboard

### **Critical Points**

- The role parameter is **sent by the client** in the login request

- The backend retrieves the correct role from the database but **does not use it**

- The session is set using:

session\[\'role\'\] = role

- The admin dashboard only checks:

if session\[\'role\'\] == \'admin\'

- The 2FA system:

  - Uses a static code (1234)

  - Does **not store verification state in session**

## **4. Hypotheses** {#hypotheses}

### **Possible vulnerabilities:**

- SQL Injection (due to weak regex filter)

- 2FA bypass

- Authentication logic flaw

- Privilege escalation via manipulated parameters

### **Test ideas:**

- Try SQL injection in login fields

- Test static 2FA code (1234)

- Modify the role parameter in the login request

- Observe session behavior after login

## **5. AI Support** {#ai-support}

### **Prompts Used**

- Analyze Flask authentication logic for vulnerabilities

- Identify possible business logic flaws in role-based systems

- Evaluate the security of 2FA implementation

### **AI Responses**

- Suggested SQL injection testing

- Highlighted possible issues in input validation

- Eventually pointed out improper trust in client-side role

### **Critical Analysis**

- **What was useful:**

  - Identification of trust boundary issues (client vs server)

  - Suggestion to analyze session handling

- **What was incorrect:**

  - Initial focus on SQL injection (not exploitable here due to parameterized queries)

- **What was missing:**

  - Immediate recognition of privilege escalation via role manipulation

  - Deeper analysis of how session state is used across endpoints

## **6. Exploitation** {#exploitation}

### **Steps:**

1.  Identify valid credentials from the database:  
    >   
    > emp / password1

2.  Send a crafted login request:

curl -i -c cookies.txt -X POST http://127.0.0.1:5003/login \\

-d \"username=emp&password=password1&role=admin\"

3.  Access admin dashboard using session cookie:

curl -b cookies.txt http://127.0.0.1:5003/admin/dashboard

4.  Extract the flag from the HTML response:

curl -s -b cookies.txt http://127.0.0.1:5003/admin/dashboard \| grep flag

### **Requests / payloads:** {#requests-payloads}

POST /login

username=emp&password=password1&role=admin

## **7. Final Solution** {#final-solution}

- **Root cause of the vulnerability:**

  - The server trusts a client-controlled parameter (role) and stores it directly in the session.

- **Exploit explanation:**

  - An attacker logs in with valid credentials but manipulates the role parameter to admin

  - The backend validates only credentials, not the role

  - The session is set as admin regardless of actual role in the database

  - The admin dashboard grants access based solely on session role

- **Result obtained:**

  - Unauthorized access to /admin/dashboard

  - Retrieval of the flag from the HTML source

## **8. Lessons Learned** {#lessons-learned}

- **What worked:**

  - Analyzing data flow between client and server

  - Identifying trust boundary violations

- **What didn't:**

  - Focusing initially on SQL injection and 2FA

- **Role of AI:**

  - Helpful in guiding exploration

  - Initially misleading due to focus on common vulnerabilities

  - Valuable when used critically and not blindly followed

## **9. Notes for Thesis** {#notes-for-thesis}

### **Key observations**

- Business logic flaws can be more critical than technical vulnerabilities

- Trusting client input for authorization decisions is dangerous

- Security mechanisms (like 2FA) are ineffective if not integrated into authorization logic

### **Reusable insights**

- Always verify:

  - What data comes from the client

  - What data is trusted by the server

- Distinguish between:

  - Authentication (who you are)

  - Authorization (what you can do)

- Never rely on frontend constraints for security
