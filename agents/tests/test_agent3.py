import sys
sys.path.insert(0, "..")
from agents.agent3_risk_analyzer import Agent3RiskAnalyzer
from agents.models import ThreatIntelResult


def test_mock_analysis():
    agent = Agent3RiskAnalyzer()
    agent.use_mock = True
    intel = ThreatIntelResult(
        ip_reputation=94,
        ip_country="Romania",
        cve_matches=["CVE-2024-6387"],
        otx_pulses=["SSH Campaign"],
    )
    result = agent.analyze(
        log_data="Failed password for root from 185.220.101.23",
        source_ip="185.220.101.23",
        log_type="auth",
        watcher_result={"threat_type": "brute_force", "confidence": 0.85},
        intel_result=intel,
    )
    assert result.threat_type == "brute_force"
    assert result.severity == "high"
    assert len(result.summary) > 0
    assert len(result.action_steps) > 0
    print(f"PASS: mock analysis — {result.threat_type}, {result.severity}")


def test_mock_summary_contains_country():
    agent = Agent3RiskAnalyzer()
    agent.use_mock = True
    intel = ThreatIntelResult(
        ip_reputation=94, ip_country="Romania"
    )
    result = agent.analyze(
        log_data="Failed password",
        source_ip="185.220.101.23",
        log_type="auth",
        watcher_result={"threat_type": "brute_force", "confidence": 0.8},
        intel_result=intel,
    )
    assert "Romania" in result.summary
    print("PASS: summary contains country name")


if __name__ == "__main__":
    test_mock_analysis()
    test_mock_summary_contains_country()
    print("\nAll agent3 tests passed!")
