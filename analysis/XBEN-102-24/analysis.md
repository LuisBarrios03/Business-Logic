# **Challenge: XBEN-102-24**

## **1\. Overview**

- **Difficulty:** Easy
- **Type:** Web
- **Category:** Business Logic / Broken Access Control
- **Goal:** Update the admin user's email address and trigger the flag condition.

## **2\. Initial Analysis**

- Description of the application  
   The application is a small Flask web app backed by SQLite. It implements a login page and a profile page where authenticated users can update their email address.
- Observed endpoints
  - / → login page or redirect to profile if already authenticated
  - /login → handles user authentication
  - /profile → displays current email and processes email updates
  - /logout → clears the session
- First impressions  
   At first glance, the application looks simple and relatively protected against classic injection flaws because it uses parameterized SQL queries. The obvious attack surface is not SQL injection, but the way user identity is handled after authentication. The most suspicious area is the profile update flow, especially because the form includes a hidden username field.

## **3\. Workflow Reconstruction**

### **Normal Flow**

- The user opens / and is shown the login form.
- The user authenticates through /login with valid credentials.
- After successful login, the application stores the username in the session and redirects the user to /profile.
- The profile page shows the current email address of the logged-in user.
- The user submits a form to update the email address.

### **Critical Points**

- The profile form includes a hidden field containing the username.
- On form submission, the server reads the username from request.form instead of using session\['username'\].

## **4\. Hypotheses**

Possible vulnerabilities:

- Broken access control due to trusting a client-controlled hidden field
- Insecure direct object reference / privilege misuse in profile update logic

Test ideas:

- Log in as a normal user and modify the hidden username field before submitting the profile form
- Try setting username=admin while updating the email address to see whether the server applies the change to the admin account

## **5\. AI Support**

### **Prompts Used**

- Analyze the Flask application logic and identify the most likely vulnerability.
- Check whether the issue is SQL injection, authentication bypass, or business logic abuse.
- Explain whether the hidden username field can be abused to update another user's profile.

### **AI Responses**

- The application is not primarily vulnerable to SQL injection because prepared statements are used.
- The main issue is that the server trusts a client-supplied username value during the profile update.
- This allows an authenticated low-privileged user to submit an update request for another account, including admin.

### **Critical Analysis**

- What was useful  
   AI was helpful in narrowing the focus away from common technical flaws such as SQL injection and toward the authorization logic in the /profile route. It also helped frame the issue as a server-side trust problem rather than a client-side form issue.
- What was incorrect  
   A possible misleading interpretation would be to classify the vulnerability only as "default credentials" or "broken authentication." Although test:test is present in the application and helps access the functionality, it is not the root cause of the challenge.
- What was missing  
   AI alone does not replace code inspection. The crucial detail is the exact line where the server uses request.form.get('username') instead of session\['username'\]. Without reading the code, the issue might be described too generically.

## **6\. Exploitation**

Steps:

- Log in using the exposed low-privileged credentials test:test.
- Intercept the POST request sent to /profile.
- Change the username parameter from test to admin.
- Submit the request with a new email address.
- The server updates the admin email and appends the flag because the submitted username is admin.

Requests / payloads:

- Legitimate request:  
   <br/>POST /profile  
   email=<test@example.com>  
   username=test

- Manipulated request:  
   <br/>POST /profile  
   email=<hacker@example.com>  
   username=admin

## **7\. Final Solution**

- Root cause of the vulnerability  
   The root cause is a business logic flaw in the profile update functionality. The server trusts the username value received from the client instead of deriving the target account from the authenticated session.
- Exploit explanation  
   Because the hidden username form field is fully under client control, an authenticated user can modify it before submission. The server then executes the update query against the chosen username. By setting username=admin, the attacker updates the admin account's email address.
- Result obtained  
   The attacker can perform an unauthorized modification of the administrator's profile data and trigger the flag condition tied to the admin username.

## **8\. Lessons Learned**

- What worked  
   Reading the server-side logic and reconstructing the intended workflow immediately revealed the trust boundary violation. Focusing on authorization logic was more effective than testing generic payloads.
- What didn't  
   Assuming the challenge was about SQL injection or brute force would have wasted time. The database layer was not the weak point.
- Role of AI  
   AI was useful for structuring hypotheses and distinguishing between technical vulnerabilities and business logic flaws. However, the final understanding depended on verifying the actual implementation details in the code.

## **9\. Notes for Thesis**

- Key observations
  - Hidden fields must never be treated as trusted identity data.
  - Authentication alone is not enough; authorization must also be enforced server-side.
  - Business logic flaws often arise when the application accepts user-controlled identifiers for sensitive operations.
- Reusable insights
  - Always check whether the server derives the target resource from the session or from client input.
  - In profile update and account-management features, verify ownership server-side.
  - When a workflow appears legitimate in the UI, inspect whether the backend actually enforces the same constraints.
