# **Final Solution**

## **Overview**

The application exposes a flag through a PHP page protected by HTTP Basic Authentication.  
While the web layer correctly enforces authentication, the challenge environment allows direct access to the Docker container, enabling the attacker to bypass the authentication mechanism entirely and retrieve the flag.

## **Root Cause**

The vulnerability exists because the system assumes that the attacker is restricted to interacting with the application through the web interface.

However, since the application is deployed inside a locally accessible Docker container, this assumption is invalid.  
An attacker with access to the container can directly inspect the filesystem and bypass all web-based access controls.

## **Exploit Steps**

1.  Identify the running container:  
    docker ps
2.  Access the container shell:  
    docker exec -it &lt;container_id&gt; /bin/bash
3.  Navigate to the web root and inspect files:  
    cd /var/www/html  
    ls -la
4.  Read the application files and retrieve the flag.

## **Technical Details**

- **Requests used**
    - curl requests were used to test:
        - HTTP methods (OPTIONS, HEAD)
        - path variations (/index.php, /./index.php, //index.php)
    - All returned 401 Unauthorized or 403 Forbidden
- **Parameters manipulated**
    - HTTP method
    - URL path structure
- **Logic exploited**
    - The application relies entirely on Apache Basic Auth
    - No protection exists at the environment level
    - Direct container access bypasses authentication completely

## **Impact**

An attacker can:

- bypass authentication without valid credentials
- access protected application files
- retrieve sensitive data (e.g., the flag)
- fully compromise the application environment

## **Mitigation**

- Do not rely solely on web server authentication when distributing the full runtime environment
- Restrict or isolate access to the Docker container
- Avoid storing sensitive data in accessible filesystem locations
- Design challenges (or systems) assuming that local access may be possible

## **Key Insight**

The main takeaway is that security mechanisms are only effective within the assumptions they are built on.  
Once those assumptions are broken (e.g., by gaining container access), the protection becomes meaningless.

## **Relation to Business Logic**

This is a business logic flaw because the system’s security model is based on an incorrect assumption about attacker behavior.

The application enforces the rule:

"Only authenticated users can access the flag"

However, the deployment allows an alternative path (direct container access) that bypasses this rule entirely.

Therefore, the vulnerability is not due to a technical misconfiguration in Apache or PHP, but due to flawed assumptions in the system design.
