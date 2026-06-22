"""
demo_log_generator.py
Since you can't show a REAL hacked server during a demo, this script
writes fake "Failed password" lines into a local file every few seconds.
Run this alongside log_watcher.py (which should watch the same file).

Usage:
  1. Set LOG_PATHS=demo_auth.log in backend/.env
  2. Terminal 1: python demo_log_generator.py
  3. Terminal 2: python log_watcher.py
  4. Terminal 3: python main.py
"""

import time
import random
from datetime import datetime

FAKE_IPS = ["185.220.101.23", "91.234.56.78", "45.33.32.156", "103.21.244.10"]
USERNAMES = ["root", "admin", "ubuntu", "test"]
LOG_FILE = "demo_auth.log"

if __name__ == "__main__":
    print(f"✍️  Writing fake failed logins to {LOG_FILE} every 3-6 seconds. Ctrl+C to stop.")
    with open(LOG_FILE, "a") as f:
        while True:
            ip = random.choice(FAKE_IPS)
            user = random.choice(USERNAMES)
            timestamp = datetime.now().strftime("%b %d %H:%M:%S")
            line = f"{timestamp} demo-server sshd[1234]: Failed password for {user} from {ip} port 22 ssh2\n"
            f.write(line)
            f.flush()
            print(f"   wrote: {line.strip()}")
            time.sleep(random.randint(3, 6))
