<div align="center">

# 🤖 BurpAI

**AI-Powered Vulnerability Analysis for Burp Suite**

[![Version](https://img.shields.io/badge/Version-1.0-0052CB?style=flat-square&logo=semantic-release)](https://github.com/Stalin-143/BURP-AI/releases/tag/v1.0)
[![License](https://img.shields.io/badge/License-Apache%202.0-0052CB?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-2.7+-0052CB?style=flat-square&logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-00C853?style=flat-square)](SECURITY_ADVISORY.md)

[Official Burp Suite](https://portswigger.net/burp) • [Security Policy](SECURITY.md) • [Changelog](CHANGELOG.md) • [Report Issue](https://github.com/Stalin-143/BURP-AI/issues)

</div>

---

## 🎯 Overview

BurpAI seamlessly integrates **multi-model AI analysis** into Burp Suite, providing intelligent vulnerability detection directly in your pentesting workflow. Instantly analyze HTTP requests and get actionable security insights with zero friction.

**Perfect for:** Security Researchers • Penetration Testers • Bug Bounty Hunters • Security Teams

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Model AI** | 11 AI models with automatic failover (Kimi, DeepSeek, GLM, Qwen, LLaMA, Mistral, etc.) |
| ⚡ **Real-time Analysis** | Background threading—zero UI lag during analysis |
| 🔍 **Smart Detection** | Priority detection for P1/P2 vulnerabilities (RCE, IDOR, SQLi, Auth bypass) |
| 📋 **Native Repeater** | Built-in request/response editing with Burp's native editors |
| 📊 **Request History** | Automatic tracking of 1000+ requests with full context |
| 🎛️ **Easy Configuration** | One-click API key setup, model selection dropdown |
| 💬 **Interactive Chat** | Custom prompts for targeted security analysis |
| 🔒 **Security First** | HTTPS-only, no telemetry, local-only data storage |

---

## 🚀 Quick Start

### 1️⃣ Install
```bash
# In Burp Suite: Extensions → Add → Select burpaai.py
```

### 2️⃣ Configure
- Go to **BurpAI** tab
- Enter your DigitalOcean AI API key → **Save**

### 3️⃣ Analyze
- Load a request in **Repeater**
- Click **"Analyze with AI"**
- Review vulnerability report in chat panel

---

## 📋 Requirements

| Requirement | Details |
|-------------|---------|
| **Burp Suite** | Pro or Community Edition (latest) |
| **API Key** | DigitalOcean AI (free tier available) |
| **Java** | 8+ (included with Burp) |
| **Network** | HTTPS outbound to AI API |

---

## 🔧 Supported Models

```
✅ Alibaba Qwen 3 (32B)
✅ DeepSeek R1 (70B) 
✅ GLM-5
✅ Kimi K2.5
✅ LLaMA 3 & 3.3 (8B-70B)
✅ Mistral Nemo (2407)
✅ NVIDIA Nemotron (120B)
✅ OpenAI GPT OSS (20B-120B)
```

Automatic failover if primary model unavailable.

---

## 🛡️ Security & Compliance

✅ **HTTPS-only** API communication  
✅ **No telemetry** or tracking  
✅ **Local-only** data storage  
✅ **API keys** user-managed  
✅ **Open-source** for transparency  

👉 [Security Policy](SECURITY.md) • [Vulnerability Reporting](SECURITY.md#reporting-security-vulnerabilities) • [Advisory](SECURITY_ADVISORY.md)

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [SECURITY.md](SECURITY.md) | Security policy & best practices |
| [SECURITY_ADVISORY.md](SECURITY_ADVISORY.md) | Release security assessment |
| [CHANGELOG.md](CHANGELOG.md) | Version history & fixes |
| [COLLABORATION.md](COLLABORATION.md) | Contributing guidelines |
| [DISCLAIMER.md](DISCLAIMER.md) | Legal notices & warranty |

---

## 📞 Support & Security

### Report Issues
- **Bugs & Features**: [GitHub Issues](https://github.com/Stalin-143/BURP-AI/issues)
- **General Discussion**: [GitHub Discussions](https://github.com/Stalin-143/BURP-AI/discussions)

### 🔒 Report Security Vulnerabilities
**⚠️ DO NOT open public issues for security vulnerabilities**

Instead, use **GitHub Security Advisory**:
1. Go to [GitHub Security Advisory](https://github.com/Stalin-143/BURP-AI/security/advisories)
2. Click **"Report a vulnerability"**
3. Provide detailed information:
   - Vulnerability description
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if applicable)
4. Submit privately to maintainers

**Or email the maintainers** (See [SECURITY.md](SECURITY.md#reporting-security-vulnerabilities) for contact)

**Thank you for helping keep BurpAI secure!** 🙏

---

## 📄 License

Licensed under **Apache License 2.0** — See [LICENSE](LICENSE) for details.

**Disclaimer**: For authorized security testing only. See [DISCLAIMER.md](DISCLAIMER.md)

---

## 👥 Contributors

Special thanks to the security community for feedback and contributions.

**Want to contribute?** See [COLLABORATION.md](COLLABORATION.md)

---

<div align="center">

**Built for the modern security toolkit** | [v1.0](https://github.com/Stalin-143/BURP-AI/releases/tag/v1.0) | March 2026

</div>

### Critical (P1) - Automatic Detection
- **RCE** - Remote code execution, command injection
- **IDOR** - Insecure direct object reference
- **SSRF** - Server-side request forgery
- **SQLi** - SQL injection
- **Auth Bypass** - Session hijacking, weak auth

### High (P2)
- XSS, CSRF, XXE, Header Injection
- Cookie/credential handling flaws
- Privilege escalation

### Medium & Low
- Missing security headers
- CORS misconfiguration
- Information disclosure
- Weak configuration

---

## AI Models

The extension uses DigitalOcean's inference models and automatically falls back through this chain:

1. alibaba-qwen3-32b
2. deepseek-r1-distill-llama-70b
3. glm-5
4. kimi-k2.5
5. llama3-8b-instruct
6. llama3.3-70b-instruct
7. minimax-m2.5
8. mistral-nemo-instruct-2407
9. nvidia-nemotron-3-super-120b
10. openai-gpt-oss-120b
11. openai-gpt-oss-20b

If the selected model fails, the next model in the chain is automatically tried.

---

---

## 🔧 Setup

**Get API Key**: [DigitalOcean AI](https://cloud.digitalocean.com)  
**Add Extension**: Burp Suite → Extensions → Add → Select `burpaai.py`  
**Configure**: Enter API key in BurpAI tab → Save  
**Start**: Analyze requests or enable Auto-Analyze  

---

## 🐛 Found a Vulnerability?

### Security Reporting ⚠️

**Please DO NOT create a public GitHub issue for security vulnerabilities.**

Use one of these secure reporting methods:

#### Method 1: GitHub Security Advisory (Recommended)
1. Visit: [GitHub Security Advisory - Report](https://github.com/Stalin-143/BURP-AI/security/advisories/new)
2. Click **"Report a vulnerability"** button
3. Fill in the form with:
   - **Vulnerability Title**: Brief description
   - **Vulnerability Description**: Detailed explanation
   - **Steps to reproduce**: How to trigger the issue
   - **Impact**: Potential damage/risk
   - **CVSS Score**: If you have one
4. Submit privately to maintainers

#### Method 2: Private Email
- See [SECURITY.md](SECURITY.md#reporting-security-vulnerabilities) for maintainer contact

**Response Timeline:**
- 24-48 hours: Initial acknowledgment
- 7 days: Targeted fix or timeline provided
- 30 days: Security patch release

**Your privacy will be respected, and you'll be credited in the fix** 🙏

---

## 🎓 Example Scenarios

| Scenario | Action |
|----------|--------|
| Find SQLi vulnerabilities | Load request → Click "Analyze" → Review results |
| Custom analysis prompt | Use chat box to ask specific questions |
| Auto-analyze requests | Enable checkbox → Requests auto-analyzed when captured |
| Switch AI models | Change dropdown → New model selected immediately |

---

## ⚡ API Integration

**Endpoint**: `https://inference.do-ai.run/v1/chat/completions`  
**Models**: 11 AI models with automatic failover  
**Response Time**: < 15 seconds per analysis  
**Timeout Handling**: Automatic retry chain  

---

## 🏆 What Others Love

✅ Zero configuration complexity  
✅ Instant integration with existing workflow  
✅ Enterprise-grade AI models  
✅ No performance impact on Burp  
✅ Privacy-first architecture  

---

## 📖 Learn More

Dive into the detailed docs:
- [Installation & Setup](README.md#-quick-start) 
- [Security Guidelines](SECURITY.md)
- [Contribution Guide](COLLABORATION.md)
- [Release Notes](CHANGELOG.md)

---

<div align="center">

### Ready to analyze like a pro?

[⭐ Star on GitHub](https://github.com/Stalin-143/BURP-AI) • [📢 Report Issue](https://github.com/Stalin-143/BURP-AI/issues) • [💬 Discuss](https://github.com/Stalin-143/BURP-AI/discussions)

Built with ❤️ for the security community

</div>
