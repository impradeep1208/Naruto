from flask import Flask, render_template, request, jsonify, send_file
import os
from validator import validate_tool, validate_target, validate_scan_type, parse_command, ValidationError
from executor import execute_scan, ExecutionError
from ai_analyzer import AIAnalyzer
from report_generator import ReportGenerator
from threat_intelligence import get_threat_intelligence
from config import REPORTS_DIR, AI_ANALYSIS_TIMEOUTS

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__,
            static_folder=STATIC_DIR,
            static_url_path='/static',
            template_folder=TEMPLATES_DIR)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ai_analyzer = AIAnalyzer()

@app.route("/")
def index():
    """Serve main UI."""
    return render_template("index.html")

@app.route("/api/scan", methods=["POST"])
def scan():
    """Execute reconnaissance scan."""
    try:
        data = request.get_json()
        target = data.get("target", "").strip()
        tool = data.get("tool", "nmap").strip()
        scan_type = data.get("scan_type", "basic").strip()
        port_range = data.get("port_range", "").strip() if data.get("port_range") else None
        
        print(f"[SCAN REQUEST] Target: {target}, Tool: {tool}, Scan Type: {scan_type}, Ports: {port_range}")
        
        if not target:
            return jsonify({"status": "error", "message": "Target required"}), 400
        
        # Validate inputs
        validate_target(target)
        validate_tool(tool)
        validate_scan_type(scan_type)
        
        # Validate port range if custom ports requested
        if scan_type == "custom_ports":
            if not port_range:
                return jsonify({"status": "error", "message": "Port range required for custom port scan"}), 400
        
        # Execute scan
        execution_result = execute_scan(tool, target, scan_type, port_range)
        
        # Get AI analysis with scan-type-specific timeout for all tools
        ai_analysis = None
        timeout = AI_ANALYSIS_TIMEOUTS.get(scan_type, 60)
        
        if ai_analyzer.available:
            if tool == "nmap":
                ai_analysis = ai_analyzer.analyze_nmap_results(execution_result["stdout"], scan_type=scan_type, timeout=timeout)
            elif tool == "whois":
                ai_analysis = ai_analyzer.analyze_whois_results(execution_result["stdout"], timeout=timeout)
            elif tool == "gobuster":
                ai_analysis = ai_analyzer.analyze_gobuster_results(execution_result["stdout"], timeout=timeout)
        
        # Get threat intelligence for Nmap scans
        threat_intelligence_data = None
        if tool == "nmap":
            try:
                print(f"[THREAT INTELLIGENCE] Analyzing Nmap output for CVEs...")
                threat_intelligence_data = get_threat_intelligence(execution_result["stdout"])
                print(f"[THREAT INTELLIGENCE] Found {threat_intelligence_data.get('total_vulnerabilities', 0)} vulnerabilities")
            except Exception as e:
                print(f"[THREAT INTELLIGENCE] Error: {str(e)}")
                threat_intelligence_data = {"status": "error", "message": str(e)}
        elif tool in ["whois", "gobuster"]:
            # For other tools, also attempt threat intelligence if applicable
            try:
                print(f"[THREAT INTELLIGENCE] Analyzing {tool.upper()} output for threat data...")
                threat_intelligence_data = get_threat_intelligence(execution_result["stdout"], tool_type=tool)
                print(f"[THREAT INTELLIGENCE] Found {threat_intelligence_data.get('total_vulnerabilities', 0)} vulnerabilities")
            except Exception as e:
                print(f"[THREAT INTELLIGENCE] Skipped for {tool} (not applicable)")
                threat_intelligence_data = None
        
        # Generate report
        report_gen = ReportGenerator(target, tool, scan_type)
        report_path, report_filename, ti_report_filename = report_gen.generate_report(
            execution_result, ai_analysis, threat_intelligence_data
        )
        
        return jsonify({
            "status": "success",
            "execution": execution_result,
            "analysis": ai_analysis,
            "threat_intelligence": threat_intelligence_data,
            "report_filename": report_filename,
            "ti_report_filename": ti_report_filename
        })
    
    except ValidationError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except ExecutionError as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"Unexpected error: {str(e)}"}), 500

@app.route("/api/parse-command", methods=["POST"])
def parse_voice_command():
    """Parse voice command from frontend."""
    try:
        data = request.get_json()
        command_text = data.get("command", "").strip()
        
        if not command_text:
            return jsonify({"status": "error", "message": "No command provided"}), 400
        
        parsed = parse_command(command_text)
        
        if not parsed["target"]:
            return jsonify({
                "status": "error",
                "message": "Could not parse target from command"
            }), 400
        
        return jsonify({
            "status": "success",
            "parsed": parsed
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/download-report/<filename>", methods=["GET"])
def download_report(filename):
    """Download generated report."""
    try:
        file_path = os.path.join(REPORTS_DIR, filename)
        
        if not os.path.exists(file_path):
            return jsonify({"error": "Report not found"}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("=" * 80)
    print("NARUTO - Cybersecurity Reconnaissance Assistant")
    print("=" * 80)
    print(f"Static files: {STATIC_DIR}")
    print(f"Templates: {TEMPLATES_DIR}")
    print(f"Reports: {REPORTS_DIR}")
    print(f"\nStarting server at http://127.0.0.1:5000")
    print("Press CTRL+C to stop")
    print("=" * 80)
    app.run(host="127.0.0.1", port=5000, debug=False)