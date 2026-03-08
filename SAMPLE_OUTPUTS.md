## 💡 Usage Examples

### Basic Health Check
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/health' \
  -H 'accept: application/json'
```
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-08T08:22:54.882615",
  "version": "0.1.0"
}
```

### Upload a Document

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/documents/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@security_policy.txt;type=text/plain'
```

**Response:**
```json
{
  "message": "Document uploaded and processed successfully",
  "filename": "security_policy.txt",
  "chunks_created": 1,
  "document_ids": [
    "5a05f19e-e0f5-4406-9b28-14e42b2591da"
  ]
}
```

### Ask a Question

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "include_sources": true,
  "question": "What are the key security risks?"
}'
```

**Response:**
```json
{
  "question": "What are the key security risks?",
  "answer": "The key security risks are:\n- Weak password policies\n- Lack of multi-factor authentication\n- Unauthorized access to internal systems\n- Unencrypted data transmission",
  "sources": [
    {
      "content": "Enterprise Security Policy\n\nThe organization enforces strict access control policies to protect sensitive data.\n\nKey Security Risks:\n- Weak password policies\n- Lack of multi-factor authentication\n- Unauthorized access to internal systems\n- Unencrypted data transmission\n\nSecurity Measures:\n- Enforce strong passwords\n- Enable multi-factor authentication (MFA)\n- Monitor login attempts\n- Encrypt sensitive data\n\nFailure to follow these policies may lead to security breaches and compliance violations.",
      "metadata": {
        "source": "security_policy.txt"
      }
    },
    {
      "content": "Enterprise Security Policy\n\nThe organization enforces strict access control policies to protect sensitive data.\n\nKey Security Risks:\n- Weak password policies\n- Lack of multi-factor authentication\n- Unauthorized access to internal systems\n- Unencrypted data transmission\n\nSecurity Measures:\n- Enforce strong passwords\n- Enable multi-factor authentication (MFA)\n- Monitor login attempts\n- Encrypt sensitive data\n\nFailure to follow these policies may lead to security breaches and compliance violations.",
      "metadata": {
        "source": "security_policy.txt"
      }
    },
    {
      "content": "Enterprise Security Policy\n\nThe organization enforces strict access control policies to protect sensitive data.\n\nKey Security Risks:\n- Weak password policies\n- Lack of multi-factor authentication\n- Unauthorized access to internal systems\n- Unencrypted data transmission\n\nSecurity Measures:\n- Enforce strong passwords\n- Enable multi-factor authentication (MFA)\n- Monitor login attempts\n- Encrypt sensitive data\n\nFailure to follow these policies may lead to security breaches and compliance violations.",
      "metadata": {
        "source": "security_policy.txt"
      }
    },
    {
      "content": "Enterprise Security Policy\n\nThe organization enforces strict access control policies to protect sensitive data.\n\nKey Security Risks:\n- Weak password policies\n- Lack of multi-factor authentication\n- Unauthorized access to internal systems\n- Unencrypted data transmission\n\nSecurity Measures:\n- Enforce strong passwords\n- Enable multi-factor authentication (MFA)\n- Monitor login attempts\n- Encrypt sensitive data\n\nFailure to follow these policies may lead to security breaches and compliance violations.",
      "metadata": {
        "source": "security_policy.txt"
      }
    }
  ],
  "processing_time_ms": 3717.26
}
```

### External System Integration Agent

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/integration/github-summary' \
  -H 'accept: application/json'
```
**Response:**
```json

{
  "source": "github",
  "summary": "Repository enterprise-ai has 3 recent commits."
}
```

### Agentic Security Intelligence

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/agent/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "source": "incident_logs"
}'
```
**Response:**
```json
{
  "summary": "### 1. Summary\nThe security logs indicate several critical issues within the system. There is a database timeout error, which may affect system performance and availability. Additionally, there are multiple failed login attempts, suggesting potential brute-force attacks or unauthorized access attempts. An explicit unauthorized access attempt has also been logged, indicating a serious security breach. Finally, a system restart has been completed, which may be a response to the issues detected.\n\n### 2. Severity\n- **Database timeout detected**: MEDIUM\n- **Multiple failed login attempts**: HIGH\n- **Unauthorized access attempt**: HIGH\n- **System restart completed**: LOW\n\n### 3. Recommendations\n1. **Database Timeout Detected**:\n   - Investigate the cause of the database timeout. Check for performance issues, such as slow queries or resource constraints.\n   - Optimize database queries and consider increasing resources if necessary.\n   - Implement monitoring tools to alert on future timeouts.\n\n2. **Multiple Failed Login Attempts**:\n   - Implement account lockout policies after a certain number of failed login attempts to prevent brute-force attacks.\n   - Encourage users to use strong, unique passwords and consider implementing multi-factor authentication (MFA).\n   - Review logs to identify the source of the failed attempts and block any suspicious IP addresses.\n\n3. **Unauthorized Access Attempt**:\n   - Immediately investigate the unauthorized access attempt to determine the source and nature of the attack.\n   - Review user access controls and permissions to ensure that only authorized personnel have access to sensitive areas of the system.\n   - Consider implementing intrusion detection systems (IDS) to monitor for future unauthorized access attempts.\n\n4. **System Restart Completed**:\n   - Ensure that the system restart was performed as a precautionary measure and not due to a critical failure.\n   - Review system logs to confirm that the restart did not cause any additional issues.\n   - Schedule regular maintenance and updates to minimize the need for unexpected restarts.\n\nBy addressing these issues promptly, the security and stability of the system can be improved, reducing the risk of future incidents.",
  "severity": "HIGH",
  "recommendations": [
    "Review access logs",
    "Enable MFA"
  ]
}
```