# BurpAI - AI-Powered Security Analysis for Burp Suite

A professional Burp Suite extension that leverages multi-model AI to identify vulnerabilities in HTTP requests and provide actionable test payloads for authorized security research and penetration testing.

## Overview

BurpAI is designed for security researchers and penetration testers who need intelligent vulnerability analysis integrated directly into their Burp Suite workflow. It combines enterprise-grade AI models with expert security knowledge to deliver precise, actionable security insights.

**Key Capability**: Analyzes HTTP requests/responses from your Burp environment and classifies vulnerabilities by severity with practical test payloads.

---

## Features

### Core Analysis
- **Multi-Model AI Engine**: 11 fallback models with automatic switching
- **P1 Focus**: Prioritizes critical vulnerabilities (RCE, IDOR, SSRF, SQLi, Auth bypass)
- **Automatic Severity Classification**: CRITICAL → HIGH → MEDIUM → LOW
- **Structured Output**: Organized vulnerability reports with payloads

### Integration
- **Native Burp Repeater Panel**: Full request/response editing in native Burp UI
- **Request History**: Tracks up to 1000 requests with automatic cleanup
- **Auto-Analyze Mode**: Optional automatic analysis on send
- **Model Selection**: User-selectable AI model with automatic fallback

### Performance
- **Background Threading**: Non-blocking analysis (no UI freeze)
- **Custom Prompts**: Chat interface for custom analysis prompts
- **API Fallback**: Automatic retry chain across 11 models
- **Timeout Handling**: 15-second per-model limits

---

## Installation

### Prerequisites
- Burp Suite (Pro or Community Edition)
- DigitalOcean AI API key (from inference.do-ai.run)
- Python 2.7+ (Jython)

### Quick Start

**1. Load Extension in Burp:**
```
Extensions → Add → Select burpaai.py → Load
```

**2. Configure API Key:**
- Click BurpAI tab → Enter DigitalOcean API key → Save

**3. Start Analyzing:**
- Load any request in Repeater
- Click "Analyze with AI"
- View results in chat panel

---

## Usage Guide

### Analyzing Requests

**Manual Analysis:**
1. Open any request in Burp Repeater
2. Click **"Analyze with AI"** button
3. Select model (or use auto-fallback)
4. Review structured vulnerability report

**Example Output:**
```
[VULNERABILITIES]
- SQL Injection (CRITICAL)
- IDOR (HIGH)

[ATTACK VECTORS]
- user_id parameter in /api/profile

[TEST PAYLOADS]
' OR 1=1--
admin_id=999

[EXPLOITATION STEPS]
- Modify user_id parameter
- Observe unauthorized data access
```

### Auto-Analyze Mode

1. Enable **"Auto Analyze"** checkbox
2. Click **"Send Request"**
3. Analysis runs automatically when response loads

### Custom Prompts

Use the chat input field to ask custom security questions about the current request/response context.

---

## Supported Vulnerabilities

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

## Architecture

### Main Components

| Component | Purpose |
|-----------|---------|
| `burpaai.py` | Extension main class & UI |
| `analyze_with_ai()` | Vulnerability analysis trigger |
| `call_ai()` | Multi-model API management |
| `_parse_vulnerability_response()` | Response structuring |
| `_classify_vulnerability_severity()` | Severity mapping |
| `_format_vulnerability_output()` | Professional formatting |

### UI Elements

- **Request/Response Editors**: Native Burp message editors
- **Chat Display**: Analysis results and custom prompts
- **Model Dropdown**: AI model selection
- **Control Buttons**: Analyze, Send, API Config
- **Auto-Analyze Checkbox**: Enable automatic analysis

---

## API Configuration

**Endpoint**: `https://inference.do-ai.run/v1/chat/completions`

**Authentication**: Bearer token (DigitalOcean API key)

**Parameters**: 
- model: Selected AI model
- messages: User prompt + request context
- max_tokens: 400 per request

---

## Performance & Optimization

- **History Limit**: 1000 entries (automatic FIFO cleanup)
- **Response Timeout**: 15 seconds per model attempt
- **Threading**: Background threads for non-blocking analysis
- **Memory Management**: Automatic history pruning

---

## Security & Ethics

**Authorized Testing Only**
- Use only on systems you own or have explicit written permission to test
- Verify scope before analysis (user controls what gets analyzed)
- Comply with all applicable laws and regulations
- Practice responsible disclosure

The extension operates within your Burp environment—you decide what requests to analyze and what targets to test.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No response from AI | Verify API key, check internet, fallback attempts all models |
| Empty analysis | Check request format, try a simple GET request |
| Auto-analyze not triggering | Enable checkbox, use "Send Request", verify response loads |
| Timeout errors | Some models are slower; fallback chain will retry |

---

## File Structure

```
burpaai.py          Main extension (1378 lines)
requirements.txt    Dependencies
README.md          This documentation
```

---

## Version History

- **v2.0** (March 2026): Production enhancement - multi-model fallback, structured parsing, severity classification
- **Earlier versions**: Initial development and fixes

---

## Support

For issues:
1. Check API key configuration
2. Review Burp console for error logs
3. Test with a simple HTTP request
4. Verify internet connectivity

---

**Status**: ✅ Production Ready | **License**: Authorized Use | **Updated**: March 2026
| AI ON/OFF | ON (Green) | Enable/disable automatic analysis |
| Headers ON/OFF | OFF (Orange) | Enable/disable bypass header injection |
| API Config | - | Open API configuration dialog |
| Analyze All | - | Manually trigger analysis |
| Export | - | Export findings to file |
| Clear | - | Clear all data |

---

## 📊 UI Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Mode ▼ │ AI: ON │ Headers: OFF │ Model: gpt-4 │ [API Config]  │ (Toolbar)
├──────────────┬──────────────────────────────────────────────┤
│              │ [Requests] [Raw] [Response]                  │
│  Request     ├──────────────────────────────────────────────┤
│  Table       │  [Viewer Panel - Details]                    │
│              ├──────────────────────────────────────────────┤
│  #│Host│    │ 🤖 AI Chat Interface                          │
│  1│api │    │ [Chat History]                                │
│  2│web │    │ [Input: Type your question...]        [Send] │
│              ├──────────────────────────────────────────────┤
│              │ Security Findings                            │
│              │ [CRITICAL] SQLi - 90% (example.com)         │
│              │ [HIGH] XSS - 75% (api.endpoint)             │
│              │ [Det] [Test Payload]                         │
├──────────────┴──────────────────────────────────────────────┤
│ [+] Logs and Real-time Activity Feed                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 💬 Chat Commands

```
"Analyze this for XSS"         → Injects XSS payload & checks response
"Modify for SQLi"              → Adds SQL injection bypass syntax
"Check IDOR"                   → Changes ID parameters incrementally
"Add bypass headers"           → Injects X-Forwarded-For, etc.
"What vulnerabilities found?"  → Summarizes all findings
"Test this endpoint"           → Runs comprehensive security tests
```

---

## 🔍 Detected Vulnerabilities

### CRITICAL 🔴
- SQL Injection (SQLi)
- Remote Code Execution (RCE)

### HIGH 🟠  
- Cross-Site Scripting (XSS)
- Server-Side Template Injection (SSTI)
- Server-Side Request Forgery (SSRF)
- Insecure Direct Object Reference (IDOR)

### MEDIUM 🟡
- Cross-Site Request Forgery (CSRF)
- Missing Security Headers
- Weak Authentication

---

## 📋 Analysis Modes

### 🔄 Auto Mode
- Analyzes every HTTP request automatically
- Runs in background (non-blocking)
- Real-time findings in Findings panel
- Best for: Passive continuous testing

### 💬 Chat Mode
- Manual interaction with AI expert
- No automatic processing
- Ask targeted questions
- Best for: Focused exploration

### 🔀 Hybrid Mode
- Automatic background analysis
- Manual chat interaction
- Best of both worlds
- Best for: Comprehensive testing

---

## 🛠️ API Configuration Dialog

```
┌─────────────────────────────────────┐
│ API Configuration                   │
├─────────────────────────────────────┤
│ API Key:     [••••••••••••••••••]   │
│ Endpoint:    [https://api.openai..] │
│ AI Model:    [gpt-4 ▼]              │
│              Options:                │
│              - gpt-4 (Best)          │
│              - gpt-4-turbo           │
│              - claude-3-opus         │
│              - gemini-pro            │
├─────────────────────────────────────┤
│                        [Save] [Cancel]│
└─────────────────────────────────────┘
```

Supported Models:
- `gpt-4` - Most accurate, slower
- `gpt-4-turbo` - Fast, good quality
- `claude-3-opus` - Alternative, excellent
- `gemini-pro` - Alternative, reliable

---

## 🎯 Usage Examples

### Example 1: XSS Testing
```
1. Browse application normally
2. Requests auto-capture in Request Table
3. AI detects potential XSS in search parameters
4. Click found vulnerability in Findings panel
5. In chat: "Test this for XSS"
6. Click "Test Payload" to inject
7. Check response for reflected HTML
```

### Example 2: IDOR Vulnerability  
```
1. Access /user/profile?id=123
2. AI detects numeric ID parameter
3. In chat: "Check IDOR on this"
4. AI modifies request: /user/profile?id=124, 125, etc.
5. If you see other users' data → IDOR confirmed
```

### Example 3: SQLi Detection
```
1. Access page with db query parameter
2. AI auto-detects SQLi potential
3. Severity: CRITICAL, Confidence: 90%
4. Click "Deep Dive" for explanation
5. AI suggests: ' OR '1'='1 payload
6. Click "Test Payload" to inject
7. If database errors appear → SQLi confirmed
```

### Example 4: Authentication Bypass
```
1. Try to access /admin (get 403)
2. Toggle "Headers: ON"
3. Try again with bypass headers
4. AI injects: X-Forwarded-For, X-Original-URL
5. If access granted → Bypass successful
```

---

## ⚙️ Advanced Features

### Adaptive Fuzzing
AI generates smart payloads based on context:
- Reduces false positives
- Focuses on exploitable issues
- Mutates parameters intelligently

### Deep Context Analysis
- Tracks authentication flows
- Correlates multiple endpoints
- Detects business logic flaws
- Identifies privilege escalation

### Global Header Injection
Bypass techniques automatically injected:
```
X-Forwarded-For: 127.0.0.1
X-Original-URL: /admin
X-Rewrite-URL: /admin
X-HTTPMethodOverride: POST
```

### Session Memory
AI remembers conversation context:
- Learns from previous findings
- Adapts to user feedback
- Prioritizes user-selected targets

---

## 📊 Code Architecture

```
burpaai.py (118 lines)
├── Main extension class
├── HTTP listener integration
└── Threading for non-blocking

ai_handler.py (289 lines)
├── Vulnerability detection
├── Request modification
├── AI/LLM integration
└── Analysis engine

ui_panel.py (600+lines)
├── Professional UI build
├── Chat interface
├── Toolbar controls
├── API config dialog

request_modifier.py (161 lines)
├── Payload injection
├── Header manipulation
├── Fuzzing engine
└── Mutation utilities

scanner.py (288 lines)
├── Deep analysis
├── Pattern matching
├── Correlation engine
└── Recommendation system

utils.py (164 lines)
├── Logging
├── Data structures
├── Configuration
└── Helper functions

Total: ~1,988 lines of production code
```

---

## 🔒 Security & Privacy

✅ API keys never logged to console
✅ Sensitive data masking in UI
✅ No plaintext storage
✅ Optional header injection
✅ Configurable data retention

---

## 🐛 Troubleshooting

**Q: "No API key configured"**
- Click API Config button
- Enter valid API key
- Select model and save

**Q: Extension won't load**
- Check Extender → Errors
- Verify all .py files in same folder
- Reload extension

**Q: No vulnerabilities found**
- Enable AI ON button (check green)
- Browse more pages to capture traffic
- Try Chat mode for manual analysis

**Q: Buttons not working**
- Reload extension in Burp
- Check Extender → Logs
- Restart Burp Suite

---

## 📞 Support

- Check Extender → Errors tab
- Review logs in bottom panel
- Test with basic requests first
- Verify API connectivity

---

**BurpAI Ultra v3.0** - Production Ready ✅
Built for professional penetration testers and bug bounty hunters


### 🔍 **Automatic Traffic Analysis**
- Auto-captures all HTTP requests/responses flowing through Burp Suite
- Analyzes traffic for common web vulnerabilities
- Provides severity ratings (HIGH, MEDIUM, LOW)

### 🤖 **AI-Powered Vulnerability Detection**
- Uses DigitalOcean Inference API with 35+ models
- **Model Selection**: Choose from kimi-k2.5, Claude, GPT-4, Llama, and more
- Runtime model switching without restarting
- Detects multiple vulnerability types:
  - SQL Injection
  - Cross-Site Scripting (XSS)
  - Cross-Site Request Forgery (CSRF)
  - Command Injection
  - Path Traversal
  - XXE Injection
  - Authentication Issues
  - API Security Issues

### 🚀 **Active Testing**
- Two modes: **Manual Approval** and **Automatic**
- Tests identified vulnerabilities with appropriate payloads
- Confirms vulnerabilities through response analysis
- Requests are signed and tracked

### ⚙️ **Configurable Settings**
- Easy API key management with validation
- **Professional Dark UI**: Optimized for Kali Linux
- *Toggle auto-capture on/off*
- Select vulnerability analysis scope
- Choose active testing mode
- **Select AI model** from 35+ options
- Built-in result caching to reduce API calls
- API key format validation
- Real-time connection testing

### 📊 **Real-time Reporting**
- Live analysis results in UI
- Detailed vulnerability descriptions
- Recommendations for remediation
- Test confirmation status

## Installation

### Prerequisites
- **Burp Suite Professional** (Community Edition has limited Python support)
- **Python 3.7+** with `requests` library
- **DigitalOcean Account** with API access

### Step 1: Get DigitalOcean API Key

1. Go to [DigitalOcean Console](https://cloud.digitalocean.com)
2. Navigate to **API → Tokens → Model Access Keys**
3. Click **Create Key**
4. Name it "burp" or similar
5. **Copy and secure the key** (it won't be shown again)

⚠️ **SECURITY WARNING**: Never share your API key publicly!

### Step 2: Install Python Dependencies

```bash
cd /path/to/BurpAI
pip install -r requirements.txt
```

### Step 3: Load Extension in Burp Suite

1. Open **Burp Suite → Extensions → Installed Extenders**
2. Click **Add Error** or **Add** (depending on version)
3. Select **Extension type: Python**
4. Select **burpaai.py** as the extension file
5. Click **Load**

You should see the **BurpAI** tab appear in Burp Suite

### Step 4: Configure API Key

1. Go to the **BurpAI** tab in Burp Suite
2. Paste your DigitalOcean API key in the **API Key** field
3. Configure settings:
   - **Auto-Capture Traffic**: Enable to automatically analyze traffic
   - **Analysis Scope**: Choose vulnerability types (All Types recommended)
   - **Active Testing**: Select **Manual Approval** for safety
4. Click **Save Settings**

## Usage

### Basic Workflow

1. **Configure** your API key and settings
2. **Enable Auto-Capture** in the BurpAI tab
3. **Browse** websites normally through Burp proxy
4. **Review Results** in the BurpAI tab as vulnerabilities are identified
5. **Approve Testing** for HIGH severity vulnerabilities (if using Manual Approval mode)

### Manual Analysis

1. In the BurpAI tab, click **Analyze Selected**
2. Analyzes the last 10 captured requests
3. Results appear in real-time

### Interpreting Results

```
🔴 [HIGH]    SQL Injection
    → SQL injection detected in login parameter
    
🟠 [MEDIUM]  Cross-Site Scripting
    → User input not properly sanitized
    
🟡 [LOW]     Information Disclosure
    → Server version leaking in headers
```

Color coding:
- 🔴 **RED (HIGH)**: Critical vulnerability, requires immediate fix
- 🟠 **ORANGE (MEDIUM)**: Should be fixed soon
- 🟡 **YELLOW (LOW)**: Low risk, fix when possible

### Active Testing

**Manual Approval Mode** (Recommended):
- Suspicious vulnerabilities require your approval
- Click **Test** button to send exploit payloads
- Results shown in the UI

**Automatic Mode**:
- Extension automatically tests HIGH severity vulnerabilities
- Results logged and displayed
- Use with caution!

## Architecture

```
burpaai.py                 - Main extension interface
├── vulnerability_analyzer.py  - AI analysis engine
├── active_tester.py          - Payload injection & testing
└── config.py                 - Configuration management
```

### Data Flow

```
HTTP Request/Response
    ↓
[Captured by Burp]
    ↓
[BurpAI Listener]
    ↓
[Extracted Details]
    ↓
[Sent to DigitalOcean API]
    ↓
[AI Analysis]
    ↓
[Parse Results]
    ↓
[Display in UI]
    ↓
[Optional: Active Testing]
```

## API Integration

### DigitalOcean Inference API (v2.0)

**Endpoint**: `https://inference.do-ai.run/v1/chat/completions`

**Supported Models** (35+ available):
- kimi-k2.5 (Recommended for security)
- anthropic-claude-4.6-sonnet
- anthropic-claude-opus-4.6
- openai-gpt-4o, openai-gpt-4o-mini
- alibaba-qwen3-32b
- llama3.3-70b-instruct
- And 28+ more...

**Request Format** (Chat Completions):
```json
{
    "model": "kimi-k2.5",
    "messages": [
        {"role": "system", "content": "You are a security analyst..."},
        {"role": "user", "content": "Analyze this traffic..."}
    ],
    "max_tokens": 1500,
    "temperature": 0.7
}
```

**Response Format**:
```json
{
    "choices": [{
        "message": {
            "content": "{\"vulnerabilities\": [...], \"summary\": \"...\"}"
        }
    }]
}
```

## Performance Considerations

- **Rate Limiting**: 1 second delay between API calls (configurable)
- **Caching**: Results cached by URL to reduce API usage
- **Batch Analysis**: Analyzes in batches of 5-10 requests
- **Timeout**: 15 second timeout per API request

## Configuration File

Settings saved to `~/.burpaai/config.json`:

```json
{
  "api_key": "sk-do-...",
  "auto_capture": true,
  "scope": "All Types",
  "testing_mode": "Manual Approval",
  "max_requests_to_analyze": 50,
  "cache_timeout": 3600,
  "enable_logging": true,
  "auto_analyze_threshold": 5
}
```

## Troubleshooting

### "API Key not configured"
- Go to BurpAI tab
- Enter your DigitalOcean API key
- Click Save Settings

### "API request timeout"
- Check your internet connection
- Verify DigitalOcean API key is valid
- Try again (API might be temporarily slow)

### "No requests to analyze"
- Enable **Auto-Capture Traffic** in BurpAI tab
- Make sure Burp is configured as proxy
- Browse some sites to generate traffic

### Extension won't load
- Ensure Python 3.7+ is installed
- Run `pip install requests` manually
- Check Burp Suite's Python path configuration

### "Invalid JSON response"
- DigitalOcean API returned unexpected format
- Check your API key validity
- Check your internet connection

## Security Notes

⚠️ **Important Security Reminders**:

1. **API Key Security**:
   - Never commit API keys to version control
   - Store in secure password manager
   - Rotate keys regularly
   - Restrict key permissions in DigitalOcean console

2. **Active Testing**:
   - Only test on authorized systems
   - Only use on systems you own or have permission to test
   - Always use Manual Approval mode for production systems
   - Understand payload implications before testing

3. **Data Privacy**:
   - HTTP request/response data is sent to DigitalOcean for analysis
   - Ensure no sensitive data (passwords, tokens) in traffic
   - Review what's being sent before enabling auto-capture

4. **Burp Configuration**:
   - Use HTTPS interception carefully
   - Ensure only authorized traffic is captured
   - Consider segmented proxy settings per scope

## Limitations

- Python support varies by Burp Suite version
- Large response bodies are truncated to 500 characters
- Active testing uses basic payload injection (not context-aware)
- Cache disabled after 1 hour by default
- Rate limited by DigitalOcean API quotas

## Future Enhancements

- [ ] Custom vulnerability detection rules
- [ ] Integration with other threat intelligence APIs
- [ ] Advanced payload generation for specific frameworks
- [ ] Automated remediation suggestions
- [ ] Export reports in multiple formats (PDF, JSON, HTML)
- [ ] Webhook integration for CI/CD pipelines
- [ ] Machine learning model for false positive reduction

## Support & Contact

For issues, features requests, or security concerns:
1. Check the Troubleshooting section above
2. Review DigitalOcean Gradient API documentation
3. Check Burp Suite extension compatibility

## License

This extension is provided as-is for educational and authorized security testing purposes.

## Disclaimer

This tool is intended for authorized security testing only. Unauthorized testing of systems you don't own or have permission to test is illegal. The authors are not responsible for any misuse of this tool.

---

**Happy Hunting! 🎯**
