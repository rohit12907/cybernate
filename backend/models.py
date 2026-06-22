"""
models.py
Pydantic models matching the API contract in the team sync doc (section 4).
"""

from pydantic import BaseModel
from typing import Optional, List


class LogIngest(BaseModel):
    """POST /api/log request body"""
    log_type: str
    content: str
    source_ip: Optional[str] = None
    timestamp: str
    hostname: Optional[str] = "localhost"


class LogIngestResponse(BaseModel):
    success: bool
    alert_id: int
    status: str
    message: str


class AnalyzeRequest(BaseModel):
    """What backend sends to Person 2's /api/analyze"""
    alert_id: int
    log_data: str
    source_ip: Optional[str] = None
    log_type: str


class AnalyzeResponse(BaseModel):
    """What Person 2's pipeline returns"""
    alert_id: int
    threat_type: str
    severity: str
    confidence: float
    summary: str
    action_steps: List[str]
    source_ip: Optional[str] = None
    ip_reputation: Optional[int] = None
    ip_country: Optional[str] = None
    ip_isp: Optional[str] = None
    otx_pulses: Optional[List[str]] = []
    cve_matches: Optional[List[str]] = []
    analysis_time_ms: Optional[int] = None


class AlertSendRequest(BaseModel):
    alert_id: int
    channel: str  # "telegram" or "email"
    message: str


class AlertSendResponse(BaseModel):
    success: bool
    alert_id: int
    channel: str
    message_id: Optional[int] = None
    delivered_at: Optional[str] = None
    status: str
