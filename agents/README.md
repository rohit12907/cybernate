# CyberMate — AI Agent Pipeline

Multi-agent AI threat detection pipeline that watches server logs, cross-checks threats against global databases, and produces plain-English alerts.

## Architecture

```
Log Data → Agent 1 (Watcher) → Agent 2 (Threat Intel) → Agent 3 (Risk Analyzer) → Agent 4 (Action) → Alert
```

Four agents run in sequence:

| Agent | File | Role | Input | Output |
|-------|------|------|-------|--------|
| 1. Log Watcher | `agent1_watcher.py` | Detects anomalies in raw logs | Log text | Threat type + confidence score |
| 2. Threat Intel | `agent2_threat_intel.py` | Cross-checks IPs against 3 databases | Source IP | IP reputation + CVE matches |
| 3. Risk Analyzer | `agent3_risk_analyzer.py` | Groq AI turns data into plain English | Watcher + Intel results | Summary + action steps |
| 4. Action Agent | `agent4_action.py` | Formats alert for delivery channels | Analysis result | Telegram + Email ready messages |

## Quick Start

### 1. Setup

```bash
cd agents
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your API keys
# At minimum: GROQ_API_KEY and ABUSEIPDB_API_KEY
```

### 3. Run Tests

```bash
python -m pytest tests/ -v
```

### 4. Start Server

```bash
python pipeline.py
```

Server starts on `http://localhost:8001`

## API Endpoints

### POST /api/analyze

Main endpoint. Person 1's backend calls this after receiving a log.

```json
{
  "alert_id": 123,
  "log_data": "Failed password for root from 185.220.101.23 port 22 ssh2",
  "source_ip": "185.220.101.23",
  "log_type": "auth"
}
```

Response:

```json
{
  "success": true,
  "alert_id": 123,
  "threat_type": "brute_force",
  "severity": "high",
  "confidence": 0.94,
  "summary": "Someone tried to log into your server 47 times from an IP in Romania...",
  "action_steps": ["Change password", "Enable 2FA", "Block IP"],
  "source_ip": "185.220.101.23",
  "ip_reputation": 94,
  "analysis_time_ms": 340
}
```

### GET /health

Returns pipeline health status.

### POST /api/pipeline/test

Runs the pipeline with mock data for testing.

## Project Structure

```
agents/
├── pipeline.py                 # FastAPI server + orchestrator
├── agent1_watcher.py           # Log anomaly detection
├── agent2_threat_intel.py      # AbuseIPDB + NVD + OTX clients
├── agent3_risk_analyzer.py     # Groq AI integration
├── agent4_action.py            # Alert formatting
├── config.py                   # Environment config
├── models.py                   # Pydantic data models
├── prompts/
│   ├── risk_analysis.txt       # Groq system prompt
│   └── action_format.txt       # Alert formatting prompt
├── tests/
│   ├── test_agent1.py          # 6 tests
│   ├── test_agent2.py          # 4 tests
│   ├── test_agent3.py          # 2 tests
│   ├── test_agent4.py          # 3 tests
│   └── test_pipeline.py        # 3 tests
├── mock_data/
│   ├── sample_logs.txt         # 25 sample log lines
│   └── test_responses.json     # Mock API responses
├── requirements.txt
├── .env.example
└── README.md
```

## Free APIs Used

| API | Tier | Limit | Purpose |
|-----|------|-------|---------|
| Groq (Llama 3.1) | Free | 14,400 req/day | AI text analysis |
| AbuseIPDB | Free | 1,000 lookups/day | IP reputation scoring |
| NVD (NIST) | Free | Rate limited | CVE vulnerability lookup |
| AlienVault OTX | Free | Unlimited | Threat intelligence pulses |

## Integration with Backend

Person 1's FastAPI server calls this pipeline via POST /api/analyze:

```
Person 1 (Backend)                     Person 2 (Agents)
     │                                      │
     │  POST /api/log                        │
     │  (receives raw log)                   │
     │                                      │
     │  POST /api/analyze ──────────────────►│
     │  (sends log + IP)                    │  Agent 1: Watcher
     │                                      │  Agent 2: Threat Intel
     │                                      │  Agent 3: Groq AI
     │◄─────────────────────────────────────│  Agent 4: Format
     │  (returns analysis)                   │
     │                                      │
     │  Stores in SQLite                     │
     │  Sends Telegram/Email                 │
     │  GET /api/threats ◄─── Frontend       │
```

## Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_agent1.py -v

# Run with coverage
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=term-missing
```

All 18 tests pass with mock data (no API keys needed).
