# Security Advisory - BurpAI v1.0

**Product:** BurpAI (Burp Suite AI Extension)  
**Version:** 1.0  
**Release Date:** March 23, 2026  
**Status:** ACTIVE

---

## Overview

BurpAI v1.0 is production-ready with no known critical vulnerabilities.

---

## Risk Assessment

**Overall Level: LOW**

**Secure:**
- ✅ HTTPS-only API communication
- ✅ No hardcoded secrets
- ✅ Input validation
- ✅ Local-only data storage
- ✅ No RCE or file system access

**User Responsibility:**
- ⚠️ Chat history stored in plaintext (manage yourself)
- ⚠️ API keys in home directory (keep secure)
- ⚠️ AI-generated content (verify independently)

---

## Security Practices

**Mandatory:**
1. Secure API keys - treat like passwords
2. Verify AI findings independently
3. Use on trusted networks only

**Recommended:**
4. Keep Burp Suite and Java updated
5. Monitor API usage
6. Rotate keys monthly

---

## Deployment

- Use secure, managed systems
- Apply firewall rules
- Run with least privilege
- Keep audit logs
- Monitor resource usage

---

## Known Limitations

- Jython 2.7 uses older dependencies
- AI analysis depends on model quality
- API rate limits apply
- Chat history not encrypted locally

---

## Incident Response

**If compromised:**
1. Revoke/rotate API keys immediately
2. Check API usage logs
3. Report to maintainers
4. Notify API provider

---

## Security Contacts

See [SECURITY.md](SECURITY.md) for vulnerability reporting and contacts.

---

**Status:** Production Ready ✅  
**Security Review:** No critical vulnerabilities found  
**Last Updated:** March 23, 2026
