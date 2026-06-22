import sys
sys.path.insert(0, "..")
from agents.pipeline import PipelineOrchestrator, LogInput


def test_pipeline_brute_force():
    pipeline = PipelineOrchestrator()
    result = pipeline.run(
        LogInput(
            alert_id=100,
            log_data="Failed password for root from 185.220.101.23 port 22 ssh2\n"
            "Failed password for admin from 185.220.101.23",
            source_ip="185.220.101.23",
            log_type="auth",
        )
    )
    assert result.success is True
    assert result.threat_type == "brute_force"
    assert result.severity in ["high", "critical"]
    assert result.confidence > 0
    assert len(result.summary) > 0
    assert len(result.action_steps) > 0
    assert result.analysis_time_ms >= 0
    print(f"PASS: pipeline returned {result.threat_type} ({result.severity}) in {result.analysis_time_ms}ms")


def test_pipeline_normal_log():
    pipeline = PipelineOrchestrator()
    result = pipeline.run(
        LogInput(
            alert_id=101,
            log_data="Accepted password for john from 10.0.0.45 port 55432 ssh2",
            source_ip="10.0.0.45",
            log_type="auth",
        )
    )
    assert result.success is True
    print(f"PASS: normal log processed without error")


def test_pipeline_missing_fields():
    pipeline = PipelineOrchestrator()
    result = pipeline.run(
        LogInput(
            alert_id=102,
            log_data="Test log line",
            log_type="syslog",
        )
    )
    assert result.success is True
    print("PASS: pipeline handles missing optional fields")


if __name__ == "__main__":
    test_pipeline_brute_force()
    test_pipeline_normal_log()
    test_pipeline_missing_fields()
    print("\nAll pipeline tests passed!")
