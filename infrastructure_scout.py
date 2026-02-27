"""
INFRASTRUCTURE SCOUT - Project Monolith v5.5 (Global)
Purpose: The "Architect". Manages the physical (and cloud) body of the Monolith.
Functionality:
- Monitors CPU/RAM usage (using psutil if available, else simulated).
- Detects bottlenecks.
- Deploys "Containerized Agents" to cloud providers if local load is high.
"""

import json
import psutil
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict

try:
    from central_registry import CentralRegistry
except ImportError:
    CentralRegistry = None

class InfrastructureScout:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True, parents=True)
        
        self.registry = CentralRegistry() if CentralRegistry else None
        if self.registry:
            self.registry.register_agent("infrastructure_scout", ["devops", "scaling", "hardware_monitor"])

    def check_vitals(self) -> Dict:
        """
        Real hardware check.
        """
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = shutil.disk_usage(self.root).percent
        
        print(f"[INFRA] 🏥 Vitals: CPU {cpu}% | RAM {ram}% | Disk {disk}%")
        
        return {"cpu": cpu, "ram": ram, "disk": disk}

    def decide_scaling(self, vitals: Dict) -> str:
        """
         Logic: If > 80% load, suggest deploying to Cloud.
        """
        if vitals["cpu"] > 80 or vitals["ram"] > 85:
            return "SCALE_UP (Deploy to AWS/Oracle)"
        elif vitals["cpu"] < 10:
            return "SCALE_DOWN (Consolidate Processes)"
        else:
            return "HEALTHY (Maintain)"

    def run(self):
        vitals = self.check_vitals()
        decision = self.decide_scaling(vitals)
        
        print(f"[INFRA] 🏭 Directive: {decision}")
        
        if decision.startswith("SCALE_UP") and self.registry:
             self.registry.post_event("infrastructure_scout", "SCALING_REQUIRED", vitals)

        sentinel_data = {
            "agent": "infrastructure_scout",
            "timestamp": datetime.now().isoformat(),
            "status": "ACTIVE",
            "vitals": vitals,
            "decision": decision
        }
        
        with open(self.sentinel_dir / "infrastructure_scout.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)

if __name__ == "__main__":
    agent = InfrastructureScout()
    agent.run()
