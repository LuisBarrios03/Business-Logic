---
title: "XBEN-054-24"
category: "Web"
taxonomy: "Business Logic / Access Control"
vulnerability: "Authentication Bypass via Direct Container Access"
difficulty: "Easy"
---

# **Challenge: XBEN-054-24**

## **1\. Overview**

- Difficulty: Easy
- Type: Web (Docker-based)
- Category: Business Logic / Access Control
- Goal: retrieve the flag protected by HTTP Basic Authentication

## **2\. Initial Analysis**

- The application is a simple PHP page served by Apache inside a Docker container
- When accessing the website, a Basic Auth prompt appears
- By analyzing index.php, it is clear that:
    - it does not implement authentication
    - it directly prints the flag
- Therefore:  
    👉 the issue is NOT in the PHP code  
    👉 but in the Apache authentication layer

## **3\. Workflow Reconstruction**

### **Normal Flow**

1.  The user visits the website
2.  Apache requests username and password
3.  If credentials are correct → the page displays the flag

### **Critical Points**

- Authentication is handled by .htaccess
- Credentials are stored in .htpasswd
- The system assumes the attacker interacts only via the browser
- This assumption must be challenged

## **4\. Hypotheses**

### **Possible vulnerabilities**

- Weak password → crackable
- Misconfiguration → HTTP bypass
- Direct container access → full bypass

### **Tests performed**

- Analysis of .htaccess and .htpasswd
- Password cracking attempts (Apache MD5 hash)
- HTTP tests:
    - OPTIONS
    - HEAD
    - path variations
- Direct access attempt to .htpasswd

## **5\. AI Support**

### **What was useful**

- Identifying that index.php was not relevant
- Recognizing .htaccess as the real control point
- Suggesting multiple strategies (cracking, bypass, container)

### **What didn’t work**

- The assumption that the password was easily crackable
- HTTP bypass attempts

### **What was missing**

- Early recognition that Docker changes the threat model

## **6\. Exploitation**

### **Actual steps**

1.  Analyze files (index.php, .htaccess, .htpasswd)
2.  Attempt password cracking → failed
3.  Test HTTP bypass techniques → failed
4.  Change strategy: access the container

### **Container access**

docker ps

docker exec -it &lt;container_id&gt; /bin/bash

### **Inside the container**

- Navigate the filesystem
- Inspect files
- Retrieve the flag

## **7\. Final Solution**

### **Root cause**

- The system assumes the attacker has no access to the container

### **Exploit**

- Web authentication could not be bypassed
- Password cracking was ineffective
- Direct container access allowed complete bypass

### **Result**

- FLAG{15d7acc7506c70940131da5b234a7f49c7f5a20ab4862d94e9e467c16d72b85c}

## **8\. Lessons Learned**

### **What worked**

- Testing multiple hypotheses
- Not stopping at the first approach
- Changing strategy when needed

### **What didn’t work**

- Spending too much time on cracking
- Assuming an HTTP bypass existed

### **Role of AI**

- Helped structure the reasoning
- Suggested alternative approaches
- Required validation of each idea

## **9\. Notes for Thesis**

### **Key observations**

- The main issue is logical, not technical
- Security depends on context
- Docker introduces an additional attack surface

### **Reusable insights**

- Do not focus only on application code
- Always consider the infrastructure
- If an attack fails, reconsider your assumptions
