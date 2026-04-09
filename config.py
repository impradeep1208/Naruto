import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Whitelist Configuration
ALLOWED_TOOLS = ["nmap", "whois", "gobuster"]

ALLOWED_PRIVATE_IPS = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16"
]

WHITELISTED_DOMAINS = [
    "testlab.local",
    "lab.internal",
    "hackhethebox.eu",
    "tryhackme.com",
    "example.com"
]

# Scan Type Mappings
SCAN_TYPES = {
    "basic": ["-sn"],
    "service_detection": ["-sV", "-p-"],
    "aggressive": ["-A", "-T4"],
    "custom_ports": []  # Will be built dynamically with user-specified ports
}

# AI Configuration - Remote Ollama Support
OLLAMA_MODEL = "mistral"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")  # Remote Ollama server URL
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")  # Optional API key for auth

# AI Analysis timeouts by scan type (seconds)
# Optimized for speed - if AI takes too long, gracefully skip it
AI_ANALYSIS_TIMEOUTS = {
    "basic": 30,                    # Quick scan (30 sec)
    "service_detection": 60,        # Medium scan (1 min)
    "aggressive": 90,               # Full analysis (1.5 min)
    "custom_ports": 120             # Custom ports - varies (2 min)
}

# Report Configuration
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Flask Configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
DEBUG = False
