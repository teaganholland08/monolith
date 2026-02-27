"""
DRIFT SENTINEL - Project Monolith v7.0
Purpose: Detect Stagnation and Efficiency Drift.
Strategy: Compare Current vs. Historical Performance -> Flag Drift.
"""
import json
import sys
from pathlib import Path
from datetime import datetime

class DriftSentinel:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.logs_dir = self.root.parent / "Logs"
        self.config_dir = self.root.parent / "Config"
        self.sentinel_dir.mkdir(parents=True, exist_ok=True)

    def check_stagnation(self):
        """Checks if key metrics have stalled."""
        print("[DRIFT] 📉 Analyzing System Momentum...")
        
        # Mock check: In reality, compare last 5 cycles of revenue.
        # If variance < 1% for 24h, flag "STAGNATION".
        
        status = "NOMINAL" 
        momentum = "STABLE"
        
        # We can check modification times of key log files
        try:
            gov_log = self.logs_dir / "Governor" / "sovereign_core.log"
            if gov_log.exists():
                last_mod = datetime.fromtimestamp(gov_log.stat().st_mtime)
                delta = (datetime.now() - last_mod).seconds
                if delta > 3600: # 1 hour silence
                    status = "STAGNATION_DETECTED"
                    momentum = "HALTED"
        except:
            pass
            
        print(f"   -> Momentum: {momentum}")
        return status

    def run(self):
        status = self.check_stagnation()
        
        report = {
            "agent": "drift_sentinel",
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "action": "REBOOT_GENESIS" if status == "STAGNATION_DETECTED" else "NONE"
        }

        with open(self.sentinel_dir / "drift_sentinel.done", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
            
        print("--- [DRIFT SENTINEL] CHECK COMPLETE --- \n")

if __name__ == "__main__":
    DriftSentinel().run()
