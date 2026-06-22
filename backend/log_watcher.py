"""
log_watcher.py
Watches log files for new lines (failed logins etc.) and POSTs them to /api/log.

For the hackathon demo, point LOG_PATHS in .env at a fake log file you control,
since you usually can't read real production server logs during a demo.

Run standalone: python log_watcher.py
"""

import time
import re
import requests
from datetime import datetime
from config import settings

API_URL = f"http://{settings.HOST}:{settings.PORT}/api/log"
IP_PATTERN = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")


def watch_file(path: str):
    print(f"👁  Watching {path} ...")
    try:
        f = open(path, "r")
    except FileNotFoundError:
        print(f"⚠️  File not found: {path}. Create it first (see demo_log_generator.py).")
        return

    f.seek(0, 2)  # jump to end of file, only watch NEW lines

    while True:
        line = f.readline()
        if not line:
            time.sleep(0.5)
            continue
        process_line(line.strip(), path)


def process_line(line: str, source_path: str):
    if "Failed password" not in line and "failed" not in line.lower():
        return  # only care about suspicious lines for now

    ip_match = IP_PATTERN.search(line)
    source_ip = ip_match.group(1) if ip_match else None

    payload = {
        "log_type": "auth",
        "content": line,
        "source_ip": source_ip,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hostname": "demo-server",
    }

    try:
        resp = requests.post(API_URL, json=payload, timeout=10)
        print(f"📤 Sent log to backend -> {resp.status_code}: {line[:60]}")
    except Exception as e:
        print(f"❌ Could not reach backend at {API_URL}: {e}")


if __name__ == "__main__":
    for path in settings.LOG_PATHS:
        watch_file(path.strip())  # NOTE: only watches the first path in this simple version
        break
