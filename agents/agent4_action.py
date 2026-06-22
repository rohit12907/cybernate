import time
from models import AnalysisResult, FormattedAlert


class Agent4Action:
    def format_alert(self, analysis: AnalysisResult) -> FormattedAlert:
        sev_emoji = {
            "critical": "\U0001f6a8",
            "high": "\u26a0\ufe0f",
            "medium": "\U0001f50d",
            "low": "\u2139\ufe0f",
            "info": "\u2139\ufe0f",
        }

        emoji = sev_emoji.get(analysis.severity, "\u2139\ufe0f")

        telegram = f"{emoji} CyberMate Alert: {analysis.threat_type.upper()}\n\n"
        telegram += f"{analysis.summary}\n\n"
        if analysis.action_steps:
            telegram += "What to do:\n"
            for i, step in enumerate(analysis.action_steps, 1):
                telegram += f"{i}. {step}\n"
        telegram += f"\nSource IP: {analysis.source_ip or 'N/A'}"

        email_subject = (
            f"[{analysis.severity.upper()}] CyberMate Alert "
            f"\u2014 {analysis.threat_type} detected on your server"
        )

        email_body = f"CyberMate Alert\n"
        email_body += f"Severity: {analysis.severity.upper()}\n"
        email_body += f"Threat Type: {analysis.threat_type}\n"
        email_body += f"{'='*40}\n\n"
        email_body += f"{analysis.summary}\n\n"
        if analysis.action_steps:
            email_body += "Recommended Actions:\n"
            for i, step in enumerate(analysis.action_steps, 1):
                email_body += f"{i}. {step}\n"
        email_body += f"\nSource IP: {analysis.source_ip or 'N/A'}"
        email_body += f"\nConfidence: {analysis.confidence:.0%}"
        email_body += f"\n\nThis alert was generated automatically by CyberMate."

        return FormattedAlert(
            alert_id=analysis.alert_id,
            telegram_message=telegram.strip(),
            email_subject=email_subject.strip(),
            email_body=email_body.strip(),
            severity=analysis.severity,
            threat_type=analysis.threat_type,
            raw_summary=analysis.summary,
            action_steps=analysis.action_steps,
        )
