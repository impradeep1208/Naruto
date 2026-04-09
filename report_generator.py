import os
from datetime import datetime
from config import REPORTS_DIR

class ReportGenerator:
    """Generate structured reconnaissance reports."""
    
    def __init__(self, target, tool, scan_type):
        self.target = target
        self.tool = tool
        self.scan_type = scan_type
        self.timestamp = datetime.now()
    
    def generate_report(self, execution_result, ai_analysis=None, threat_intelligence=None):
        """Generate AI analysis report and threat intelligence report."""
        ai_report_filename = f"naruto_report_{self.target}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
        ai_report_path = os.path.join(REPORTS_DIR, ai_report_filename)
        
        # Generate AI Analysis Report
        with open(ai_report_path, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("NARUTO AI ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Target: {self.target}\n")
            f.write(f"Tool: {self.tool.upper()}\n")
            f.write(f"Scan Type: {self.scan_type}\n")
            f.write(f"Date/Time: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Only include AI analysis, not raw scan output
            if ai_analysis and ai_analysis.get("status") == "success":
                f.write("-" * 80 + "\n")
                f.write("AI ANALYSIS\n")
                f.write("-" * 80 + "\n")
                f.write(ai_analysis.get("analysis", "No analysis available") + "\n\n")
            else:
                f.write("-" * 80 + "\n")
                f.write("AI ANALYSIS\n")
                f.write("-" * 80 + "\n")
                f.write("No AI analysis available for this scan.\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        # Generate Threat Intelligence Report (for any tool if applicable)
        ti_report_filename = None
        if threat_intelligence and threat_intelligence.get("status") == "success":
            ti_report_filename = f"naruto_ti_report_{self.target}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
            ti_report_path = os.path.join(REPORTS_DIR, ti_report_filename)
            
            with open(ti_report_path, "w") as f:
                f.write("=" * 80 + "\n")
                f.write("NARUTO THREAT INTELLIGENCE REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Target: {self.target}\n")
                f.write(f"Tool: {self.tool.upper()}\n")
                f.write(f"Scan Type: {self.scan_type}\n")
                f.write(f"Date/Time: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write(f"Services Analyzed: {threat_intelligence.get('services_analyzed', 0)}\n")
                f.write(f"Total Vulnerabilities: {threat_intelligence.get('total_vulnerabilities', 0)}\n\n")
                
                f.write("-" * 80 + "\n")
                f.write("VULNERABILITY DETAILS\n")
                f.write("-" * 80 + "\n\n")
                
                threat_data = threat_intelligence.get("threat_data", [])
                if threat_data:
                    for service in threat_data:
                        f.write(f"SERVICE: {service.get('service')} v{service.get('version')}\n")
                        f.write(f"  Port: {service.get('port')}/{service.get('protocol')}\n")
                        f.write(f"  Risk Level: {service.get('risk_level')}\n")
                        f.write(f"  Vulnerabilities Found: {service.get('vulnerability_count')}\n\n")
                        
                        cves = service.get('cves', [])
                        if cves:
                            f.write("  CVEs:\n")
                            for cve in cves:
                                f.write(f"    • {cve.get('cve_id')} [{cve.get('severity')}] CVSS: {cve.get('cvss_score', 'N/A')}\n")
                                f.write(f"      {cve.get('description', 'No description')}\n")
                                f.write(f"      Link: {cve.get('nvd_link', 'N/A')}\n\n")
                        else:
                            f.write("  No CVEs found\n\n")
                else:
                    f.write("No services analyzed or threat data available.\n")
                
                f.write("\n" + "-" * 80 + "\n")
                f.write(f"SUMMARY\n")
                f.write("-" * 80 + "\n")
                f.write(f"{threat_intelligence.get('summary', 'No summary available')}\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("END OF THREAT INTELLIGENCE REPORT\n")
                f.write("=" * 80 + "\n")
        
        return ai_report_path, ai_report_filename, ti_report_filename