import json
import time
from groq import Groq
from models import AnalysisResult, ThreatIntelResult
from config import config


class Agent3RiskAnalyzer:
    def __init__(self):
        self.client = None
        if config.GROQ_API_KEY:
            self.client = Groq(api_key=config.GROQ_API_KEY)
        self._load_prompts()
        self.use_mock = self.client is None

    def _load_prompts(self):
        try:
            with open("prompts/risk_analysis.txt", "r") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            self.system_prompt = "You are a cybersecurity AI that analyzes server logs and produces plain English summaries."

    def analyze(
        self,
        log_data: str,
        source_ip: str,
        log_type: str,
        watcher_result: dict,
        intel_result: ThreatIntelResult,
    ) -> AnalysisResult:
        result = AnalysisResult(alert_id=0)

        if self.use_mock:
            return self._mock_analysis(result, watcher_result, intel_result)

        return self._groq_analysis(
            result, log_data, source_ip, log_type, watcher_result, intel_result
        )

    def _groq_analysis(
        self,
        result: AnalysisResult,
        log_data: str,
        source_ip: str,
        log_type: str,
        watcher_result: dict,
        intel_result: ThreatIntelResult,
    ) -> AnalysisResult:
        start = time.time()

        user_message = self._build_prompt(
            log_data, source_ip, log_type, watcher_result, intel_result
        )

        try:
            response = self.client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.3,
                max_tokens=1024,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)

            result.threat_type = parsed.get("threat_type", "unknown")
            result.severity = parsed.get("severity", "low")
            result.confidence = parsed.get("confidence", 0.0)
            result.summary = parsed.get("summary", "")
            result.action_steps = parsed.get("action_steps", [])

        except Exception as e:
            print(f"Groq API call failed: {e}")
            result.summary = f"Analysis failed: {str(e)}"
            result.severity = "info"

        result.analysis_time_ms = int((time.time() - start) * 1000)
        return result

    def _mock_analysis(
        self,
        result: AnalysisResult,
        watcher_result: dict,
        intel_result: ThreatIntelResult,
    ) -> AnalysisResult:
        start = time.time()
        threat_type = watcher_result.get("threat_type", "none")
        rep = intel_result.ip_reputation or 0
        country = intel_result.ip_country or "unknown"

        summaries = {
            "none": (
                "No suspicious activity detected in the analyzed logs. "
                "All events appear normal."
            ),
            "brute_force": (
                f"Someone tried to log into your server multiple times from an IP in {country}. "
                f"The IP has a reputation score of {rep} out of 100. "
                "The attempts did not succeed."
            ),
            "port_scan": (
                "An unknown system scanned multiple ports on your server. "
                "This is often done before an attack to find open doors."
            ),
            "data_exfil": (
                "A large data transfer was detected from your server. "
                "This could be a backup or someone copying data without permission."
            ),
            "suspicious_command": (
                "A user ran a command on your server that looks suspicious. "
                "Commands like this are sometimes used by attackers."
            ),
        }

        result.threat_type = threat_type
        result.summary = summaries.get(
            threat_type, f"Unusual activity detected from IP in {country}."
        )

        if threat_type == "none":
            result.action_steps = [
                "No action required at this time",
                "Continue monitoring as usual",
            ]
        else:
            result.action_steps = [
                "Check your server logs for more details",
                f"Review the IP {watcher_result.get('source_ip', 'unknown')}",
                "Contact your team if you did not trigger this activity",
            ]

        severity_map = {
            "none": "info",
            "brute_force": "high",
            "port_scan": "high",
            "data_exfil": "high",
            "suspicious_command": "medium",
            "unauthorized_access": "critical",
        }
        result.severity = severity_map.get(threat_type, "low")
        result.confidence = round(watcher_result.get("confidence", 0.5), 2)
        result.ip_reputation = rep
        result.cve_matches = intel_result.cve_matches
        result.analysis_time_ms = max(int((time.time() - start) * 1000), 1)

        return result

    def _build_prompt(
        self,
        log_data: str,
        source_ip: str,
        log_type: str,
        watcher_result: dict,
        intel_result: ThreatIntelResult,
    ) -> str:
        lines = log_data.strip().split("\n")[:5]
        log_preview = "\n".join(lines)

        prompt = f"Log type: {log_type}\n"
        prompt += f"Source IP: {source_ip or 'unknown'}\n"
        prompt += f"Raw log data:\n{log_preview[:2000]}\n\n"
        prompt += f"Watcher detected: {watcher_result.get('threat_type', 'none')}\n"
        prompt += f"IP reputation: {intel_result.ip_reputation or 'N/A'}\n"
        prompt += f"IP country: {intel_result.ip_country or 'N/A'}\n"
        prompt += f"IP ISP: {intel_result.ip_isp or 'N/A'}\n"
        prompt += f"CVE matches: {', '.join(intel_result.cve_matches) or 'none'}\n"
        prompt += f"OTX pulses: {', '.join(intel_result.otx_pulses) or 'none'}\n"

        return prompt
