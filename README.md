# 🔴 NARUTO - Red Team Security Scanner

A powerful **web-based reconnaissance and vulnerability scanning tool** with AI analysis and threat intelligence integration. Scan networks, identify services, and analyze security vulnerabilities with automated reports.

## ✨ Features

✅ **Multiple Scanning Tools**
- **Nmap**: Port scanning with service detection
- **Whois**: Domain registration information
- **Gobuster**: Web directory and file discovery

✅ **AI-Powered Analysis**
- Ollama integration (Mistral 7B model)
- Intelligent security insights
- Natural language threat assessment

✅ **Threat Intelligence**
- NVD (National Vulnerability Database) integration
- CVE lookup and CVSS scoring
- Vulnerability severity assessment
- Actionable risk recommendations

✅ **Dual Report Generation**
- AI Analysis Reports
- Threat Intelligence Reports
- Download with one click

✅ **Advanced Features**
- Voice command support (speech recognition)
- Custom port scanning
- Input validation & safety checks
- Timeout protection
- Formatted terminal output

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Nmap** (installed on system)
- **Whois** (installed on system)
- **Gobuster** (installed on system)
- **Ollama** (running on local or remote machine)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/naruto.git
cd naruto

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env and add your Ollama server IP address
nano .env
```

### Configuration (.env file)

Create a `.env` file in the project root and configure your Ollama server:

```env
# Ollama server URL (replace with your machine IP)
OLLAMA_URL=http://YOUR_MACHINE_IP:11434
OLLAMA_API_KEY=

# Flask settings
FLASK_ENV=production
FLASK_DEBUG=False
```

**Finding your machine IP:**
- **Windows**: Open Command Prompt → `ipconfig` → Look for IPv4 Address
- **Mac/Linux**: Open Terminal → `hostname -I` or `ifconfig`

### Running the Application

```bash
# Start Flask server
python3 app.py

# Open in browser
http://127.0.0.1:5000
```

---

## 📊 How It Works

### Complete Workflow

```
User Input
    ↓
Frontend Validation
    ↓
Backend Processing
    ├─ Input Validation
    ├─ Tool Execution (Nmap/Whois/Gobuster)
    ├─ AI Analysis (Ollama Mistral 7B)
    └─ Threat Intelligence (NVD API)
    ↓
Report Generation
    ├─ AI Analysis Report
    └─ Threat Intelligence Report
    ↓
Display Results & Download
```

### Typical Scan Timeline

| Time | Component |
|------|-----------|
| 0-10s | Input validation |
| 10-180s | Tool execution (Nmap/Whois/Gobuster) |
| 180-240s | AI analysis (Ollama) |
| 240-300s | Threat intelligence lookup (NVD) |
| 300-310s | Report generation |
| 310s+ | Display & download |

**Total: ~5-10 minutes** (depending on scan type)

---

## 🎯 Scan Types Explained

### **Nmap Scans**

1. **Basic Scan**
   - Quick scan of common ports
   - Time: ~30 seconds
   - Use: Quick reconnaissance

2. **Service Detection**
   - Identifies services and versions
   - Time: ~1-3 minutes
   - Use: Service discovery (RECOMMENDED)

3. **Aggressive Scan**
   - Deep scan of all 65535 ports
   - Time: ~5-10 minutes
   - Use: Comprehensive analysis

4. **Custom Ports**
   - User-specified port ranges
   - Examples: `22`, `1-1000`, `22,80,443`
   - Time: Varies
   - Use: Specific port targeting

### **Whois Lookups**
- Gets domain registration info
- Domain owner details
- Registrar information

### **Gobuster Scanning**
- Finds hidden directories
- Web path discovery
- API endpoint detection

---

## 🛡️ Security Features

✅ **Input Validation** - Prevents malicious inputs
✅ **IP Whitelisting** - Only private IPs (192.168.x.x, 10.x.x.x)
✅ **Safe Command Execution** - No shell injection vulnerabilities
✅ **Timeout Protection** - Prevents runaway processes
✅ **Error Handling** - Graceful failure modes

---

## 📁 Project Structure

```
naruto/
├── app.py                      # Flask backend
├── config.py                   # Configuration & settings
├── executor.py                 # Tool execution (safe)
├── validator.py               # Input validation
├── ai_analyzer.py             # Ollama AI integration
├── threat_intelligence.py      # NVD API integration
├── report_generator.py        # Report file generation
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
├── templates/                # HTML templates
│   └── index.html            # Main UI
├── static/                   # Static files
│   ├── script.js             # Frontend JavaScript
│   └── style.css             # Dark theme styling
└── reports/                  # Generated reports (git ignored)
```

---

## 🔧 Configuration Options

All configuration is in `config.py`. To customize, edit the settings:

```python
# Scan timeouts (seconds)
AI_ANALYSIS_TIMEOUTS = {
    "basic": 30,
    "service_detection": 60,
    "aggressive": 90,
    "custom_ports": 120
}

# Allowed tools
ALLOWED_TOOLS = ["nmap", "whois", "gobuster"]

# Whitelisted domains
WHITELISTED_DOMAINS = [
    "example.com",
    "test.local"
]

# Whitelisted private IPs
ALLOWED_PRIVATE_IPS = [
    "192.168.0.0/16",
    "10.0.0.0/8",
    "172.16.0.0/12"
]
```

---

## 📝 API Endpoints

### POST /api/scan
Execute a scan with the specified parameters.

**Request:**
```json
{
  "target": "192.168.1.1",
  "tool": "nmap",
  "scan_type": "service_detection",
  "port_range": ""
}
```

**Response:**
```json
{
  "status": "success",
  "execution": {"stdout": "..."},
  "analysis": {"status": "success", "analysis": "..."},
  "threat_intelligence": {"status": "success", "threat_data": [...]},
  "report_filename": "naruto_report_...",
  "ti_report_filename": "naruto_ti_report_..."
}
```

### GET /api/download-report/<filename>
Download a generated report file.

### POST /api/parse-command
Parse natural language voice/text command.

**Request:**
```json
{"command": "scan 192.168.1.1 with nmap aggressive"}
```

---

## 🐛 Troubleshooting

### Ollama Connection Error
```
Error: Connection refused (http://YOUR_MACHINE_IP:11434)
```
**Solution:**
1. Ensure Ollama is running on the specified IP
2. Check firewall allows traffic on port 11434
3. Verify IP in `.env` file matches your actual machine IP
4. Check `.env` file location and permissions

### Nmap Not Found
```
Error: nmap command not found
```
**Solution:**
```bash
# Install Nmap
# On Ubuntu/Debian:
sudo apt-get install nmap

# On Mac:
brew install nmap

# On Windows:
# Download from https://nmap.org/download.html
```

### Reports Not Generating
1. Check `./reports/` directory exists
2. Verify write permissions: `chmod 755 reports/`
3. Check disk space availability

---

## 🚀 Deployment

### Local Deployment
```bash
python3 app.py
```

### Production Deployment (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Support (Optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## 📊 Example Scan Output

### Terminal Display
```
✅ Execution Output
   PORT      STATE    SERVICE VERSION
   21/tcp    open     ftp     vsftpd 2.3.4
   22/tcp    open     ssh     OpenSSH 4.7p1
   80/tcp    open     http    Apache 2.2.8

✅ AI Analysis
   "FTP service (vsftpd 2.3.4) is outdated with known backdoor 
    vulnerability. SSH version 4.7 is also outdated. Apache 2.2.8 
    has unpatched security issues."

✅ Threat Intelligence
   Services: 3
   Vulnerabilities: 7
   Critical Issues: 1
   High Severity: 2
   Medium Severity: 4
```

---

## 🔐 Privacy & Security

⚠️ **Important:**
- `.env` file contains sensitive IP addresses - NEVER commit to GitHub
- Use `.gitignore` to exclude `.env` automatically
- Share `.env.example` with teammates instead
- Always validate targets before scanning

---

## 📚 Dependencies

See `requirements.txt` for all Python packages:
- Flask 2.3.2
- Requests 2.31.0
- Other security and scanning integrations

---

## 🎓 Use Cases

✅ **Penetration Testing** - Authorized security assessments
✅ **Network Reconnaissance** - Authorized network mapping
✅ **Vulnerability Scanning** - Find exposures in your infrastructure
✅ **Security Audits** - Compliance and risk assessment
✅ **Learning** - Educational security tool

---

## ⚖️ Legal Disclaimer

**NARUTO is for authorized security testing only.**

- Only scan networks/systems you own or have explicit permission to test
- Unauthorized network scanning may violate laws
- User assumes all responsibility for illegal use
- Developers are not liable for misuse

---

## 📞 Support

- Check documentation in `NARUTO_SIMPLIFIED_GUIDE.md`
- Review troubleshooting section above
- Check configuration in `config.py`

---

## 📄 License

This project is provided as-is for educational and authorized security testing purposes.

---

## 🙏 Acknowledgments

- **Nmap** - Network scanning tool
- **NVD** - Vulnerability database
- **Ollama** - Local AI inference
- **Mistral** - LLM model

---

## 🚀 What's Next?

1. Setup `.env` file with your Ollama IP
2. Run the application
3. Open http://127.0.0.1:5000
4. Start scanning!

**Happy Red Teaming! 🔴**
