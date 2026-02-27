"""
SENTINEL AGENT - Project Monolith v6.0 (REAL GUARD MODE)
Status: ACTIVE MONITORING
Capabilities:
- Real-time File Integrity Monitoring (SHA-256)
- System Resource Guard (CPU/RAM/Disk Real telemetry)
- Unauthorized Modification Alerts
"""

import json
import logging
import psutil
import hashlib
import time
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Fix Windows console encoding
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class IntegrityMonitor:
    """Monitors critical system files for unauthorized changes"""
    
    CRITICAL_FILES = [
        "System/Agents/micro_task_executor.py",
        "System/Core/revenue_orchestrator.py",
        "System/Config/financial_policy.json",
        "monolith_dashboard.py"
    ]
    
    def __init__(self, root_path: Path):
        self.root = root_path
        self.hashes = {}
        self.baseline_file = root_path / "System" / "Config" / "integrity_baseline.json"
        
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file"""
        if not file_path.exists():
            return "MISSING"
        
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return f"ERROR: {e}"

    def update_baseline(self):
        """Update the known-good baseline"""
        print("[SENTINEL] 📸 Taking new system baseline snapshot...")
        for rel_path in self.CRITICAL_FILES:
            full_path = self.root / rel_path
            self.hashes[rel_path] = self.calculate_file_hash(full_path)
        
        with open(self.baseline_file, "w") as f:
            json.dump(self.hashes, f, indent=2)

    def check_integrity(self) -> List[str]:
        """Compare current state to baseline"""
        if not self.baseline_file.exists():
            self.update_baseline()
            return []
            
        with open(self.baseline_file, "r") as f:
            baseline = json.load(f)
            
        violations = []
        for rel_path, expected_hash in baseline.items():
            current_hash = self.calculate_file_hash(self.root / rel_path)
            if current_hash != expected_hash:
                violations.append(f"integrity_violation: {rel_path} (Expected: {expected_hash[:8]}, Got: {current_hash[:8]})")
                
        return violations

class SentinelAgent:
    """
    Guardian of the Monolith v6.0.
    Enforces System Integrity and Resource Health.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.sentinel_dir = self.root / "System" / "Sentinels"
        self.logs_dir = self.root / "System" / "Logs" / "Security"
        self.config_dir = self.root / "System" / "Config"
        
        # Ensure directories
        for d in [self.sentinel_dir, self.logs_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        self.monitor = IntegrityMonitor(self.root)
        
        logging.basicConfig(
            filename=self.logs_dir / "sentinel_hyper_log.txt",
            level=logging.INFO, 
            format='[%(asctime)s] [SENTINEL-REAL] %(message)s'
        )

    def check_resources(self) -> Dict:
        """Real system resource check"""
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        status = "GREEN"
        if cpu > 90 or ram > 90 or disk > 90:
            status = "RED"
        elif cpu > 70 or ram > 70 or disk > 80:
            status = "YELLOW"
            
        return {
            "status": status,
            "cpu": cpu,
            "ram": ram,
            "disk": disk
        }

    def run(self):
        print("[SENTINEL] 🛡️ SYSTEM INTEGRITY GUARD ACTIVE")
        
        # 1. Integrity Check
        violations = self.monitor.check_integrity()
        integrity_status = "GREEN"
        if violations:
            integrity_status = "RED"
            print(f"[SENTINEL] 🚨 INTEGRITY VIOLATION DETECTED!")
            for v in violations:
                print(f"  - {v}")
                logging.warning(v)
        else:
            print("[SENTINEL] ✅ Core Files Verified Clean")
            
        # 2. Resource Check
        resources = self.check_resources()
        print(f"[SENTINEL] 📊 System Health: {resources['status']} (CPU: {resources['cpu']}%, RAM: {resources['ram']}%)")
        
        # 3. Report
        final_status = "GREEN" if integrity_status == "GREEN" and resources['status'] != "RED" else "RED"
        
        self._report(final_status, f"Integrity: {integrity_status} | Load: {resources['status']}")
        
        return {
            "status": final_status,
            "integrity_violations": violations,
            "resources": resources
        }

    def _report(self, status, message):
        data = {
            "agent": "sentinel_agent",
            "version": "v6.0-Real",
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.sentinel_dir / "sentinel_agent.done", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    SentinelAgent().run()
