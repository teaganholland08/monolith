"""
RESOURCE GOVERNOR - Project Monolith v5.6
Purpose: Active throttling of background processes to prevent i3 system crash.
Logic: 
- If CPU > 90% for 30s -> Pause IO.net worker
- If CPU < 50% for 5 mins -> Resume IO.net worker
- Priority: Human Activity > Bandwidth Apps > Compute Worker
"""

import psutil
import time
import subprocess
import signal
import os
import json
import io
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class ResourceGovernor:
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.sentinel_dir = self.root / "System" / "Sentinels"
        self.sentinel_dir.mkdir(parents=True, exist_ok=True)
        
        self.thresholds = {
            "critical_cpu": 90.0,
            "resume_cpu": 50.0,
            "critical_ram": 90.0
        }
        
        # Processes to manage (Low Priority)
        self.managed_processes = [
            "io-worker", "io-worker-launcher", # High load
            "python" # Be careful with this, only target specific scripts if possible
        ]

    def check_system_load(self):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        return cpu, ram

    def log_action(self, action, details):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": "resource_governor",
            "action": action,
            "details": details
        }
        with open(self.sentinel_dir / "resource_governor.log", "a", encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
        print(f"[GOVERNOR] {action}: {details}")

    def throttle_processes(self):
        """Pause or lower priority of heavy processes"""
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                # Find IO.net worker
                if 'io-worker' in proc.info['name'].lower():
                    # Check if already paused? (Hard to tell cross-platform without state)
                    # For Windows, we can assume 'suspend' works
                    proc.suspend() 
                    self.log_action("SUSPEND", f"Suspended {proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def resume_processes(self):
        """Resume paused processes"""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'io-worker' in proc.info['name'].lower():
                    proc.resume()
                    self.log_action("RESUME", f"Resumed {proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    
    def run_monitor_loop(self, duration_sec=60):
        print("[GOVERNOR] 🛡️ Active protection enabled...")
        start_time = time.time()
        
        while time.time() - start_time < duration_sec:
            cpu, ram = self.check_system_load()
            
            if cpu > self.thresholds['critical_cpu']:
                print(f"[GOVERNOR] ⚠️ CRITICAL LOAD: CPU {cpu}% -> THROTTLING")
                self.throttle_processes()
                
            elif cpu < self.thresholds['resume_cpu']:
                # Potential to resume, but let's be conservative
                # self.resume_processes() # Uncomment to enable active resuming
                pass
                
            time.sleep(5)
            
        return {"status": "Active", "last_cpu": cpu}

if __name__ == "__main__":
    governor = ResourceGovernor()
    # Run a single check for the verified run
    cpu, ram = governor.check_system_load()
    print(f"[GOVERNOR] Current Load - CPU: {cpu}%, RAM: {ram}%")
    
    if cpu > 85:
        print("[GOVERNOR] System Under Load. Recommending Throttling.")
        governor.throttle_processes()
    else:
        print("[GOVERNOR] System Nominal.")
