import sys
sys.path.insert(0, "..")
from agents.agent1_watcher import Agent1Watcher


def test_brute_force_detection():
    agent = Agent1Watcher()
    log = "Failed password for root from 185.220.101.23 port 22 ssh2"
    result = agent.analyze(log)
    assert result["is_suspicious"] is True
    assert result["threat_type"] == "brute_force"
    assert result["confidence"] > 0
    print("PASS: brute_force detection")


def test_port_scan_detection():
    agent = Agent1Watcher()
    log = "TCP: port scan detected from 51.15.0.100, ports 22,80,443"
    result = agent.analyze(log)
    assert result["is_suspicious"] is True
    assert result["threat_type"] == "port_scan"
    print("PASS: port_scan detection")


def test_normal_log_no_false_positive():
    agent = Agent1Watcher()
    log = "Accepted password for john from 10.0.0.45 port 55432 ssh2"
    result = agent.analyze(log)
    assert result["is_suspicious"] is False
    print("PASS: normal log not flagged")


def test_ip_extraction():
    agent = Agent1Watcher()
    log = "Failed password from 203.0.113.5 port 22"
    result = agent.analyze(log)
    assert result["source_ip"] == "203.0.113.5"
    print("PASS: IP extraction")


def test_private_ip_ignored():
    agent = Agent1Watcher()
    log = "Connection from 192.168.1.100"
    result = agent.analyze(log)
    assert result.get("source_ip") != "192.168.1.100"
    print("PASS: private IP filtering")


def test_multiple_suspicious_lines():
    agent = Agent1Watcher()
    log = (
        "Failed password for root from 1.2.3.4\n"
        "Failed password for admin from 1.2.3.4\n"
        "sudo: authentication failure\n"
    )
    result = agent.analyze(log)
    assert result["is_suspicious"] is True
    assert result["confidence"] > 0.3
    print("PASS: multiple suspicious lines increase confidence")


if __name__ == "__main__":
    test_brute_force_detection()
    test_port_scan_detection()
    test_normal_log_no_false_positive()
    test_ip_extraction()
    test_private_ip_ignored()
    test_multiple_suspicious_lines()
    print("\nAll agent1 tests passed!")
