"""
AGENT OPS - OBSERVER LAYER v1.0
Real-time telemetry and health monitoring for Monolith Agents.
Prevents "Zombie Loops" and tracks automated efficiency.
"""
import json
import time
import os
import psutil
from datetime import datetime
from pathlib import Path

class AgentOps:
    def __init__(self):
        self.root = Path(__file__).parents[2] # Go up from System/Core
        self.log_path = self.root / "Logs" / "agent_telemetry.json"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
    def log_run(self, agent_name, status, duration, output=None, earnings=0.0):
        """Log a single agent execution event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "status": status,
            "duration_sec": round(duration, 2),
            "earnings": earnings,
            "system_cpu": psutil.cpu_percent(),
            "system_ram": psutil.virtual_memory().percent,
            "output_snippet": str(output)[:200] if output else ""
        }
        
        # Append to log file (JSONL format for speed)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
            
    def check_drift(self, agent_name):
        """
        Check if an agent is 'drifting' (failing repeatedly or running too long).
        Returns (is_drifting, reason)
        """
        if not self.log_path.exists():
            return False, "No Data"
            
        # Read last 5 runs for this agent
        recent_runs = []
        try:
            with open(self.log_path, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    if data.get("agent") == agent_name:
                        recent_runs.append(data)
        except Exception:
            return False, "Read Error"
            
        recent_runs = recent_runs[-5:]
        
        if not recent_runs:
            return False, "New Agent"
            
        # 1. Failure Loop Check
        failures = sum(1 for r in recent_runs if r["status"] != "SUCCESS")
        if len(recent_runs) >= 3 and failures == len(recent_runs):
            return True, "100% Failure Rate (Last 5 Runs)"
            
        # 2. Zombie Check (Duration Drift) - simplistic
        avg_duration = sum(r["duration_sec"] for r in recent_runs) / len(recent_runs)
        if recent_runs[-1]["duration_sec"] > (avg_duration * 3 + 10): # +10s buffer
            return True, f"Execution Time Spike ({recent_runs[-1]['duration_sec']}s vs avg {avg_duration}s)"
            
        return False, "Healthy"

    def kill_zombies(self):
        """Scans for orphaned python processes consuming high CPU/RAM"""
        # This is a dangerous method, use with caution. 
        # For Phase Alpha, we just log potential zombies.
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name']:
                    # Check if it's a monolith agent but NOT the main Prime or API
                    cmd = str(proc.info['cmdline'])
                    if 'monolith' in cmd and 'prime' not in cmd and 'api' not in cmd:
                        if proc.cpu_percent(interval=0.1) > 80:
                             print(f"⚠️ [OPS] Potential Zombie detected: PID {proc.info['pid']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
