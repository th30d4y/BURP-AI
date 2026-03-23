# CHANGELOG

All notable changes to BurpAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0] - 2026-03-23

### ✨ Added

#### Core Features
- **AI-Powered Analysis:** Integration with multiple AI models (Kimi, DeepSeek, GLM, Qwen, LLaMA, Mistral, etc.)
- **Chat Interface:** Interactive chat display with message history and timestamps
- **HTTP Capture:** Real-time HTTP request/response capture via IHttpListener
- **Context Menu Integration:** Right-click "Send to BurpAI" functionality in Proxy, Repeater, and Target tabs
- **Native Repeater:** Built-in request/response editor using Burp's native message editors
- **History Table:** Complete request history with method, host, path, and status columns

#### Security & Configuration
- **API Key Management:** First-load dialog for API key configuration
- **Persistent Storage:** Secure configuration storage in `~/.burpaai/config.json`
- **Model Selection:** Dropdown to switch between 11 supported AI models
- **Auto-Analysis:** Optional automatic analysis checkbox for captured requests

#### UI/UX
- **Professional Dark Theme:** Dark mode interface matching Burp Suite aesthetics
- **Responsive Layout:** BorderLayout with horizontal/vertical split panels
- **Toolbar:** Compact toolbar with API key input, model selector, and status indicator
- **Split Panes:** Resizable panels for chat, history, and repeater sections

#### Technical
- **Threading:** Non-blocking async operations using Java threading
- **Error Handling:** Comprehensive try-catch blocks with detailed logging
- **Jython 2.7 Compatible:** Full compatibility with Jython 2.7 in Burp Suite
- **Memory Optimized:** Configurable history limit (default: 1000 entries)
- **Clean Imports:** Explicit Java/Swing imports without generic java. prefix

### 🔧 Fixed

- Fixed HTTP capture not triggering (IHttpListener properly registered)
- Fixed chat display null pointer exceptions
- Fixed Jython module caching issues with defensive getattr() wrappers
- Fixed API key loading on first run
- Fixed message editor initialization errors

### 📚 Documentation

- `README.md` - Comprehensive setup and usage guide
- `DISCLAIMER.md` - Legal notice and warranty disclaimer
- `SECURITY.md` - Security policy and vulnerability reporting
- `COLLABORATION.md` - Contribution guidelines
- `CHANGELOG.md` - This file

### 🔐 Security

- No known vulnerabilities at release
- All third-party dependencies reviewed
- HTTPS-only API communication
- Input validation and sanitization
- No telemetry or external tracking

### 📦 Dependencies

- Python 2.7+ (via Jython)
- Burp Suite API (IBurpExtender, ITab, IHttpListener, IContextMenuFactory)
- Java 8+ (Swing, AWT components)
- urllib2/urllib (HTTP requests)

### 🚀 Known Limitations

- Jython 2.7 limits some Python 3 features
- AI responses depend on selected model quality
- API rate limits apply (model/vendor specific)
- Local storage of chat history (not encrypted)
- Single API key per extension instance

### 🎯 Future Roadmap

- [ ] Multi-API support (rotate between providers)
- [ ] Encrypted local storage for chat history
- [ ] Export analysis reports (PDF, JSON)
- [ ] Custom prompt templates
- [ ] Multi-language support
- [ ] Machine learning for pattern recognition
- [ ] Integration with other Burp plugins
- [ ] Web UI alternative

### 💻 Installation

1. Download `burpaai.py`
2. In Burp Suite: Extensions → Add → Select file
3. On first load: Enter your AI API key
4. Start analyzing requests!

### 🙏 Contributors

Initial release developed with focus on:
- Production-grade code quality
- Jython 2.7 compatibility
- Professional UI/UX
- Security best practices
- Comprehensive documentation

---

## Versioning

- **1.0** (March 23, 2026) - Initial public release

### Semantic Versioning

- **MAJOR** (1.0.0): Breaking changes or major new features
- **MINOR** (1.0.0): New features, backward compatible
- **PATCH** (1.0.1): Bug fixes, no new features

### Release Schedule

- Security patches: As needed
- Minor updates: Every 2-4 weeks
- Major updates: As warranted by community feedback

---

## How to Report Issues

Found a bug? Please report it on [GitHub Issues](https://github.com/Stalin-143/BURP-AI/issues)

Include:
- BurpAI version
- Burp Suite version
- OS and Python version
- Steps to reproduce
- Error logs/stacktrace

## Security Updates

Security vulnerabilities should be reported privately. See [SECURITY.md](SECURITY.md) for details.

---

**Last Updated:** March 23, 2026  
**Current Stable Release:** 1.0
