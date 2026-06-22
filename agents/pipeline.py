import time
import json
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import LogInput, PipelineResult
from agent1_watcher import Agent1Watcher
from agent2_threat_intel import Agent2ThreatIntel
from agent3_risk_analyzer import Agent3RiskAnalyzer
from agent4_action import Agent4Action
from config import config

app = FastAPI(
    title="CyberMate AI Pipeline",
    description="Multi-agent AI threat detection pipeline API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

watcher = Agent1Watcher()
threat_intel = Agent2ThreatIntel()
risk_analyzer = Agent3RiskAnalyzer()
action_agent = Agent4Action()


class PipelineOrchestrator:
    def run(self, log_input: LogInput) -> PipelineResult:
        pipeline_start = time.time()

        try:
            step1 = watcher.analyze(log_input.log_data, log_input.source_ip)
            step2 = threat_intel.analyze(step1.get("source_ip"))
            step3 = risk_analyzer.analyze(
                log_data=log_input.log_data,
                source_ip=step1.get("source_ip") or "",
                log_type=log_input.log_type,
                watcher_result=step1,
                intel_result=step2,
            )
            step3.alert_id = log_input.alert_id
            step3.source_ip = step1.get("source_ip")
            step3.attempts = step1.get("attempts", 0)
            step3.ip_reputation = step2.ip_reputation
            step3.cve_matches = step2.cve_matches
            step3.ip_country = step2.ip_country
            step3.ip_isp = step2.ip_isp
            step3.otx_pulses = step2.otx_pulses
            step4 = action_agent.format_alert(step3)

            elapsed = int((time.time() - pipeline_start) * 1000)

            return PipelineResult(
                attempts=step1.get("attempts", 0),
                success=True,
                alert_id=log_input.alert_id,
                threat_type=step3.threat_type,
                severity=step3.severity,
                confidence=step3.confidence,
                summary=step3.summary,
                action_steps=step3.action_steps,
                source_ip=step1.get("source_ip"),
                ip_reputation=step2.ip_reputation,
                ip_country=step2.ip_country,
                ip_isp=step2.ip_isp,
                otx_pulses=step2.otx_pulses,
                cve_matches=step2.cve_matches,
                analysis_time_ms=elapsed,
                matched_pattern=step1.get("matched_pattern"),
is_suspicious=step1.get("is_suspicious", False),
watcher_matches=step1.get("matches", []),
            )

        except Exception as e:
            elapsed = int((time.time() - pipeline_start) * 1000)
            return PipelineResult(
                success=False,
                alert_id=log_input.alert_id,
                analysis_time_ms=elapsed,
                error=str(e),
            )


orchestrator = PipelineOrchestrator()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "cybermate-agent-pipeline",
        "version": "1.0.0",
        "agents_loaded": ["watcher", "threat_intel", "risk_analyzer", "action"],
        "groq_configured": bool(config.GROQ_API_KEY),
        "abuseipdb_configured": bool(config.ABUSEIPDB_API_KEY),
        "nvd_configured": bool(config.NVD_API_KEY),
        "otx_configured": bool(config.OTX_API_KEY),
    }


@app.post("/api/analyze", response_model=PipelineResult)
def analyze(log_input: LogInput):
    result = orchestrator.run(log_input)
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)
    return result


@app.post("/api/pipeline/test")
def test_pipeline():
    test_input = LogInput(
        alert_id=999,
        log_data="Failed password for root from 185.220.101.23 port 22 ssh2\n"
        "Failed password for admin from 185.220.101.23 port 22 ssh2\n"
        "Failed password for root from 185.220.101.23 port 22 ssh2",
        source_ip="185.220.101.23",
        log_type="auth",
    )
    return orchestrator.run(test_input)


if __name__ == "__main__":
    print("=" * 50)
    print("CyberMate AI Agent Pipeline")
    print(f"Server: http://{config.HOST}:{config.PORT}")
    print(f"Health: http://{config.HOST}:{config.PORT}/health")
    print(f"Analyze: POST http://{config.HOST}:{config.PORT}/api/analyze")
    print(f"Test:    POST http://{config.HOST}:{config.PORT}/api/pipeline/test")
    print(f"Groq:    {'ON' if config.GROQ_API_KEY else 'OFF (mock)'}")
    print(f"AbuseIPDB: {'ON' if config.ABUSEIPDB_API_KEY else 'OFF (mock)'}")
    print("=" * 50)
    uvicorn.run(app, host=config.HOST, port=config.PORT, log_level=config.LOG_LEVEL.lower())
