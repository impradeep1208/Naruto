# 🔴 NARUTO – AI-Powered Cybersecurity Reconnaissance & Vulnerability Analysis System

> **Automating Recon → Analysis → Threat Intelligence → Reporting using Local AI**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask 2.3+](https://img.shields.io/badge/Flask-2.3%2B-green)](https://flask.palletsprojects.com/)
[![Ollama Integration](https://img.shields.io/badge/Ollama-Mistral%207B-orange)](https://ollama.ai/)
[![NVD API](https://img.shields.io/badge/NVD-API%202.0-red)](https://nvd.nist.gov/)
[![License](https://img.shields.io/badge/License-Educational%20Use-yellow)](LICENSE)

---

## ⚡ TL;DR

**NARUTO** is a **production-ready Flask-based cybersecurity platform** that integrates network scanning tools with a **locally hosted LLM (Ollama)** to automatically analyze results, identify vulnerabilities (CVEs), and generate **actionable security reports** in minutes.

👉 **Built to reduce manual effort in penetration testing workflows by 60-80%**

### Quick Demo
```bash
# 1. Enter target IP
# 2. Select scan type
# 3. Get AI analysis + CVE reports (all automated)
```

---

## 🚀 Why This Project?

### The Problem
Traditional security tools like **Nmap** provide raw technical output requiring **hours of manual interpretation**:
- Hundreds of lines of port/service data
- Manual CVE lookups needed
- No actionable insights
- Time-consuming report creation

### The Solution
**NARUTO** automates the entire pipeline:

| Traditional Workflow | NARUTO Workflow |
|-----|-----|
| Run Nmap | Run Nmap ✓ |
| Read 500 lines manually | AI analyzes automatically ✓ |
| Search each CVE manually | NVD API queries automatically ✓ |
| Create reports manually | Auto-generated reports ✓ |
| **⏱️ 2-3 hours** | **⏱️ 5 minutes** |

---

## 🧠 Key Highlights

* 🔎 **Multi-tool reconnaissance**: Nmap, Whois, Gobuster
* 🤖 **AI-powered analysis**: Local LLM (Ollama – Mistral 7B)
* 🌐 **Cross-system architecture**: Kali Linux ↔ Windows/Mac AI server
* 🎯 **Real-time CVE intelligence**: NVD API integration with CVSS scoring
* 📄 **Automated dual reports**: AI Analysis + Threat Intelligence
* 🎤 **Voice commands**: Natural language scan execution
* 🛡️ **Enterprise security**: Input validation, safe targets, timeout protection
* ⚡ **60-80% faster**: Optimized execution timeouts

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────┐
│      User (Browser Interface)       │
│  Dark Theme UI + Terminal Output    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Flask Backend (Kali Linux)       │
│  • Input Validation                 │
│  • Orchestration                    │
│  • Report Generation                │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────┐          ┌────▼──────┐
│ Scanning Engine    │ AI Analysis│
│ ├─ Nmap *          │ └─ Ollama  │
│ ├─ Whois           │   (Mistral)│
│ └─ Gobuster        │ (Windows)  │
└────┬────┘          └────▲───────┘
     │                    │
     └────────┬───────────┘
              │
     ┌────────▼────────┐
     │ Threat Intel    │
     │ NVD API v2.0    │
     │ CVE Mapping     │
     │ CVSS Scoring    │
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │ Report Gen      │
     │ ├─ AI Report    │
     │ └─ TI Report    │
     └─────────────────┘
```

---

## 🔄 Complete Workflow

```
Target Input (IP/Domain)
        ↓
Input Validation (Whitelist Check)
        ↓
Scan Execution (Nmap/Whois/Gobuster)
        ↓
AI Analysis (Ollama - Mistral LLM)
        ↓
Service Extraction (Version Detection)
        ↓
NVD API Query (Real-time CVEs)
        ↓
Severity Mapping (CVSS → Risk Levels)
        ↓
Report Generation (AI + TI Reports)
        ↓
Results Display + Download
```

### Step-by-Step Example

**Input:** User scans 192.168.1.1 with Service Detection

```
1. ✓ Validation: Is it a private IP? YES
2. ✓ Scan: Nmap -sV finds Apache 2.4.49, OpenSSH 4.7, vsftpd 2.3.4
3. ✓ AI: "Apache 2.4.49 is outdated with critical vulnerabilities..."
4. ✓ CVE Lookup: CVE-2021-41773 [CRITICAL] 9.8 CVSS
5. ✓ Report: AI analysis + full TI data with actionable recommendations
```

---

## 🤖 AI Integration (Core Innovation)

### Why Local LLM?
* **Privacy**: No cloud API = no data sent externally
* **Speed**: Local processing = instant responses
* **Cost**: No per-request charges
* **Offline**: Works without internet

### Architecture
```python
# Local Ollama running on Windows
POST http://<WINDOWS_IP>:11434/api/generate
{
    "model": "mistral",
    "prompt": "Analyze this Nmap output..."
}

Response: {"response": "This server has 3 critical issues..."}
```

### What AI Does
✓ Converts technical Nmap output → human-readable insights  
✓ Identifies suspicious findings → security concerns  
✓ Ranks threats by severity  
✓ Recommends mitigation steps

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | Dark Jarvis UI + Real-time updates |
| **Backend** | Python 3.13, Flask 2.3.2 | API routing, orchestration |
| **Scanning** | Nmap 7.95, Whois, Gobuster | Network reconnaissance |
| **AI Engine** | Ollama (Mistral 7B) | NLP analysis & insights |
| **Threat Intel** | NVD API v2.0 | Real-time CVE data |
| **Storage** | SQLite, File system | Reports & data persistence |

---

## 🔐 Environment Configuration

### Setup .env File

```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env
```

### .env Variables
```env
# Ollama Server (your machine IP)
OLLAMA_URL=http://YOUR_MACHINE_IP:11434
OLLAMA_API_KEY=  # Optional if Ollama requires auth

# Flask Settings
FLASK_ENV=production
FLASK_DEBUG=False
```

### Finding Your Machine IP

**Windows:**
```cmd
ipconfig → Look for "IPv4 Address"
```

**Mac/Linux:**
```bash
hostname -I
```

---

## 📊 Performance Benchmarks

| Metric | Baseline (v1) | Optimized (Current) | Improvement |
|--------|---------------|-------------------|-------------|
| Scan Execution | 60-180s | 60-180s | — |
| AI Analysis | 180-420s | 30-120s | **60-80% faster** |
| Full Pipeline | 4-17 min | 4-5 min | **70% faster** |
| Report Generation | ~5s | ~2s | **60% faster** |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Nmap, Whois, Gobuster (installed on system)
- Ollama (running on local/remote machine)
- pip package manager

### Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/impradeep1208/Naruto.git
cd Naruto

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Add your Ollama server IP
```

### Run Ollama (on Windows/Mac/Linux)

```bash
# Latest version
ollama pull mistral
ollama run mistral

# Ollama listens on http://localhost:11434
# (or your machine IP for remote access)
```

### Start NARUTO (on Kali Linux)

```bash
# Activate virtual environment
source venv/bin/activate

# Start Flask server
python3 app.py

# Open in browser
http://localhost:5000
```

### First Scan

```
1. Enter Target: 192.168.1.100
2. Select Tool: Nmap
3. Select Scan Type: Service Detection
4. Click: Execute Scan
5. Wait: 4-5 minutes
6. Download: AI + TI Reports
```

---

## ⏱️ Execution Timeline

| Stage | Duration | What Happens |
|-------|----------|--------------|
| Validation | ~1s | Input safety checks |
| Scan | 1-3 min | Port/service scanning |
| AI Analysis | 30-60s | Ollama generates insights |
| CVE Lookup | ~1 min | NVD API queries |
| Report Gen | ~2s | File generation |
| **Total** | **4-5 min** | **Complete analysis** |

---

## 🛡️ Security Features

### Input Protection
* ✅ Target IP validation (format + range)
* ✅ Private IP enforcement (192.168.x.x, 10.x.x.x)
* ✅ Domain whitelist for global scans
* ✅ Command injection prevention (no shell access)

### Execution Safety
* ✅ Timeout handling (prevents runaway processes)
* ✅ Subprocess isolation (safe command execution)
* ✅ Error handling (graceful failures)
* ✅ Logging (audit trail)

### Data Protection
* ✅ `.env` excluded from Git (sensitive data safe)
* ✅ Reports stored locally
* ✅ No external data transmission (except NVD API)

---

## 📈 Scan Types Explained

### Nmap Scans

**Basic Scan** (30s)
- Common ports only
- Quick reconnaissance
- Minimal network load

**Service Detection** (1-3 min) ⭐ RECOMMENDED
- All ports + services + versions
- Best for vulnerability mapping
- Balanced speed/depth

**Aggressive Scan** (5-10 min)
- All 65,535 ports + OS detection
- Comprehensive analysis
- Higher network load

**Custom Ports** (User-defined)
- Specify exact ports: `22,80,443` or `1-1000`
- Targeted scanning
- Time varies

### Whois Lookup
- Domain registration info
- Owner details
- Registrar info

### Gobuster
- Hidden directories
- Web path enumeration
- API endpoint discovery

---

## 📂 Project Structure

```
naruto/
├── app.py                          # Flask main application
├── config.py                       # Configuration & settings
├── executor.py                     # Safe tool execution
├── validator.py                    # Input validation
├── ai_analyzer.py                  # Ollama integration
├── threat_intelligence.py          # NVD API & CVE lookup
├── report_generator.py             # Report creation
├── requirements.txt                # Python dependencies
├── .env.example                    # Configuration template
├── .gitignore                      # Git security rules
├── README.md                       # Documentation
│
├── templates/
│   └── index.html                  # Web UI
├── static/
│   ├── script.js                   # Frontend logic
│   └── style.css                   # Dark theme styling
├── reports/                        # Generated report files
└── NARUTO_SIMPLIFIED_GUIDE.md      # User guide
```

---

## 🎯 Use Cases

| Use Case | Benefit |
|----------|---------|
| **Penetration Testing** | Automated recon + analysis |
| **Cybersecurity Learning** | See real CVEs + CVSS scoring |
| **Network Audits** | Quick vulnerability assessment |
| **Security Interviews** | Impress with automation skills |
| **Lab Testing** | Safe, isolated environment |

---

## 🔮 Future Enhancements

* 🔄 Multi-target batching (scan 100+ IPs)
* 📊 Dashboard analytics (trends, history)
* 🌐 Burp Suite integration
* ☁️ Cloud deployment (Docker support)
* 📱 Mobile app
* 🔐 Authentication layer
* 💾 Database integration (PostgreSQL)
* 📧 Email report delivery

---

## 🚨 Troubleshooting

### Ollama Connection Error
```
Error: Connection refused (http://YOUR_IP:11434)
```
**Solution:**
1. Ensure Ollama is running: `ollama run mistral`
2. Check firewall allows port 11434
3. Verify `.env` has correct IP address

### Nmap Not Found
```bash
# Ubuntu/Debian
sudo apt-get install nmap

# macOS
brew install nmap

# Windows: Download from https://nmap.org/download.html
```

### Reports Not Generating
1. Verify `./reports/` directory exists
2. Check write permissions: `chmod 755 reports/`
3. Ensure sufficient disk space

---

## 👨‍💻 Author

**Pradeep P**

- 🔴 Red Team Security Specialist
- 🤖 AI/ML Integration Engineer
- 🐍 Python Developer
- GitHub: [@impradeep1208](https://github.com/impradeep1208)

---

## 📞 Support

| Issue | Solution |
|-------|----------|
| API Not responding | Check Ollama running |
| Scan timeout | Reduce port range or increase timeout |
| NVD API slow | Check internet connection |
| Reports not saving | Verify disk space & permissions |

📖 See **NARUTO_SIMPLIFIED_GUIDE.md** for detailed workflow explanation

---

## ⚖️ Legal & Disclaimer

⚠️ **IMPORTANT**: This tool is for:
- ✅ Educational purposes only
- ✅ Authorized security testing (with permission)
- ✅ Lab/controlled environments

❌ **NOT for:**
- ❌ Unauthorized network scanning
- ❌ Illegal security testing
- ❌ Malicious purposes

**User assumes all responsibility for misuse.**

---

## ⭐ Support This Project

If NARUTO helped you:
1. **Star** ⭐ this repository
2. **Share** with your cybersecurity team
3. **Contribute** improvements via pull requests
4. **Cite** in your resume/portfolio

---

## 📄 License

This project is provided for **educational and authorized security testing purposes**.

---

## 🔥 Next Steps

1. ✅ Clone repository
2. ✅ Setup `.env` file
3. ✅ Run Ollama on your machine
4. ✅ Start Flask server
5. ✅ Open `http://localhost:5000`
6. ✅ Run your first scan!

---

<div align="center">

### 🚀 Ready to automate your security workflow?

[Get Started](#getting-started) | [Read Guide](NARUTO_SIMPLIFIED_GUIDE.md) | [Report Issue](https://github.com/impradeep1208/Naruto/issues)

**Built with ❤️ for the cybersecurity community**

</div>
