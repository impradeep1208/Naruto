# 🔴 NARUTO - Simplified Complete Workflow

## What is NARUTO?

NARUTO is a **Red Team Security Scanner** - a website that scans computers/servers for open ports, running services, and security vulnerabilities. It's like a digital detective that looks for weaknesses.

---

## 📊 How It Works - Step by Step

### **Step 1: User Opens Website**
```
User types: http://localhost:5000 in browser
↓
Website loads with:
  • Dark theme UI (looks like a hacker interface)
  • Input fields for target IP and scan options
  • Terminal display area for results
  • Buttons: Execute Scan, Voice Command, Download Report
```

### **Step 2: User Enters Information**
```
User can input in 2 ways:

Option A - Voice Command:
  1. Click microphone button 🎤
  2. Say: "scan 192.168.1.1 with nmap aggressive"
  3. AI understands and fills the form automatically

Option B - Manual Input:
  1. Type target IP: 192.168.1.1
  2. Choose tool: Nmap (scan ports), Whois (domain info), or Gobuster (find directories)
  3. Choose scan type: Basic, Service Detection, Aggressive, or Custom Ports
  4. Click "Execute Scan" button
```

### **Step 3: Safety Check (Validation)**
```
Before anything happens, the system checks:
  ✓ Is the target a valid IP address?
  ✓ Is it a private/safe IP (not random internet targets)?
  ✓ Is the tool valid?
  ✓ Is the scan type valid?

If something is wrong → Show error message
If everything is OK → Continue to scanning
```

### **Step 4: Run the Scan Tool**
```
The website runs actual scanning tools on your computer:

For Nmap (Port Scanner):
  • Starts the nmap program
  • Scans the target IP for open ports
  • Identifies running services (SSH, FTP, HTTP, etc.)
  • Gets version numbers of those services
  • Time: 1-3 minutes depending on options

For Whois:
  • Gets domain registration information

For Gobuster:
  • Finds hidden directories/files on web servers
```

### **Step 5: AI Analysis**
```
The scan results are sent to Ollama (an AI running locally):

  Nmap Output: "Ports 22, 80, 443 are open with SSH, Apache, HTTPS"
          ↓
       Ollama AI (Mistral Model)
          ↓
  AI Analysis: "This server has SSH remote access, Apache web server, 
               and HTTPS encryption. SSH version 4.7 is very old and 
               should be updated immediately."

Time: ~30-60 seconds
Result: Natural language explanation of what was found
```

### **Step 6: Find Vulnerabilities (Threat Intelligence)**
```
For each service found, the system looks up known vulnerabilities:

  Service Found: "Apache v2.2.8"
          ↓
  Query NVD Database (Official US vulnerability database)
  at: https://nvd.nist.gov
          ↓
  Database Returns: "CVE-2008-2364 - Critical vulnerability found"
          ↓
  Extract Info:
    • CVE ID: CVE-2008-2364
    • Severity: MEDIUM
    • CVSS Score: 5.0 (0-10 scale, higher = worse)
    • Description: Proxy handling vulnerability
    • Link: https://nvd.nist.gov/vuln/detail/CVE-2008-2364

Repeat for each service found:
  • vsftpd 2.3.4  → CVE-2011-2523 [CRITICAL]
  • OpenSSH 4.7   → 5 CVEs [HIGH severity]
  • Apache 2.2.8  → CVE-2008-2364 [MEDIUM]
  • BIND 9.4.2    → No vulnerabilities found

Total vulnerabilities found: 7
```

### **Step 7: Create Reports**
```
The system generates 2 files:

Report 1 - AI Analysis Report:
  File name: naruto_report_192.168.1.1_20260409_044623.txt
  Content:
    • What was scanned (IP, tool, scan type)
    • AI analysis of the results
    • Insights about security posture

Report 2 - Threat Intelligence Report:
  File name: naruto_ti_report_192.168.1.1_20260409_044623.txt
  Content:
    • List of all services found
    • Each service with its vulnerabilities
    • CVSS scores and severity levels
    • Risk assessment: CRITICAL/HIGH/MEDIUM/LOW
    • Links to vulnerability details
    • Summary of findings

Both files saved to: ./reports/ folder
```

### **Step 8: Display Results on Website**
```
Terminal window shows (live updates):

✅ Execution Output
   PORT      STATE    SERVICE VERSION
   21/tcp    open     ftp     vsftpd 2.3.4
   22/tcp    open     ssh     OpenSSH 4.7p1
   80/tcp    open     http    Apache 2.2.8
   443/tcp   open     https   OpenSSL 0.9.8
   [... more ports ...]

✅ AI Analysis
   "4 open ports detected. The FTP service (vsftpd 2.3.4) is 
    particularly dangerous due to a known backdoor exploit CVE-2011-2523.
    SSH and Apache are also outdated and should be upgraded."

✅ Threat Intelligence Summary
   Services Analyzed: 4
   Total Vulnerabilities: 7
   
   🔴 CRITICAL: vsftpd 2.3.4
      • CVE-2011-2523 (CVSS: 9.8)
      • Description: Backdoor vulnerability
      
   🟠 HIGH: OpenSSH 4.7p1
      • 5 vulnerabilities found
      • CVE-2007-4752, CVE-2008-5161, CVE-2009-3710, etc.
      
   🟡 MEDIUM: Apache 2.2.8
      • CVE-2008-2364 (CVSS: 5.0)
      • Proxy handling issue
      
   🟢 LOW: BIND 9.4.2
      • No known vulnerabilities

📥 Download buttons now enabled - Click to save both reports
```

### **Step 9: Download Reports**
```
User clicks "📥 Download Report" button

Backend:
  1. Creates download link for AI report
  2. Creates download link for TI report
  3. Waits 500ms (for file manager)
  4. Both files download to user's Downloads folder

Result:
  ✅ naruto_report_192.168.1.1_20260409_044623.txt (Downloaded)
  ✅ naruto_ti_report_192.168.1.1_20260409_044623.txt (Downloaded)
```

---

## ⏱️ Timeline - How Long Does It Take?

| Time | What Happens |
|------|--------------|
| 0:00 | User enters data and clicks scan |
| 0:05 | Frontend validates and sends to backend |
| 0:10 | Backend validates |
| 0:20 | Nmap starts scanning |
| 2:00 | Nmap finishes (60-180 seconds of scanning) |
| 2:30 | AI analysis runs (30-60 seconds) |
| 3:30 | Threat intelligence lookup (NVD database queries) |
| 4:00 | Reports generated and saved |
| 4:05 | Results displayed on website |
| 4:10 | User downloads both report files |

**Total Time: ~4-5 minutes**

---

## 🔧 Technical Components (Simplified)

```
Browser (Frontend)
    ↓ User clicks button
Flask Website (Backend)
    ↓ Validates inputs
Executor (Runs scanning tools)
    ├─ Nmap (scan ports)
    ├─ Whois (get domain info)
    └─ Gobuster (find directories)
    ↓ Gets results
AI Analyzer (Ollama)
    ↓ Generates insights
Threat Intelligence (NVD API)
    ↓ Looks up vulnerabilities
Report Generator
    ├─ Creates AI report
    └─ Creates TI report
    ↓ Saves files
File Storage (./reports/)
    ↓ User downloads
Browser Downloads
```

---

## 🎯 What Each Tool Does

### **Nmap (Network Mapper)**
- **Purpose**: Scans a computer to find open ports
- **What it shows**: 
  - Open ports (21, 22, 80, 443, etc.)
  - Services running (FTP, SSH, HTTP, etc.)
  - Software versions (Apache 2.2.8, OpenSSH 4.7, etc.)
- **Time**: 1-3 minutes
- **Scan types**:
  - Basic: Quick scan of common ports
  - Service Detection: Find services AND versions
  - Aggressive: Deep scan, all ports
  - Custom Ports: User specifies which ports (22, 80, 443)

### **Whois**
- **Purpose**: Gets registration information about a domain
- **What it shows**:
  - Domain owner
  - Registrar
  - Contact information
  - Domain dates

### **Gobuster**
- **Purpose**: Finds hidden directories and files on web servers
- **What it shows**:
  - Hidden admin pages (/admin, /login)
  - Configuration files (/backup, /config)
  - API endpoints (/api/users, /api/data)

---

## 🛡️ Safety & Security Features

1. **Input Validation**: Only safe targets are scanned
2. **Whitelist**: Only private IPs allowed (192.168.x.x, 10.x.x.x)
3. **No Shell Access**: Commands run safely without shell vulnerabilities
4. **Timeout Protection**: Scans stop if they take too long
5. **Error Handling**: Bad inputs show helpful error messages

---

## 📝 Example Workflow

**User Action**: "Scan 192.168.1.100 for open ports using Nmap with service detection"

**Step-by-step breakdown**:

1. **Input**: User enters IP and selects options
2. **Validation**: Checks it's a valid private IP ✓
3. **Execution**: Runs: `nmap -sV -p- 192.168.1.100`
4. **Results**: 
   ```
   Port 21: FTP vsftpd 2.3.4
   Port 22: SSH OpenSSH 4.7p1
   Port 80: HTTP Apache 2.2.8
   ```
5. **AI Analysis**: "FTP is old and has vulnerabilities. SSH version is outdated."
6. **Threat Intel**: 
   - vsftpd: 1 vulnerability (CVE-2011-2523)
   - OpenSSH: 5 vulnerabilities
   - Apache: 1 vulnerability
7. **Reports Generated**: 2 files created
8. **Display**: Results shown on terminal
9. **Download**: User clicks once, both reports download

---

## ✅ Status Check

- ✅ Flask running (Port 5000)
- ✅ All tools installed (Nmap, Whois, Gobuster)
- ✅ AI working (Ollama - Mistral 7B model)
- ✅ Vulnerability database active (NVD API)
- ✅ Reports generating correctly
- ✅ Dual downloads working
- ✅ Complete workflow verified

---

## 🚀 Quick Start

```bash
# 1. Open website
http://localhost:5000

# 2. Enter target IP
192.168.1.1

# 3. Select tool
Nmap

# 4. Select scan type
Service Detection

# 5. Click Execute Scan
(Wait 4-5 minutes)

# 6. Review results on screen

# 7. Click Download Report
(Both files download)
```

---

## 🎓 For Non-Technical Users

**Simple explanation**: 
- NARUTO is like a **security guard for your network**
- It visits each "door" (port) on your computer/server
- Checks if it's open and what's behind it
- Looks up if there are known problems with what it finds
- Writes a report telling you what's vulnerable and how serious it is
- You download the report and know what to fix

---

## That's It! 🎉

The website works automatically - you just:
1. Enter target
2. Choose options
3. Click scan
4. Wait for results
5. Download reports

Everything else happens automatically in the background!

