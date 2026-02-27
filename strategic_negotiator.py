"""
STRATEGIC NEGOTIATOR - Project Monolith v5.5 (Global)
Purpose: The "Haggler". Lowers OpEx by negotiating with APIs and vendors.
Functionality:
- Simulates email/chat negotiation logic.
- Rotates efficiently between 'Student', 'Startup', and 'Enterprise' personas to get discounts.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict

try:
    from central_registry import CentralRegistry
except ImportError:
    CentralRegistry = None

class StrategicNegotiator:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True, parents=True)
        
        self.registry = CentralRegistry() if CentralRegistry else None
        if self.registry:
            self.registry.register_agent("strategic_negotiator", ["negotiation", "cost_reduction", "procurement"])

    def draft_negotiation_email(self, vendor: str, current_spend: float) -> str:
        """
        Writes a script to ask for a discount.
        """
        print(f"[NEGOTIATOR] 💼 Drafting discount request for {vendor} (Spend: ${current_spend})...")
        
        subject = f"Optimization of our {vendor} Enterprise Account"
        body = f"""
        Hi {vendor} Team,
        
        We are scaling our usage significantly (current proj: ${current_spend}/mo).
        We are evaluating competitors but love your API.
        
        Can you move us to the Volume Tier (20% off) effective immediately?
        Looking forward to a quick confirmation.
        
        Best,
        Project Monolith Procurement
        """
        return body

    def run(self):
        # Simulated high-cost vendor found by the Auditor/Accountant
        target_vendor = "OpenAI API"
        monthly_spend = 150.00
        
        if monthly_spend > 100: # Threshold to bother negotiating
            email_draft = self.draft_negotiation_email(target_vendor, monthly_spend)
            print(f"[NEGOTIATOR] 📨 Email Ready. Potential Saving: ${monthly_spend * 0.20}")
            
            # Send event
            if self.registry:
                self.registry.post_event("strategic_negotiator", "NEGOTIATION_STARTED", {"vendor": target_vendor})
        else:
            print("[NEGOTIATOR] 💤 Spend too low to negotiate.")
            email_draft = "N/A"

        sentinel_data = {
            "agent": "strategic_negotiator",
            "timestamp": datetime.now().isoformat(),
            "status": "ACTIVE",
            "last_action": f"Drafted email for {target_vendor}",
            "draft": email_draft
        }
        
        with open(self.sentinel_dir / "strategic_negotiator.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)

if __name__ == "__main__":
    agent = StrategicNegotiator()
    agent.run()
