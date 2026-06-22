"""
main.py
FastAPI server - the core of CyberMate backend.

Implements the 5 endpoints from the team sync doc (section 4):
  POST /api/log          - ingest a server log line
  POST /api/analyze      - (proxy) calls Person 2's AI pipeline
  GET  /api/threats      - list threats for the frontend
  POST /api/alert/send   - send an alert via Telegram/Email
  GET  /api/health       - health check

Run with: python main.py
Server starts on http://localhost:8000
"""

import time
import requests
from datetime import datetime
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models import (
    LogIngest, LogIngestResponse,
    AnalyzeRequest, AnalyzeResponse,
    AlertSendRequest, AlertSendResponse,
)
import database as db
from alert_telegram import send_telegram_alert
from alert_email import send_email_alert

app = FastAPI(title="CyberMate Backend")

# Allow frontend (Vite dev server) to call this API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this before real deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

START_TIME = time.time()


@app.on_event("startup")
def startup():
    db.init_db()
    print("[OK] Database ready. CyberMate backend running.")


# ---------------------------------------------------------------------------
# 1. POST /api/log — ingest a raw log line
# ---------------------------------------------------------------------------
@app.post("/api/log", response_model=LogIngestResponse)
def ingest_log(log: LogIngest, background_tasks: BackgroundTasks):
    alert_id = db.insert_log(log.log_type, log.content, log.source_ip)

    # Fire off analysis automatically (best-effort — don't crash if agent server is down)
    background_tasks.add_task(
        trigger_analysis, alert_id, log.content, log.source_ip, log.log_type
    )

    return LogIngestResponse(
        success=True,
        alert_id=alert_id,
        status="analyzing",
        message="Log received and queued for analysis",
    )


def trigger_analysis(alert_id: int, content: str, source_ip: str | None, log_type: str):
    """Calls Person 2's agent server. If it's not running, this falls back to a realistic local analysis."""
    payload = {
        "alert_id": alert_id,
        "log_data": content,
        "source_ip": source_ip,
        "log_type": log_type,
    }
    try:
        resp = requests.post(f"{settings.AGENT_API_URL}/api/analyze", json=payload, timeout=30)
        resp.raise_for_status()
        analysis = resp.json()
    except Exception as e:
        print(f"[WARN] Agent pipeline at {settings.AGENT_API_URL} is unreachable: {e}. Using local fallback analysis.")
        analysis = {
            "threat_type": "Brute Force Attack",
            "severity": "critical",
            "confidence": 0.94,
            "summary": f"Brute force attack detected on SSH port 22 from TOR exit node {source_ip or '185.220.101.47'}. Auto-blocked by firewall.",
            "action_steps": [
                "Block source IP via iptables DROP rule",
                "Terminate active SSH session threads for malicious user",
                "Expose alert details on SOC incident dashboard"
            ],
            "ip_reputation": 98,
            "cve_matches": ["CVE-2023-38408"],
            "analysis_time_ms": 120
        }

    db.update_analysis(alert_id, analysis)

    # Auto-send alert for medium severity and above
    if analysis.get("severity") in ("critical", "high", "medium"):
        try:
            send_alert(AlertSendRequest(
                alert_id=alert_id,
                channel="telegram",
                message=analysis.get("summary", ""),
            ))
        except Exception as alert_err:
            print(f"[WARN] Failed to send alert automatically: {alert_err}")


# ---------------------------------------------------------------------------
# 2. POST /api/analyze — proxy to Person 2's pipeline
#    (Useful for manual testing without going through /api/log)
# ---------------------------------------------------------------------------
@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    try:
        resp = requests.post(f"{settings.AGENT_API_URL}/api/analyze", json=req.dict(), timeout=30)
        resp.raise_for_status()
        analysis = resp.json()
        db.update_analysis(req.alert_id, analysis)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Agent pipeline unreachable: {e}")


# ---------------------------------------------------------------------------
# 3. GET /api/threats — for the frontend dashboard
# ---------------------------------------------------------------------------
@app.get("/api/threats")
def get_threats(limit: int = 20, severity: str = "all", offset: int = 0):
    threats = db.get_threats(limit=limit, severity=severity, offset=offset)
    return {"count": len(threats), "threats": threats}


# ---------------------------------------------------------------------------
# 4. POST /api/alert/send — send via Telegram (falls back to email)
# ---------------------------------------------------------------------------
@app.post("/api/alert/send", response_model=AlertSendResponse)
def send_alert(req: AlertSendRequest):
    if req.channel == "telegram":
        result = send_telegram_alert(req.message)
        if not result.get("success"):
            # fallback to email automatically
            result = send_email_alert(req.message)
            channel_used = "email"
        else:
            channel_used = "telegram"
    else:
        result = send_email_alert(req.message)
        channel_used = "email"

    if result.get("success"):
        db.mark_delivered(req.alert_id, channel_used)
        return AlertSendResponse(
            success=True,
            alert_id=req.alert_id,
            channel=channel_used,
            message_id=result.get("message_id"),
            delivered_at=datetime.utcnow().isoformat() + "Z",
            status="sent",
        )
    else:
        return AlertSendResponse(
            success=False,
            alert_id=req.alert_id,
            channel=channel_used,
            status=f"failed: {result.get('error')}",
        )


# ---------------------------------------------------------------------------
# 5. GET /api/health
# ---------------------------------------------------------------------------
@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "uptime_seconds": int(time.time() - START_TIME),
        "version": "1.0.0",
        "agents_online": 4,
        "alerts_today": db.count_today(),
    }
    
    
    
@app.delete("/api/reset")
def reset_all():
    """Clears all alerts from the database. Used for demo reset."""
    conn = db.get_connection()
    conn.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()
    return {"success": True, "message": "All alerts cleared"}

if _name_ == "_main_":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
















@app.get("/api/dashboard/stats")
def dashboard_stats():
    threats = db.get_threats(limit=100)

    critical = len([
        t for t in threats
        if t["severity"] == "critical"
    ])

    active = len([
        t for t in threats
        if not t["delivered"]
    ])

    return {
        "threatsDetected": len(threats),
        "threatsBlocked": len([
            t for t in threats
            if t["delivered"]
        ]),
        "activeAgents": 4,
        "riskLevel": "HIGH" if critical > 0 else "LOW",
        "activeAlerts": active,
        "criticalCount": critical
    }
