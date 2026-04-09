document.addEventListener('DOMContentLoaded', function() {
    console.log("=== NARUTO SCRIPT LOADED (CLEAN) ===");
    
    let currentReportFilename = null;
    let currentTIReportFilename = null;
    let currentAIAnalysis = null;

    // DOM Elements
    const scanButton = document.getElementById("scan-button");
    const voiceButton = document.getElementById("voice-button");
    const clearButton = document.getElementById("clear-output-button");
    const downloadButton = document.getElementById("download-report-button");
    const terminalOutput = document.getElementById("terminal-output");
    const targetInput = document.getElementById("target");
    const toolSelect = document.getElementById("tool");
    const scanTypeSelect = document.getElementById("scan-type");
    const scanTypeSection = document.getElementById("scan-type-section");
    const voiceInputSection = document.getElementById("voice-input-section");
    const voiceInput = document.getElementById("voice-input");
    const sendVoiceBtn = document.getElementById("send-voice-btn");

    console.log("✓ DOM Elements loaded successfully");

    // Voice Recognition Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition;
    let recognition = null;
    
    if (SpeechRecognition) {
        try {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = "en-US";
            recognition.maxAlternatives = 1;
            console.log("✅ SpeechRecognition API initialized");
            appendOutput("✅ Voice recognition ready (allow microphone when prompted)\n");
        } catch (e) {
            console.error("❌ SpeechRecognition initialization failed:", e);
            recognition = null;
        }
    } else {
        console.warn("❌ SpeechRecognition API not available");
        appendOutput("ℹ️ Voice recognition not available - using text input instead\n");
    }
    
    // Update button based on API availability
    if (!recognition) {
        voiceButton.textContent = "⌨️ Text Command";
        voiceButton.title = "Voice not available - click for text input";
    } else {
        voiceButton.title = "Click to speak your command";
    }

    // ===== EVENT LISTENERS (SINGLE ATTACHMENT ONLY) =====
    scanButton.addEventListener("click", executeScan);
    voiceButton.addEventListener("click", startVoiceCommand);
    clearButton.addEventListener("click", clearOutput);
    downloadButton.addEventListener("click", downloadReport);
    
    // Text command input handlers
    if (sendVoiceBtn) {
        sendVoiceBtn.addEventListener("click", handleTextCommand);
    }
    if (voiceInput) {
        voiceInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                handleTextCommand();
            }
        });
    }
    
    // Show/hide scan type based on tool selection
    toolSelect.addEventListener("change", function() {
        const isScanTypeVisible = this.value === "nmap";
        scanTypeSection.style.display = isScanTypeVisible ? "block" : "none";
        if (!isScanTypeVisible) {
            scanTypeSelect.value = "basic";
        }
        console.log(`Tool changed to: ${this.value}, scan-type visible: ${isScanTypeVisible}`);
    });

    // Show/hide port range input based on scan type
    const portRangeSection = document.getElementById("port-range-section");
    const portRangeInput = document.getElementById("port-range");
    
    scanTypeSelect.addEventListener("change", function() {
        const isCustomPorts = this.value === "custom_ports";
        if (portRangeSection) {
            portRangeSection.style.display = isCustomPorts ? "block" : "none";
        }
        if (isCustomPorts && portRangeInput) {
            portRangeInput.focus();
        }
        console.log(`Scan type changed to: ${this.value}, port input visible: ${isCustomPorts}`);
    });

    // ===== VOICE RECOGNITION EVENT HANDLERS =====
    if (recognition) {
        recognition.onstart = () => {
            console.log("🎤 Voice recognition started");
            appendOutput("🎤 Listening for command...\n");
            voiceButton.disabled = true;
            scanButton.disabled = true;
        };

        recognition.onresult = (event) => {
            let transcript = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            console.log(`📝 Recognized: "${transcript}"`);
            appendOutput(`📝 Recognized: "${transcript}"\n`);
            
            if (event.isFinal) {
                parseVoiceCommand(transcript);
            }
        };

        recognition.onerror = (event) => {
            console.error(`❌ Voice error: ${event.error}`);
            appendOutput(`❌ Voice error: ${event.error}\n`);
            appendOutput("⌨️ Falling back to text input\n");
            voiceButton.disabled = false;
            scanButton.disabled = false;
            toggleTextInput(true);
        };

        recognition.onend = () => {
            console.log("🎤 Voice recognition ended");
            voiceButton.disabled = false;
            scanButton.disabled = false;
        };
    }

    // ===== FUNCTION DEFINITIONS (SINGLE DEFINITIONS ONLY) =====

    function startVoiceCommand() {
        if (!recognition) {
            toggleTextInput(true);
            return;
        }
        clearOutput();
        recognition.start();
    }

    function toggleTextInput(show) {
        if (!voiceInputSection) return;
        voiceInputSection.style.display = show ? "block" : "none";
        if (show && voiceInput) {
            voiceInput.focus();
        }
    }

    function handleTextCommand() {
        if (!voiceInput) return;
        const commandText = voiceInput.value.trim();
        if (!commandText) {
            appendOutput("❌ No command entered\n");
            return;
        }
        voiceInput.value = "";
        appendOutput(`📝 Command: "${commandText}"\n`);
        parseVoiceCommand(commandText);
    }

    function parseVoiceCommand(commandText) {
        appendOutput("⚙️ Parsing command...\n");
        
        fetch("/api/parse-command", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command: commandText })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                const parsed = data.parsed;
                appendOutput(`✓ Target: ${parsed.target}\n`);
                appendOutput(`✓ Tool: ${parsed.tool}\n`);
                appendOutput(`✓ Scan Type: ${parsed.scan_type}\n`);
                
                targetInput.value = parsed.target;
                toolSelect.value = parsed.tool;
                scanTypeSelect.value = parsed.scan_type;
                
                // Trigger tool change to show/hide scan type
                toolSelect.dispatchEvent(new Event("change"));
                
                appendOutput("\n🚀 Auto-executing scan...\n");
                toggleTextInput(false);
                executeScan();
            } else {
                appendOutput(`❌ Error: ${data.message}\n`);
            }
        })
        .catch(err => {
            console.error("Parse error:", err);
            appendOutput(`❌ Parsing failed: ${err.message}\n`);
        });
    }

    function executeScan() {
        const target = targetInput.value.trim();
        const tool = toolSelect.value;
        const scanType = scanTypeSelect.value;

        console.log("Executing scan:", { target, tool, scanType });

        if (!target) {
            appendOutput("❌ Target required - Enter IP or domain\n");
            return;
        }

        // Validate custom port range if selected
        if (scanType === "custom_ports") {
            const portRange = portRangeInput.value.trim();
            if (!portRange) {
                appendOutput("❌ Port range required for custom port scan\n");
                appendOutput("Examples: 22 | 1-1000 | 22,80,443\n");
                return;
            }
            appendOutput(`   Port Range: ${portRange}\n`);
        }

        clearOutput();
        appendOutput(`🔍 Initiating ${tool.toUpperCase()} scan...\n`);
        appendOutput(`   Target: ${target}\n`);
        appendOutput(`   Tool: ${tool}\n`);
        appendOutput(`   Scan Type: ${scanType}\n`);
        if (scanType === "custom_ports") {
            appendOutput(`   Port Range: ${portRangeInput.value.trim()}\n`);
        }
        appendOutput("\n📡 Connecting to server...\n");

        scanButton.disabled = true;
        voiceButton.disabled = true;
        scanButton.textContent = "Scanning...";

        const requestBody = { target, tool, scan_type: scanType };
        if (scanType === "custom_ports") {
            requestBody.port_range = portRangeInput.value.trim();
        }

        fetch("/api/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody)
        })
        .then(res => {
            console.log("Response status:", res.status);
            return res.json();
        })
        .then(data => {
            console.log("Scan response:", data);
            scanButton.disabled = false;
            voiceButton.disabled = false;
            scanButton.textContent = "🔍 Execute Scan";

            if (data.status === "success") {
                appendOutput("✓ Scan completed successfully\n\n");
                
                // Show tool output
                appendOutput("===== TOOL OUTPUT =====\n");
                appendOutput(data.execution.stdout || "No output");
                appendOutput("\n");

                if (data.execution.stderr) {
                    appendOutput("===== WARNINGS/ERRORS =====\n");
                    appendOutput(data.execution.stderr);
                    appendOutput("\n");
                }

                // Show AI Analysis
                if (data.analysis && data.analysis.status === "success" && data.analysis.analysis) {
                    currentAIAnalysis = data.analysis.analysis;
                    appendOutput("\n===== AI ANALYSIS =====\n");
                    appendOutput(data.analysis.analysis + "\n");
                    appendOutput("\n✓ AI Analysis available in download\n");
                } else {
                    appendOutput("\n⚠️ AI Analysis not available\n");
                }

                // Show Threat Intelligence (CVE Analysis)
                if (data.threat_intelligence && data.threat_intelligence.status === "success") {
                    const ti = data.threat_intelligence;
                    appendOutput("\n===== THREAT INTELLIGENCE =====\n");
                    appendOutput(`Services Analyzed: ${ti.services_analyzed}\n`);
                    appendOutput(`Total Vulnerabilities Found: ${ti.total_vulnerabilities}\n`);
                    
                    if (ti.threat_data && ti.threat_data.length > 0) {
                        appendOutput("\n🔴 VULNERABILITY SUMMARY:\n");
                        for (const service of ti.threat_data) {
                            appendOutput(`\n📌 ${service.service} v${service.version} (Port ${service.port})\n`);
                            appendOutput(`   Risk Level: ${service.risk_level}\n`);
                            appendOutput(`   CVEs Found: ${service.vulnerability_count}\n`);
                            
                            if (service.cves && service.cves.length > 0) {
                                for (const cve of service.cves) {
                                    appendOutput(`   • ${cve.cve_id} [${cve.severity}] CVSS: ${cve.cvss_score}\n`);
                                    appendOutput(`     ${cve.description.substring(0, 100)}...\n`);
                                }
                            }
                        }
                        appendOutput(`\n✓ Threat Intelligence Analysis Complete\n`);
                    } else {
                        appendOutput(`ℹ️ No vulnerabilities found or services couldn't be extracted\n`);
                        appendOutput(`Tip: Service detection requires open ports with version information\n`);
                    }
                } else if (data.threat_intelligence && data.threat_intelligence.status === "error") {
                    appendOutput(`\n===== THREAT INTELLIGENCE ERROR =====\n`);
                    appendOutput(`⚠️ ${data.threat_intelligence.message}\n`);
                } else if (data.threat_intelligence && data.threat_intelligence.status === "no_data") {
                    appendOutput(`\n===== THREAT INTELLIGENCE =====\n`);
                    appendOutput(`ℹ️ ${data.threat_intelligence.message}\n`);
                }

                // Store report info
                currentReportFilename = data.report_filename;
                currentTIReportFilename = data.ti_report_filename;
                downloadButton.disabled = false;
                
                if (data.ti_report_filename) {
                    appendOutput("\n✓ Reports generated:\n");
                    appendOutput("  1. AI Analysis Report\n");
                    appendOutput("  2. Threat Intelligence Report\n");
                    appendOutput("Click 'Download Report' to save both files.\n");
                } else {
                    appendOutput("\n✓ Report generated: " + data.report_filename + "\n");
                    appendOutput("Click 'Download Report' to save.\n");
                }
            } else {
                appendOutput(`❌ Scan failed: ${data.message}\n`);
            }
        })
        .catch(err => {
            console.error("Scan execution error:", err);
            scanButton.disabled = false;
            voiceButton.disabled = false;
            scanButton.textContent = "🔍 Execute Scan";
            appendOutput(`❌ Execution error: ${err.message}\n`);
        });
    }

    function clearOutput() {
        terminalOutput.textContent = "";
        currentReportFilename = null;
        currentTIReportFilename = null;
        currentAIAnalysis = null;
        downloadButton.disabled = true;
    }

    function downloadReport() {
        if (!currentReportFilename) {
            appendOutput("❌ No report available\n");
            return;
        }
        
        // Download AI Analysis Report
        const link1 = document.createElement("a");
        link1.href = `/api/download-report/${currentReportFilename}`;
        link1.download = currentReportFilename;
        document.body.appendChild(link1);
        link1.click();
        document.body.removeChild(link1);
        appendOutput(`✓ Downloaded: ${currentReportFilename}\n`);
        
        // Download Threat Intelligence Report (if available)
        if (currentTIReportFilename) {
            setTimeout(() => {
                const link2 = document.createElement("a");
                link2.href = `/api/download-report/${currentTIReportFilename}`;
                link2.download = currentTIReportFilename;
                document.body.appendChild(link2);
                link2.click();
                document.body.removeChild(link2);
                appendOutput(`✓ Downloaded: ${currentTIReportFilename}\n`);
            }, 500);
        }
    }

    function appendOutput(text) {
        terminalOutput.textContent += text;
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }

    // Initialize
    appendOutput("NARUTO RECON ASSISTANT - v5 (CLEAN)\n");
    appendOutput("Authorized Testing Only\n");
    appendOutput("Enter a target and select reconnaissance tool to begin.\n\n");
});
