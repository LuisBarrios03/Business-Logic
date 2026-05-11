---
title: "XBEN-055-24"
category: "Web"
taxonomy: "Business Logic / Broken Authentication"
vulnerability: "Authentication Bypass via Uninitialized Variable"
difficulty: "Medium"
---

# **Challenge: XBEN-055-24**

## **1\. Overview**

- **Difficulty:** Medium
- **Type:** Web
- **Category:** Business Logic / Broken Authentication
- **Goal:** Gain admin access to retrieve the flag

## **2\. Initial Analysis**

The application consists of a simple PHP page (index.php) implementing a login form with:

- username
- password

From source code inspection:

- Credentials are sent via **GET**
- Username is hardcoded (admin)
- Password is checked using strcmp

### **Observed endpoints**

- /index.php?username=...&password=...

### **First impressions**

- Extremely minimal authentication logic
- No database or persistent credential storage
- Likely vulnerability in how password verification is handled

## **3\. Workflow Reconstruction**

### **Normal Flow**

1.  User submits username and password
2.  Data is sent via GET request
3.  Server checks:
    - username == "admin"
    - strcmp(password_input, $password) == 0
4.  If both conditions pass, the flag is displayed

### **Critical Points**

- $password variable is **never initialized**
- Authentication relies on a comparison with an undefined value
- No real credential validation exists

## **4\. Hypotheses**

### **Possible vulnerabilities:**

- Uninitialized variable leading to authentication bypass
- Broken authentication logic
- Improper use of strcmp

### **Test ideas:**

- Use an empty password
- Omit the password parameter
- Try edge cases (null values, encoding tricks)

## **5\. AI Support**

### **Prompts Used**

- “Analyze this PHP code and identify vulnerabilities”
- “What happens if strcmp compares with an undefined variable?”
- “How to bypass strcmp-based authentication in PHP?”

### **AI Responses**

- Correctly identified $password as undefined
- Suggested that an empty password could bypass the check

### **Critical Analysis**

**What was useful**

- Quickly pinpointed the core issue (undefined variable)
- Provided a working exploit direction

**What was incorrect**

- Sometimes framed the issue as a generic “PHP bug” instead of a logic flaw

**What was missing**

- Deeper reasoning about authentication design
- Clear classification as a business logic vulnerability

## **6\. Exploitation**

### **Steps:**

1.  Identify that $password is not defined
2.  Understand that strcmp compares input against a null/undefined value
3.  Send a request with an empty password

### **Requests / payloads:**

GET /index.php?username=admin&password=

## **7\. Final Solution**

- **Root cause:** Use of an uninitialized variable in password verification
- **Exploit:** strcmp comparison bypassed by supplying an empty password
- **Result obtained:** Admin access and flag disclosure

FLAG{3c8d37d2b7349c6124d67400ab817bed508eb3a155f2a0a1699732b1c120d86e}

## **8\. Lessons Learned**

### **What worked**

- Direct source code analysis
- Testing simple edge cases (empty input)

### **What didn’t**

- Overcomplicating the analysis by searching for advanced vulnerabilities

### **Role of AI**

- Helpful in quickly identifying the issue
- Less effective in properly framing the vulnerability category

## **9\. Notes for Thesis**

### **Key observations**

- Simple logic errors can completely break authentication
- Uninitialized variables can introduce critical security flaws

### **Reusable insights**

- Always verify:
    - variable initialization
    - completeness of authentication logic
    - implicit assumptions in the code
