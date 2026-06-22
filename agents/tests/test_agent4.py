import sys
sys.path.insert(0, "..")
from agents.agent4_action import Agent4Action
from agents.models import AnalysisResult


def test_telegram_format():
    agent = Agent4Action()
    analysis = AnalysisResult(
        alert_id=1,
        threat_type="brute_force",
        severity="high",
        confidence=0.94,
        summary="Someone tried to log into your server 47 times.",
        action_steps=["Change password", "Enable 2FA"],
        source_ip="185.220.101.23",
    )
    result = agent.format_alert(analysis)
    assert "CyberMate Alert" in result.telegram_message
    assert "Source IP" in result.telegram_message
    print("PASS: Telegram message formatted")


def test_email_format():
    agent = Agent4Action()
    analysis = AnalysisResult(
        alert_id=2,
        threat_type="port_scan",
        severity="medium",
        confidence=0.7,
        summary="Port scan detected.",
        action_steps=["Check firewall"],
        source_ip="51.15.0.100",
    )
    result = agent.format_alert(analysis)
    assert "CyberMate" in result.email_subject
    assert "2026" not in result.email_subject
    print(f"PASS: Email formatted — subject: {result.email_subject[:50]}")


def test_critical_has_emoji():
    agent = Agent4Action()
    analysis = AnalysisResult(
        alert_id=3, threat_type="malware", severity="critical",
        summary="Malware detected.", action_steps=["Isolate server"],
    )
    result = agent.format_alert(analysis)
    assert "\U0001f6a8" in result.telegram_message
    print("PASS: Critical severity has red alert emoji")


if __name__ == "__main__":
    test_telegram_format()
    test_email_format()
    test_critical_has_emoji()
    print("\nAll agent4 tests passed!")
