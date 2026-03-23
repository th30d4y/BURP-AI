# SECURITY POLICY

## Reporting Security Vulnerabilities

**DO NOT** open a public GitHub issue for security vulnerabilities.

### Responsible Disclosure

If you discover a security vulnerability in BurpAI, please report it privately by:

1. **Email:** Send details to the maintainers (check repository for contact info)
2. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if applicable)
   - Your contact information

### Timeline

- **Immediate:** Acknowledge receipt of your report
- **24-48 hours:** Initial assessment
- **7 days:** Targeted fix or timeline provided
- **30 days:** Security update release with fix
- **Public disclosure:** After 30 days or when patch is available

## Security Considerations

### API Key Security

- **Never commit API keys** to version control
- Store keys in `~/.burpaai/config.json` (user home directory)
- Use environment variables when possible
- Rotate keys regularly
- Use separate keys for production and testing

### HTTPS Only

- All API calls use HTTPS for encryption in transit
- Certificate validation is enforced
- Man-in-the-middle attacks are mitigated

### Request Handling

- Incoming requests are validated before processing
- User input is sanitized to prevent injection attacks
- No arbitrary code execution
- Memory-safe operations

### Data Privacy

- Chat history stored locally only (on user's machine)
- No telemetry or tracking
- No data sent except to configured AI APIs
- User controls what gets analyzed

## Known Limitations

### Current Security Model

1. **Local Storage:** Chat history stored in plaintext locally
   - Mitigated by: Stored in user's home directory with restricted permissions
   
2. **API Keys in Memory:** Keys held in RAM while extension runs
   - Mitigated by: Keys cleared on extension reload; stored encrypted when possible

3. **Jython Compatibility:** Uses Jython 2.7 with older dependencies
   - Mitigated by: Regular security audits; sandboxed in Burp Suite

### Recommended Practices

- Run Burp Suite with minimal privileges
- Don't use BurpAI on untrusted systems
- Keep Burp Suite and Java updated
- Monitor API usage and costs
- Review AI-generated recommendations independently

## Dependencies Security

All dependencies are tracked and monitored:

- **Burp Suite API:** Official, maintained by PortSwigger
- **Java/Swing:** Built into Java Runtime Environment
- **Python libraries:** Listed in requirements.txt
- **Third-party APIs:** User-provided credentials only

### Dependency Updates

- We regularly review and update dependencies
- Security patches applied immediately
- Major updates tested before release

## Incident Response

### If a Vulnerability is Found

1. **Assess severity:** Critical → Emergency patch; High/Medium → Next release; Low → Future release
2. **Develop fix:** Minimal, focused fix with no feature additions
3. **Test thoroughly:** Reproduction test + regression tests
4. **Release:** New version with security advisory
5. **Communicate:** Announce fix through GitHub, changelog, security advisory

## Security Best Practices for Users

### Setup
- [ ] Use a dedicated API key for BurpAI
- [ ] Enable two-factor authentication on API provider account
- [ ] Store config file with restricted permissions (chmod 600)
- [ ] Keep Burp Suite updated
- [ ] Keep Java updated

### Usage
- [ ] Don't analyze production requests through untrusted networks
- [ ] Review all AI-generated recommendations
- [ ] Monitor API usage for unusual activity
- [ ] Rotate API keys regularly
- [ ] Clear chat history periodically

### Infrastructure
- [ ] Run on trusted systems only
- [ ] Use firewall to restrict network access
- [ ] Monitor system logs for unauthorized access
- [ ] Keep antivirus/antimalware up to date

## Security Headers

BurpAI respects:
- Content-Security-Policy
- X-Content-Type-Options
- X-Frame-Options
- Strict-Transport-Security (via HTTPS)

## Version History & Patches

| Version | Date | Security Issues | Status |
|---------|------|-----------------|--------|
| 1.0 | March 23, 2026 | None known | Current |

## Compliance

BurpAI follows:
- OWASP Top 10 guidelines
- CWE/SANS recommendations
- Secure coding practices
- Data privacy principles

## Frequently Asked Questions

**Q: Is my AI API key stored securely?**
A: Keys are stored in user home directory with restricted permissions. Consider them sensitive - treat like passwords.

**Q: Can BurpAI access my local file system?**
A: No, it only has access to HTTP requests through Burp Suite.

**Q: What data is sent to AI APIs?**
A: Only request/response data you explicitly send for analysis.

**Q: Is the extension audited by security professionals?**
A: Not formally, but the code is open-source and subject to community review.

**Q: What if I find a security issue?**
A: Please report privately using the process above. We appreciate responsible disclosure.

---

**Last Updated:** March 23, 2026  
**Current Version:** 1.0  
**Status:** Active - Security reports welcome
