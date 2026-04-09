"""
NARUTO Threat Intelligence Module
Extracts services from Nmap output and queries NVD API for CVEs

Author: NARUTO Red Team Assistant
Security: For authorized lab testing only
"""

import re
import logging
import requests
import json
from typing import List, Dict, Optional, Tuple
from urllib.parse import quote
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [TI] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# API Configuration
NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_TIMEOUT = 15  # seconds
NVD_RESULT_LIMIT = 5  # Top 5 CVEs per service

# Service version patterns for common services
SERVICE_PATTERNS = {
    'Apache': r'Apache/(\d+\.\d+\.\d+)',
    'Nginx': r'nginx/(\d+\.\d+\.\d+)',
    'OpenSSH': r'OpenSSH_(\d+\.\d+)',
    'vsftpd': r'vsftpd (\d+\.\d+\.\d+)',
    'Sendmail': r'Sendmail (\d+\.\d+\.\d+)',
    'Postfix': r'Postfix (\d+\.\d+\.\d+)',
    'MySQL': r'MySQL (\d+\.\d+\.\d+)',
    'PostgreSQL': r'PostgreSQL (\d+\.\d+\.\d+)',
    'Microsoft-IIS': r'Microsoft-IIS/(\d+\.\d+)',
    'ProFTPD': r'ProFTPD (\d+\.\d+\.\d+)',
}


class ThreatIntelligenceError(Exception):
    """Custom exception for threat intelligence operations"""
    pass


def extract_services(nmap_output: str) -> List[Dict[str, str]]:
    """
    Extract service names and versions from Nmap output.
    
    Parses Nmap output to find service banners and version information.
    
    Args:
        nmap_output (str): Raw Nmap scan output
        
    Returns:
        List[Dict]: List of {service_name, version, port, protocol}
        Example:
        [
            {"service": "Apache", "version": "2.4.49", "port": "80", "protocol": "http"},
            {"service": "OpenSSH", "version": "7.6", "port": "22", "protocol": "ssh"}
        ]
    """
    services = []
    
    try:
        if not nmap_output or not nmap_output.strip():
            logger.warning("Empty Nmap output provided")
            return services
        
        logger.info("Extracting services from Nmap output...")
        
        # Split output into lines for processing
        lines = nmap_output.split('\n')
        
        for line in lines:
            # Look for lines with version information (typically start with port number)
            # Format: "80/tcp   open  http    Apache httpd 2.4.49"
            
            # Skip headers and empty lines
            if not line.strip() or 'PORT' in line or 'STATE' in line:
                continue
            
            # Extract port and service info
            port_match = re.match(r'(\d+)/(\w+)\s+(\w+)\s+(\w+)\s+(.*)', line)
            if not port_match:
                continue
            
            port, protocol, state, service_type, service_info = port_match.groups()
            
            # Skip closed/filtered ports
            if state != 'open':
                continue
            
            # Try to extract version using service patterns
            version = None
            service_name = service_type.capitalize()
            
            for known_service, pattern in SERVICE_PATTERNS.items():
                if known_service.lower() in service_info.lower() or known_service.lower() in service_type.lower():
                    version_match = re.search(pattern, service_info)
                    if version_match:
                        version = version_match.group(1)
                        service_name = known_service
                        break
            
            # If no specific pattern matched, use generic version extraction
            if not version:
                version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', service_info)
                if version_match:
                    version = version_match.group(1)
            
            # Only add if we found a version
            if version:
                services.append({
                    'service': service_name,
                    'version': version,
                    'port': port,
                    'protocol': protocol,
                    'full_info': service_info.strip()
                })
                logger.debug(f"Extracted: {service_name} {version} on port {port}")
        
        logger.info(f"Extracted {len(services)} services with version info")
        return services
    
    except Exception as e:
        logger.error(f"Error extracting services: {str(e)}")
        return []


def calculate_severity_from_cvss(cvss_score: Optional[float]) -> str:
    """
    Calculate severity level from CVSS score.
    
    Fallback function for when NVD API doesn't provide baseSeverity.
    Uses CVSS v3.0+ severity mapper.
    
    Args:
        cvss_score (float): CVSS score (0.0-10.0)
        
    Returns:
        str: Severity level (CRITICAL, HIGH, MEDIUM, LOW, NONE)
    """
    if cvss_score is None:
        return "UNKNOWN"
    
    try:
        score = float(cvss_score)
        if score >= 9.0:
            return "CRITICAL"
        elif score >= 7.0:
            return "HIGH"
        elif score >= 4.0:
            return "MEDIUM"
        elif score > 0:
            return "LOW"
        else:
            return "NONE"
    except (ValueError, TypeError):
        return "UNKNOWN"


def fetch_cves(service_name: str, version: str) -> List[Dict]:
    """
    Query NVD API for CVEs related to a service and version.
    
    Makes REST API calls to NVD to find vulnerabilities.
    
    Args:
        service_name (str): Service name (e.g., "Apache", "OpenSSH")
        version (str): Version number (e.g., "2.4.49")
        
    Returns:
        List[Dict]: List of CVE records (max NVD_RESULT_LIMIT)
        Example:
        [
            {
                "cve_id": "CVE-2021-41773",
                "description": "Apache HTTP Server 2.4.49 and 2.4.50...",
                "cvss_score": 7.5,
                "severity": "HIGH",
                "published_date": "2021-10-05"
            }
        ]
    """
    
    try:
        if not service_name or not version:
            logger.warning("Service name or version missing")
            return []
        
        logger.info(f"Fetching CVEs for {service_name} {version}...")
        
        # Format search query
        search_query = f"{service_name} {version}"
        
        # NVD API parameters
        params = {
            'keywordSearch': search_query,
            'resultsPerPage': NVD_RESULT_LIMIT * 2,  # Get more to filter duplicates
            'startIndex': 0
        }
        
        # Make API request
        response = requests.get(
            NVD_API_BASE,
            params=params,
            timeout=NVD_API_TIMEOUT,
            headers={'User-Agent': 'NARUTO-TI/1.0'}
        )
        
        response.raise_for_status()
        data = response.json()
        
        cves = []
        vulnerabilities = data.get('vulnerabilities', [])
        
        # Process CVE results
        for vuln in vulnerabilities[:NVD_RESULT_LIMIT]:
            cve_data = vuln.get('cve', {})
            metrics = cve_data.get('metrics', {})
            
            cve_id = cve_data.get('id', 'N/A')
            description = cve_data.get('descriptions', [{}])[0].get('value', 'No description')
            published = cve_data.get('published', 'N/A')
            
            # Extract CVSS score and severity
            cvss_score = None
            severity = "UNKNOWN"
            
            # Try CVSS v3.1 first (most current), then v3.0, then v2.0
            cvssV31 = metrics.get('cvssMetricV31', [{}])[0] if metrics.get('cvssMetricV31') else None
            cvssV30 = metrics.get('cvssMetricV30', [{}])[0] if metrics.get('cvssMetricV30') else None
            cvssV2 = metrics.get('cvssMetricV2', [{}])[0] if metrics.get('cvssMetricV2') else None
            
            if cvssV31:
                cvss_score = cvssV31.get('cvssData', {}).get('baseScore')
                severity = cvssV31.get('cvssData', {}).get('baseSeverity', None)
            elif cvssV30:
                cvss_score = cvssV30.get('cvssData', {}).get('baseScore')
                severity = cvssV30.get('cvssData', {}).get('baseSeverity', None)
            elif cvssV2:
                cvss_score = cvssV2.get('cvssData', {}).get('baseScore')
                severity = cvssV2.get('cvssData', {}).get('baseSeverity', None)
            
            # Fallback: Calculate severity from CVSS score if not provided
            if not severity or severity == 'UNKNOWN':
                severity = calculate_severity_from_cvss(cvss_score)
            
            cves.append({
                'cve_id': cve_id,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'cvss_score': cvss_score,
                'severity': severity,
                'published_date': published,
                'nvd_link': f"https://nvd.nist.gov/vuln/detail/{cve_id}"
            })
        
        logger.info(f"Found {len(cves)} CVEs for {service_name} {version}")
        return cves
    
    except requests.exceptions.Timeout:
        logger.error(f"NVD API timeout for {service_name} {version}")
        return []
    except requests.exceptions.ConnectionError:
        logger.error(f"NVD API connection error for {service_name} {version}")
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f"NVD API HTTP error: {e.response.status_code}")
        return []
    except json.JSONDecodeError:
        logger.error("NVD API returned invalid JSON")
        return []
    except Exception as e:
        logger.error(f"Error fetching CVEs: {str(e)}")
        return []


def extract_services_from_whois(whois_output: str) -> List[Dict[str, str]]:
    """
    Extract service/version info from Whois output.
    
    Whois typically doesn't contain service versions, so this returns
    empty list as Whois is for domain/IP registration info, not services.
    """
    logger.info("Whois output: Threat intelligence not applicable (registration data)")
    return []


def extract_services_from_gobuster(gobuster_output: str) -> List[Dict[str, str]]:
    """
    Extract service info from Gobuster directory discovery output.
    
    Attempts to identify version info from discovered endpoints.
    Gobuster typically returns HTTP status codes and paths, not service versions.
    Returns empty list as version extraction from paths is unreliable.
    """
    logger.info("Gobuster output: Threat intelligence not applicable (directory discovery)")
    return []


def get_threat_intelligence(scan_output: str, tool_type: str = "nmap") -> Dict:
    """
    Complete threat intelligence pipeline for any reconnaissance tool.
    
    Intelligently extracts services/versions from scan output and queries NVD for CVEs.
    
    Args:
        scan_output (str): Raw tool output (Nmap, Whois, or Gobuster)
        tool_type (str): Tool used (nmap, whois, gobuster) - default: nmap
        
    Returns:
        Dict: Structured threat intelligence report with threat data or status message
    """
    
    try:
        logger.info(f"Starting threat intelligence analysis for {tool_type.upper()}...")
        
        # Step 1: Extract services based on tool type
        services = []
        if tool_type == "nmap":
            services = extract_services(scan_output)
            logger.info(f"Nmap: Extracted {len(services)} services with version info")
        elif tool_type == "whois":
            services = extract_services_from_whois(scan_output)
            logger.info(f"Whois: Extracted {len(services)} services")
        elif tool_type == "gobuster":
            services = extract_services_from_gobuster(scan_output)
            logger.info(f"Gobuster: Extracted {len(services)} services")
        else:
            # Fallback: try Nmap extraction for unknown tools
            services = extract_services(scan_output)
            logger.info(f"Unknown tool type, attempting generic extraction: {len(services)} services found")
        
        logger.info(f"Services extracted: {len(services)}")
        for service in services:
            logger.debug(f"  - {service['service']} {service['version']} on port {service.get('port', 'N/A')}")
        
        if not services:
            logger.warning(f"No services with version info found in {tool_type} output")
            return {
                "status": "no_data",
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"No services with version information found in {tool_type.upper()} output. Threat intelligence requires service version data.",
                "threat_data": []
            }
        
        # Step 2: Fetch CVEs for each service
        threat_data = []
        total_cves = 0
        
        for service in services:
            cves = fetch_cves(service['service'], service['version'])
            
            # Determine risk level
            risk_level = "LOW"
            if cves:
                max_severity = max([cve.get('severity', 'UNKNOWN') for cve in cves], default='UNKNOWN')
                risk_mapping = {
                    'CRITICAL': 'CRITICAL',
                    'HIGH': 'HIGH',
                    'MEDIUM': 'MEDIUM',
                    'LOW': 'LOW',
                    'UNKNOWN': 'UNKNOWN'
                }
                risk_level = risk_mapping.get(max_severity, 'UNKNOWN')
            
            threat_data.append({
                'service': service['service'],
                'version': service['version'],
                'port': service['port'],
                'protocol': service['protocol'],
                'cves': cves,
                'vulnerability_count': len(cves),
                'risk_level': risk_level
            })
            
            total_cves += len(cves)
        
        logger.info(f"Threat intelligence analysis complete: {total_cves} CVEs found")
        
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "services_analyzed": len(services),
            "total_vulnerabilities": total_cves,
            "threat_data": threat_data,
            "summary": f"{len(services)} services analyzed, {total_cves} vulnerabilities found"
        }
    
    except Exception as e:
        logger.error(f"Error in threat intelligence analysis: {str(e)}")
        return {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "message": str(e),
            "threat_data": []
        }


def format_threat_report(ti_data: Dict) -> str:
    """
    Format threat intelligence data into human-readable report.
    
    Args:
        ti_data (Dict): Threat intelligence data from get_threat_intelligence()
        
    Returns:
        str: Formatted report text
    """
    
    report = []
    report.append("=" * 80)
    report.append("THREAT INTELLIGENCE REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {ti_data.get('timestamp', 'N/A')}")
    report.append("")
    
    if ti_data.get('status') != 'success':
        report.append(f"Status: {ti_data.get('message', 'Analysis failed')}")
        return '\n'.join(report)
    
    report.append(f"Services Analyzed: {ti_data.get('services_analyzed', 0)}")
    report.append(f"Total Vulnerabilities Found: {ti_data.get('total_vulnerabilities', 0)}")
    report.append("")
    
    for service_data in ti_data.get('threat_data', []):
        report.append("-" * 80)
        report.append(f"Service: {service_data['service']} {service_data['version']}")
        report.append(f"Port: {service_data['port']}/{service_data['protocol']}")
        report.append(f"Risk Level: {service_data['risk_level']}")
        report.append(f"Vulnerabilities: {service_data['vulnerability_count']}")
        report.append("")
        
        if service_data['cves']:
            report.append("CVEs Detected:")
            for cve in service_data['cves']:
                report.append("")
                report.append(f"  CVE ID: {cve['cve_id']}")
                report.append(f"  Severity: {cve['severity']}")
                if cve['cvss_score']:
                    report.append(f"  CVSS Score: {cve['cvss_score']}")
                report.append(f"  Description: {cve['description']}")
                report.append(f"  Link: {cve['nvd_link']}")
        else:
            report.append("No CVEs found in NVD database for this version.")
        
        report.append("")
    
    report.append("=" * 80)
    report.append((f"Summary: {ti_data.get('summary', 'Analysis complete')}"))
    report.append("=" * 80)
    
    return '\n'.join(report)


# Example usage / Testing
if __name__ == "__main__":
    # Test with sample Nmap output
    sample_nmap_output = """
    Nmap scan report for example.com (93.184.216.34)
    Host is up (0.042s latency).
    
    PORT     STATE SERVICE VERSION
    22/tcp   open  ssh     OpenSSH_7.6p1 Ubuntu 4ubuntu0.5
    80/tcp   open  http    Apache httpd 2.4.49 (Ubuntu)
    443/tcp  open  https   Apache httpd 2.4.49 (Ubuntu)
    3306/tcp open  mysql   MySQL 5.7.31-0ubuntu0.18.04.1
    """
    
    print("Testing Threat Intelligence Module...\n")
    
    # Extract services
    print("1. Extracting services...")
    services = extract_services(sample_nmap_output)
    print(f"   Found {len(services)} services:")
    for svc in services:
        print(f"   - {svc['service']} {svc['version']} on port {svc['port']}")
    print()
    
    # Get full threat intelligence
    print("2. Fetching threat intelligence...")
    ti_report = get_threat_intelligence(sample_nmap_output)
    print(f"   Status: {ti_report['status']}")
    print(f"   Services analyzed: {ti_report.get('services_analyzed', 0)}")
    print(f"   Vulnerabilities found: {ti_report.get('total_vulnerabilities', 0)}")
    print()
    
    # Format and print report
    print("3. Formatted Report:")
    print()
    formatted = format_threat_report(ti_report)
    print(formatted)
