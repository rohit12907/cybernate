"""
database.py
All SQLite database operations. Raw SQL, no ORM (keeps it simple for hackathon).
"""

import sqlite3
import json
from datetime import datetime
from config import settings


def get_connection():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    
    
    """Create the alerts table if it doesn't exist. Call this once on startup."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            
            attempts INTEGER DEFAULT 0,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_type TEXT NOT NULL,
            content TEXT NOT NULL,
            source_ip TEXT DEFAULT NULL,
            threat_type TEXT DEFAULT NULL,
            severity TEXT DEFAULT NULL,
            confidence REAL DEFAULT NULL,
            summary TEXT DEFAULT NULL,
            action_steps TEXT DEFAULT NULL,
            ip_reputation INTEGER DEFAULT NULL,
            ip_country TEXT DEFAULT NULL,
            ip_isp TEXT DEFAULT NULL,
            otx_pulses TEXT DEFAULT NULL,
            cve_matches TEXT DEFAULT NULL,
            delivered INTEGER NOT NULL DEFAULT 0,
            channel TEXT DEFAULT NULL,
            delivered_at TEXT DEFAULT NULL,
            analysis_time_ms INTEGER DEFAULT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    existing_columns = {
        row["name"] for row in conn.execute("PRAGMA table_info(alerts)").fetchall()
    }
    for column_name, column_type in (
        ("ip_country", "TEXT DEFAULT NULL"),
        ("ip_isp", "TEXT DEFAULT NULL"),
        ("otx_pulses", "TEXT DEFAULT NULL"),
    ):
        if column_name not in existing_columns:
            conn.execute(
                f"ALTER TABLE alerts ADD COLUMN {column_name} {column_type}"
            )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_severity ON alerts(severity)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON alerts(created_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_delivered ON alerts(delivered)")
    conn.commit()
    conn.close()


def insert_log(log_type: str, content: str, source_ip: str | None) -> int:
    """Insert a raw log entry. Returns the new alert_id."""
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO alerts (log_type, content, source_ip) VALUES (?, ?, ?)",
        (log_type, content, source_ip),
    )
    conn.commit()
    alert_id = cur.lastrowid
    conn.close()
    return alert_id


def update_analysis(alert_id: int, analysis: dict):
    """Save the AI pipeline's analysis result onto an existing alert row."""
    conn = get_connection()
    conn.execute(
        """
        UPDATE alerts
     SET threat_type = ?, severity = ?, confidence = ?, attempts = ?, summary = ?,
            action_steps = ?, ip_reputation = ?, ip_country = ?, ip_isp = ?,
            otx_pulses = ?, cve_matches = ?,
            analysis_time_ms = ?
        WHERE id = ?
        """,
        (
            analysis.get("threat_type"),
            analysis.get("severity"),
            analysis.get("confidence"),
            analysis.get("attempts", 0),
            analysis.get("summary"),
            json.dumps(analysis.get("action_steps", [])),
            analysis.get("ip_reputation"),
            analysis.get("ip_country"),
            analysis.get("ip_isp"),
            json.dumps(analysis.get("otx_pulses", [])),
            json.dumps(analysis.get("cve_matches", [])),
            analysis.get("analysis_time_ms"),
            alert_id,
        ),
    )
    conn.commit()
    conn.close()


def mark_delivered(alert_id: int, channel: str):
    conn = get_connection()
    conn.execute(
        "UPDATE alerts SET delivered = 1, channel = ?, delivered_at = ? WHERE id = ?",
        (channel, datetime.utcnow().isoformat() + "Z", alert_id),
    )
    conn.commit()
    conn.close()


def get_threats(limit: int = 20, severity: str = "all", offset: int = 0):
    
    conn = get_connection()
    if severity == "all":
        rows = conn.execute(
            "SELECT * FROM alerts ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM alerts WHERE severity = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (severity, limit, offset),
        ).fetchall()
    conn.close()

    threats = []
    for r in rows:
        threats.append({
            "analysis_time_ms": r["analysis_time_ms"],
            "id": r["id"],
            "ip": r["source_ip"],
            "type": r["threat_type"],
            "severity": r["severity"],
           "attempts": r["attempts"],
            "summary": r["summary"],
            "action_steps": json.loads(r["action_steps"]) if r["action_steps"] else [],
            "timestamp": r["created_at"],
            "delivered": bool(r["delivered"]),
            "channel": r["channel"],
            "confidence": r["confidence"],
"summary": r["summary"],
"ip_reputation": r["ip_reputation"],
"ip_country": r["ip_country"],
"ip_isp": r["ip_isp"],
"otx_pulses": json.loads(r["otx_pulses"]) if r["otx_pulses"] else [],
"cve_matches": json.loads(r["cve_matches"]) if r["cve_matches"] else [],
        })
    return threats


def get_alert_by_id(alert_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def count_today():
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) as c FROM alerts WHERE date(created_at) = date('now')"
    ).fetchone()
    conn.close()
    return row["c"]

