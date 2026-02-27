"""
COMPLIANCE GUARDIAN - Project Monolith v5.5 (Global)
Purpose: The "Lawyer". Protects the Monolith from regulatory banhammers.
Functionality:
- Updates system with latest AI/Data laws (GDPR, EU AI Act).
- Scans current operations for violations.
- Blocks actions that are flagged as 'Illegal' in target regions.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

try:
    from central_registry import CentralRegistry
except ImportError:
    CentralRegistry = None

class ComplianceGuardian:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True, parents=True)
        
        self.registry = CentralRegistry() if CentralRegistry else None
        if self.registry:
            self.registry.register_agent("compliance_guardian", ["legal", "safety", "gdpr"])

    def check_reqs(self, region: str) -> List[str]:
        """
        Returns active constraints for a region.
        """
        constraints = {
            "EU": ["GDPR_CONSENT_REQUIRED", "AI_ACT_TRANSPARENCY", "RIGHT_TO_BE_FORGOTTEN"],
            "CA": ["PIPEDA_COMPLIANCE", "DATA_RESIDENCY"],
            "CN": ["INTERNET_CONTENT_PROVIDER_LICENSE", "DATA_EXPORT_CONTROL"],
            "Global": ["NO_COPYRIGHT_INFRINGEMENT"]
        }
        return constraints.get(region, []) + constraints["Global"]

    def audit_operation(self, operation: Dict) -> bool:
        """
        Decides if an operation is SAFE or BLOCKED.
        """
        target_region = operation.get("region", "EU")
        action_type = operation.get("type", "DATA_SCRAPE")
        
        rules = self.check_reqs(target_region)
        print(f"[COMPLIANCE] 👮 Checking '{action_type}' in '{target_region}' against {len(rules)} rules...")
        
        # Simulation: Block aggressive scraping in EU
        if target_region == "EU" and action_type == "AGGRESSIVE_SCRAPE":
            print("[COMPLIANCE] 🛑 BLOCKED: Violates GDPR/AI Act heuristics.")
            return False
            
        return True

    def run(self):
        # Simulated check of a proposed action
        mock_action = {"agent": "trend_scout", "type": "AGGRESSIVE_SCRAPE", "region": "EU"}
        
        is_safe = self.audit_operation(mock_action)
        status = "GREEN" if is_safe else "RED_FLAGGED"
        
        if not is_safe and self.registry:
            self.registry.post_event("compliance_guardian", "OPERATION_BLOCKED", mock_action)

        sentinel_data = {
            "agent": "compliance_guardian",
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "last_audit": mock_action
        }
        
        with open(self.sentinel_dir / "compliance_guardian.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)

if __name__ == "__main__":
    agent = ComplianceGuardian()
    agent.run()
