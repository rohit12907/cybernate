import sys
sys.path.insert(0, "..")
from agents.agent2_threat_intel import Agent2ThreatIntel


def test_mock_abuseipdb():
    agent = Agent2ThreatIntel()
    agent.use_mock = True
    result = agent.analyze("185.220.101.23")
    assert result.total_apis_queried > 0
    assert result.ip_reputation is not None
    print(f"PASS: mock AbuseIPDB returned reputation {result.ip_reputation}")


def test_mock_nvd():
    agent = Agent2ThreatIntel()
    agent.use_mock = True
    result = agent.analyze("185.220.101.23")
    assert len(result.cve_matches) > 0
    print(f"PASS: mock NVD returned CVEs: {result.cve_matches}")


def test_mock_otx():
    agent = Agent2ThreatIntel()
    agent.use_mock = True
    result = agent.analyze("185.220.101.23")
    assert len(result.otx_pulses) > 0
    print(f"PASS: mock OTX returned pulses: {result.otx_pulses}")


def test_empty_ip():
    agent = Agent2ThreatIntel()
    agent.use_mock = True
    result = agent.analyze(None)
    assert result.ip_reputation is None
    print("PASS: empty IP returns empty result")


if __name__ == "__main__":
    test_mock_abuseipdb()
    test_mock_nvd()
    test_mock_otx()
    test_empty_ip()
    print("\nAll agent2 tests passed!")
