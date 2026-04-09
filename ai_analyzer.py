import requests
import json
from config import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_API_KEY

class AIAnalyzer:
    """Optional modular AI analysis using Ollama (local or remote)."""
    
    def __init__(self):
        self.base_url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.headers = self._build_headers()
        self.available = self._check_availability()
    
    def _build_headers(self):
        """Build request headers with API key if provided."""
        headers = {"Content-Type": "application/json"}
        if OLLAMA_API_KEY:
            headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"
        return headers
    
    def _check_availability(self):
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", headers=self.headers, timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def analyze_nmap_results(self, nmap_output, scan_type="basic", timeout=60):
        """Analyze Nmap results with AI in structured format."""
        if not self.available:
            return {"status": "ollama_unavailable", "analysis": None}
        
        prompt = f"""You are a cybersecurity assistant.

Analyze the following Nmap output.

Tool: Nmap
Scan Type: {scan_type}

Provide structured output with:

1. Scan Overview - Summary of what was scanned
2. Key Findings - Open ports, services, versions detected
3. Risk Analysis - Security implications (realistic, no assumptions)
4. Recommended Next Steps - Actions for further reconnaissance
5. Notes - Any additional observations

Keep it clear, concise, and professional.

Nmap Output:
{nmap_output}"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                headers=self.headers,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "analysis": data.get("response", "")
                }
            else:
                return {"status": "error", "analysis": "AI analysis failed"}
        except Exception as e:
            return {"status": "error", "analysis": f"Error: {str(e)}"}
    
    def analyze_whois_results(self, whois_output, timeout=60):
        """Analyze Whois results with AI in structured format."""
        if not self.available:
            return {"status": "ollama_unavailable", "analysis": None}
        
        prompt = f"""You are a cybersecurity assistant.

Analyze the following Whois output.

Tool: Whois
Scan Type: Domain Lookup

Provide structured output with:

1. Scan Overview - What domain information was retrieved
2. Key Findings - Registrar, registrant details, nameservers, registration dates
3. Risk Analysis - Privacy concerns, potential security implications (realistic, no assumptions)
4. Recommended Next Steps - Further reconnaissance or verification steps
5. Notes - Any notable registrant or registration patterns

Keep it clear, concise, and professional.

Whois Output:
{whois_output}"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                headers=self.headers,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "analysis": data.get("response", "")
                }
            else:
                return {"status": "error", "analysis": "AI analysis failed"}
        except Exception as e:
            return {"status": "error", "analysis": f"Error: {str(e)}"}
    
    def analyze_gobuster_results(self, gobuster_output, timeout=60):
        """Analyze Gobuster results with AI in structured format."""
        if not self.available:
            return {"status": "ollama_unavailable", "analysis": None}
        
        prompt = f"""You are a cybersecurity assistant.

Analyze the following Gobuster output.

Tool: Gobuster
Scan Type: Directory/Path Brute Force

Provide structured output with:

1. Scan Overview - What directories/paths were discovered
2. Key Findings - Found directories, status codes, interesting paths, potential application mapping
3. Risk Analysis - Exposure of sensitive directories or admin panels (realistic, no assumptions)
4. Recommended Next Steps - Further investigation of discovered paths
5. Notes - Application hints, framework detection, interesting patterns

Keep it clear, concise, and professional.

Gobuster Output:
{gobuster_output}"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                headers=self.headers,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "analysis": data.get("response", "")
                }
            else:
                return {"status": "error", "analysis": "AI analysis failed"}
        except Exception as e:
            return {"status": "error", "analysis": f"Error: {str(e)}"}