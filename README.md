<div align="center">

# 🤖 BurpAI

**AI-Powered Vulnerability Analysis for Burp Suite**

v1.0 • Apache 2.0 • Production

[![Self-Hosted Git](https://img.shields.io/badge/Self--Hosted-Gitea-green?style=flat-square\&logo=gitea\&logoColor=white)](https://git.w4nn4d13.tech/0x5t4l1n/BURP-AI)

[🌐 Website](https://stalin-143.github.io/BURP-AI/) • [📖 Security](SECURITY.md) • [🐛 Issues](https://github.com/Stalin-143/BURP-AI/issues)

</div>


---

## Overview

BurpAI integrates advanced AI directly into Burp Suite to automate vulnerability detection and security analysis. Analyze HTTP requests in real-time with 11+ AI models, get intelligent insights, and collaborate with AI to find hidden vulnerabilities faster.

**Key Features:**
- 🧠 Multi-model AI engine with automatic fallback
- ⚡ Zero-lag background processing
- 🔍 Detects RCE, IDOR, SQLi, XSS, Auth bypass, and more
- 💬 Interactive chat for custom security questions
- 📊 Native request history and repeater
- 🎯 One-click vulnerability analysis

---

## Installation

### Prerequisites

- **Burp Suite** (Pro or Community Edition)
- **Python 2.7+** (Jython runtime, included with Burp)
- **API Key** from [DigitalOcean AI](https://cloud.digitalocean.com) or compatible provider
- **Java 8+** (bundled with Burp Suite)

### Setup Steps

1. **Download Extension**
   ```bash
   git clone https://github.com/Stalin-143/BURP-AI.git
   cd BURP-AI
   ```

2. **Load in Burp Suite**
   - Open Burp Suite
   - Go to **Extensions** → **Installed** → **Add**
   - Select `burpaai.py`
   - Confirm and wait for initialization

3. **Configure API Key**
   - Click **BurpAI** tab in main window
   - Enter your DigitalOcean API key
   - Click **Save**
   - Status should show "Connected"

4. **Verify Installation**
   - Select any HTTP request
   - Right-click → **Send to BurpAI** (or click **Analyze with AI**)
   - AI response appears in chat panel

---

## Quick Usage

| Action | Method |
|--------|--------|
| **Analyze Request** | Select request → Click "Analyze with AI" |
| **Send to AI** | Right-click request → "Send to BurpAI" |
| **Chat With AI** | Type in input → Press ENTER or click Send |
| **Switch Model** | Select from Model dropdown → Auto-updates |
| **View History** | Click request in history table |

---

## Documentation

- [Security Policy](SECURITY.md)
- [Security Advisory](SECURITY_ADVISORY.md)
- [Contributing](COLLABORATION.md)
- [License](LICENSE)

---

**Status:** Production Ready | **For authorized security testing only**

