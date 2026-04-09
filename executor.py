import subprocess
import json
from datetime import datetime
from validator import validate_tool, validate_target, validate_scan_type, ValidationError
from config import SCAN_TYPES

class ExecutionError(Exception):
    pass

def execute_nmap(target, scan_type, port_range=None):
    """Execute Nmap scan safely."""
    validate_target(target)
    validate_scan_type(scan_type)
    
    flags = SCAN_TYPES[scan_type]
    
    # Build command as list (NEVER use shell=True)
    cmd = ["nmap"] + flags + [target]
    
    # Handle custom port range
    if scan_type == "custom_ports" and port_range:
        cmd = ["nmap", "-sV"] + ["-p", port_range] + [target]
    
    # Set timeout based on scan type (optimized for speed)
    timeout_map = {
        "basic": 60,                  # 1 minute
        "service_detection": 180,     # 3 minutes
        "aggressive": 240,            # 4 minutes
        "custom_ports": 300           # 5 minutes (ports vary)
    }
    timeout = timeout_map.get(scan_type, 120)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "status": "success" if result.returncode == 0 else "partial",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "timestamp": datetime.now().isoformat(),
            "command": " ".join(cmd)
        }
    except subprocess.TimeoutExpired:
        raise ExecutionError(f"Nmap scan timed out after {timeout} seconds. Try a faster scan type (Service Detection) or smaller port range.")
    except Exception as e:
        raise ExecutionError(f"Nmap execution failed: {str(e)}")

def execute_whois(target):
    """Execute Whois lookup safely."""
    validate_target(target)
    
    cmd = ["whois", target]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "status": "success" if result.returncode == 0 else "partial",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "timestamp": datetime.now().isoformat(),
            "command": " ".join(cmd)
        }
    except subprocess.TimeoutExpired:
        raise ExecutionError("Whois lookup timed out after 30 seconds")
    except Exception as e:
        raise ExecutionError(f"Whois execution failed: {str(e)}")

def execute_gobuster(target, scan_type="basic"):
    """Execute Gobuster directory scan safely."""
    validate_target(target)
    
    # Gobuster requires wordlist path
    wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"
    
    cmd = ["gobuster", "dir", "-u", f"http://{target}", "-w", wordlist]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        return {
            "status": "success" if result.returncode == 0 else "partial",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "timestamp": datetime.now().isoformat(),
            "command": " ".join(cmd)
        }
    except subprocess.TimeoutExpired:
        raise ExecutionError("Gobuster scan timed out after 120 seconds")
    except Exception as e:
        raise ExecutionError(f"Gobuster execution failed: {str(e)}")

def execute_scan(tool, target, scan_type, port_range=None):
    """Route execution to appropriate tool."""
    validate_tool(tool)
    validate_target(target)
    validate_scan_type(scan_type)
    
    if tool == "nmap":
        return execute_nmap(target, scan_type, port_range)
    elif tool == "whois":
        return execute_whois(target)
    elif tool == "gobuster":
        return execute_gobuster(target, scan_type)
    else:
        raise ExecutionError(f"Unknown tool: {tool}")