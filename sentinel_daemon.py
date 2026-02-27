"""
SENTINEL DAEMON v1.0
INDIVIDUAL PROCESS - WATCHDOG
Monitors:
1. Financial Drift (Ledger Scan)
2. Process Liveness (Heartbeat)
3. God Rule Violations

Authority:
- Can KILL the Main Process
- Can LOCK the Ledger
"""

import sys
import time
import json
import sqlite3
import psutil
import os
import io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- Configuration ---
ROOT = Path(__file__).parent.parent.parent
LEDGER_PATH = ROOT / "System" / "Logs" / "ledger.db"
CONFIG_PATH = ROOT / "System" / "Config" / "treasurer_god_rules.json"
HEARTBEAT_FILE = ROOT / "System" / "Logs" / "system_heartbeat.json"

class SentinelDaemon:
    def __init__(self):
        self.running = True
        self.rules = self._load_rules()
        self.main_pid = None
        
        print("\n" + "="*50)
        print("👁️ SENTINEL DAEMON: ONLINE")
        print("="*50)
        print(f"   [Buffer Limit]: ${self.rules.get('survival_buffer', 20000)}")
        print(f"   [Daily Limit] : ${self.rules.get('daily_spend_limit', 1000)}")
        
    def _load_rules(self):
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def find_main_process(self):
        """Find the main Monolith Omega process"""
        # Look for heartbeat file pid
        if HEARTBEAT_FILE.exists():
            try:
                with open(HEARTBEAT_FILE, 'r') as f:
                    data = json.load(f)
                    pid = data.get("pid")
                    if pid and psutil.pid_exists(pid):
                        self.main_pid = pid
                        return pid
            except:
                pass
        return None

    def check_financial_health(self):
        """Query Ledger directly"""
        if not LEDGER_PATH.exists():
            return True # Nothing to complain about yet

        try:
            conn = sqlite3.connect(LEDGER_PATH)
            c = conn.cursor()
            
            # Check Daily Spend
            today = datetime.now().strftime("%Y-%m-%d")
            c.execute("""
                SELECT SUM(amount) FROM transactions 
                WHERE type='EXPENSE' AND timestamp LIKE ?
            """, (f"{today}%",))
            res = c.fetchone()
            daily_spend = res[0] if res and res[0] else 0.0
            
            if daily_spend > self.rules.get("daily_spend_limit", 1000.0):
                print(f"   [ALERT] 💸 Daily Spend Limit Exceeded: ${daily_spend}")
                self.trigger_emergency_protocol("DAILY_SPEND_EXCEEDED")
                
            conn.close()
        except Exception as e:
            print(f"   [ERROR] Ledger Check Failed: {e}")

    def check_heartbeat(self):
        """Ensure Omega is alive (if it should be)"""
        # If we found a PID before, check if it's still there
        if self.main_pid:
            if not psutil.pid_exists(self.main_pid):
                print(f"   [ALERT] 💀 Main Process (PID {self.main_pid}) Vanished!")
                self.trigger_recovery()
                self.main_pid = None
        else:
             # Try to find it
             pid = self.find_main_process()
             if pid:
                 print(f"   [INFO] Found Main Process: {pid}")

    def trigger_emergency_protocol(self, reason):
        print(f"   🔴 TRIGGERING EMERGENCY STOP: {reason}")
        # Implementation: Create a 'LOCK' file or Kill process
        lock_file = ROOT / "System" / "STOP.lock"
        with open(lock_file, 'w') as f:
            f.write(f"LOCKED_BY_SENTINEL: {reason}\nTimestamp: {datetime.now()}")
            
        if self.main_pid:
            try:
                p = psutil.Process(self.main_pid)
                p.terminate()
                print("   [ACTION] Killed Main Process.")
            except:
                pass

    def trigger_recovery(self):
        print("   [ACTION] Attempting Recovery... (Placeholder)")
        # In future: launch monolith_omega.py again

    def loop(self):
        while self.running:
            self.check_heartbeat()
            self.check_financial_health()
            
            # Check for config updates
            time.sleep(5)

if __name__ == "__main__":
    daemon = SentinelDaemon()
    try:
        daemon.loop()
    except KeyboardInterrupt:
        print("\n👁️ Sentinel Offline.")
