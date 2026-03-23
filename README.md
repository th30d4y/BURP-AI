# 🤖 BurpAI

**AI-Powered Vulnerability Analysis for Burp Suite**

[![v1.0](https://img.shields.io/badge/Version-1.0-blue)](https://github.com/Stalin-143/BURP-AI/releases)
[![Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)
[![Production](https://img.shields.io/badge/Status-Production%20Ready-success)](SECURITY_ADVISORY.md)

🌐 [Website](https://stalin-143.github.io/BURP-AI/) • 📖 [Security](SECURITY.md) • 🐛 [Issues](https://github.com/Stalin-143/BURP-AI/issues)

---

## What is BurpAI?

BurpAI integrates multi-model AI directly into Burp Suite for intelligent vulnerability detection. Analyze HTTP requests in real-time and get actionable security insights instantly.

---

## ✨ Features

- **🧠 Multi-Model AI** - 11 models with automatic failover
- **⚡ Real-time Analysis** - Zero UI lag, background threading
- **🔍 Smart Detection** - RCE, IDOR, SQLi, Auth bypass, XSS, and more
- **📋 Native Repeater** - Built-in request/response editing
- **📊 Request History** - Tracks 1000+ requests automatically
- **💬 Interactive Chat** - Ask custom security questions

---

## 🚀 Quick Start

```bash
# 1. Get DigitalOcean AI API key
# https://cloud.digitalocean.com

# 2. Load in Burp Suite
# Extensions → Add → Select burpaai.py

# 3. Configure API key in BurpAI tab → Save

# 4. Analyze requests
# Load any request → Click "Analyze with AI"
```

---

## 📋 Requirements

| Item | Details |
|------|---------|
| Burp Suite | Pro or Community (latest) |
| API Key | DigitalOcean AI |
| Java | 8+ (included with Burp) |
| Network | HTTPS outbound |

---

## 🧠 Supported Models

- Alibaba Qwen 3 (32B)
- DeepSeek R1 (70B)
- GLM-5
- Kimi K2.5
- LLaMA 3 & 3.3 (8B-70B)
- Mistral Nemo (2407)
- NVIDIA Nemotron (120B)
- OpenAI GPT OSS (20B-120B)

---

## 🛡️ Security & Privacy

✅ HTTPS-only API calls  
✅ No telemetry or tracking  
✅ Local-only data storage  
✅ User-managed API keys  
✅ Open-source codebase  

### Report Security Vulnerabilities

**⚠️ DO NOT** open public issues for security vulnerabilities.

Use [GitHub Security Advisory](https://github.com/Stalin-143/BURP-AI/security/advisories):
1. Click "Report a vulnerability"
2. Provide details privately
3. Maintainers respond within 24-48 hours

---

## 📚 Documentation

- [Security Policy](SECURITY.md)
- [Contributing Guide](COLLABORATION.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE)
- [Disclaimer](DISCLAIMER.md)

---

## 📥 Download

[Download v1.0](https://github.com/Stalin-143/BURP-AI/releases/tag/v1.0) • [GitHub](https://github.com/Stalin-143/BURP-AI) • [Issues](https://github.com/Stalin-143/BURP-AI/issues)

---

**License:** Apache 2.0 | **Status:** Production Ready | **For authorized security testing only**
