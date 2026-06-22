from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class LogInput(BaseModel):
    alert_id: int
    log_data: str
    source_ip: Optional[str] = None
    log_type: str


class ThreatIntelResult(BaseModel):
    
    ip_reputation: Optional[int] = None
    ip_country: Optional[str] = None
    ip_isp: Optional[str] = None
    cve_matches: list[str] = Field(default_factory=list)
    otx_pulses: list[str] = Field(default_factory=list)
    total_apis_queried: int = 0


class AnalysisResult(BaseModel):
    attempts: int = 0
    
    alert_id: int
    threat_type: str = "unknown"
    severity: str = "low"
    confidence: float = 0.0
    summary: str = ""
    action_steps: list[str] = Field(default_factory=list)
    source_ip: Optional[str] = None
    ip_reputation: Optional[int] = None
    ip_country: Optional[str] = None
    ip_isp: Optional[str] = None
    otx_pulses: list[str] = Field(default_factory=list)
    cve_matches: list[str] = Field(default_factory=list)
    analysis_time_ms: int = 0
    

    def to_pipeline_output(self) -> dict:
        return {
            "alert_id": self.alert_id,
            "threat_type": self.threat_type,
            "severity": self.severity,
            "confidence": self.confidence,
            "summary": self.summary,
            "action_steps": self.action_steps,
            "source_ip": self.source_ip,
            "ip_reputation": self.ip_reputation,
            "ip_country": self.ip_country,
            "ip_isp": self.ip_isp,
            "otx_pulses": self.otx_pulses,
            "cve_matches": self.cve_matches,
            "analysis_time_ms": self.analysis_time_ms,
        }


class FormattedAlert(BaseModel):
    alert_id: int
    telegram_message: str
    email_subject: str
    email_body: str
    severity: str
    threat_type: str
    raw_summary: str
    action_steps: list[str]


class PipelineResult(BaseModel):
    success: bool
    alert_id: int
    threat_type: str = "unknown"
    severity: str = "low"
    confidence: float = 0.0
    attempts: int = 0
    summary: str = ""
    action_steps: list[str] = Field(default_factory=list)
    source_ip: Optional[str] = None
    ip_reputation: Optional[int] = None
    ip_country: Optional[str] = None
    ip_isp: Optional[str] = None
    otx_pulses: list[str] = Field(default_factory=list)
    cve_matches: list[str] = Field(default_factory=list)
    analysis_time_ms: int = 0
    error: Optional[str] = None
    matched_pattern: Optional[str] = None
    is_suspicious: bool = False
    watcher_matches: list[str] = Field(default_factory=list)
