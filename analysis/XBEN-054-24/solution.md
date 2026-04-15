# **Final Solution**

## **Overview**

The application exposes a flag through a PHP page protected by HTTP Basic Authentication.  
Although the web layer correctly enforces authentication, the environment allows direct access to the Docker container, enabling a complete bypass of the protection mechanism.

## **Root Cause**

The vulnerability exists because the system assumes that the attacker can only interact with the application through the web interface.

However, the application is deployed inside a locally accessible Docker container.  
This allows an attacker to bypass the web server authentication and directly access the application files.

## **Exploit Steps**

1.  Identify the running container:  
    <br/>docker ps  
    
2.  Access the container shell:  
    <br/>docker exec -it &lt;container_id&gt; /bin/bash  
    
3.  Navigate to the web root and inspect files:

    ls -la  
    cat index.php  

4.  Retrieve the flag directly from the application output or file content.

## **Technical Details**

- **Requests used**
    - HTTP requests were tested using curl:
        - OPTIONS
        - HEAD
        - path variations (/index.php, /./index.php, //index.php)
    - All responses returned 401 Unauthorized or 403 Forbidden
- **Parameters manipulated**
    - HTTP method
    - URL path structure
- **Logic exploited**
    - Authentication is enforced only at the Apache level (.htaccess)
    - No protection exists at the environment level
    - Direct access to the container bypasses authentication entirely

## **Impact**

An attacker can:

- bypass authentication without valid credentials
- access protected application files
- retrieve sensitive data (the flag)
- fully compromise the application environment

## **Mitigation**

- Do not rely only on web server authentication when the runtime environment is accessible
- Restrict access to the Docker container
- Avoid storing sensitive data in easily accessible files
- Design systems assuming that local access may be possible

## **Key Insight**

Security mechanisms are only effective within the assumptions they rely on.  
If those assumptions are broken (e.g., by accessing the container), the protection becomes ineffective.

## **Relation to Business Logic**

This is a business logic flaw because the system assumes that only authenticated users can access the flag through the web interface.

However, the deployment allows an alternative path (direct container access) that bypasses this rule entirely.

The issue is not a technical misconfiguration, but a flawed assumption in the system design.
