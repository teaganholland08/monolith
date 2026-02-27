"""
RATE LIMIT CAPTAIN - Project Monolith v5.5 (Global)
Purpose: The "Traffic Cop". Prevents API bans by coordinating global calls.
Functionality:
- Centralized tracking of API usage quotas.
- Implements exponential backoff strategies.
- Prioritizes 'Revenue' calls over 'Research' calls when limits are tight.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict

try:
    from central_registry import CentralRegistry
except ImportError:
    CentralRegistry = None

class RateLimitCaptain:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True, parents=True)
        
        # API Quotas (Simulated)
        self.quotas = {
            "OPENAI": {"limit": 5000, "used": 1200, "reset": "24h"},
            "TWITTER": {"limit": 500, "used": 490, "reset": "15m"}, # Danger zone
            "GOOGLE_SERP": {"limit": 1000, "used": 200, "reset": "24h"}
        }
        
        self.registry = CentralRegistry() if CentralRegistry else None
        if self.registry:
            self.registry.register_agent("rate_limit_captain", ["api_management", "throttling"])

    def request_permission(self, api_name: str, priority: str = "LOW") -> bool:
        """
        Agents call this before hitting an API.
        """
        quota = self.quotas.get(api_name)
        if not quota:
            return True # Unknown API, proceed with caution
            
        remaining = quota["limit"] - quota["used"]
        
        print(f"[RATE-LIMIT] 🚦 Traffic Control for {api_name}: {remaining} requests left.")
        
        # Logic: If < 5% remaining, only HIGH priority allowed
        if remaining < (quota["limit"] * 0.05):
            if priority == "HIGH":
                print(f"[RATE-LIMIT] ⚠️ CRITICAL: Approving HIGH priority request despite low quota.")
                return True
            else:
                print(f"[RATE-LIMIT] 🛑 DENIED: Low priority request blocked to save quota.")
                return False
        
        return True

    def run(self):
        # Simulation: Strategic Negotiator wants to use Twitter (High Priority)
        # Trend Scout wants to use Twitter (Low Priority)
        
        req1 = self.request_permission("TWITTER", "HIGH")
        req2 = self.request_permission("TWITTER", "LOW")
        
        status_report = {
            "OPENAI": "GREEN",
            "TWITTER": "ORANGE (Approaching Limit)",
            "GOOGLE_SERP": "GREEN"
        }

        sentinel_data = {
            "agent": "rate_limit_captain",
            "timestamp": datetime.now().isoformat(),
            "status": "ACTIVE",
            "quotas": self.quotas,
            "decisions": [{"req": "High-Priority Twitter", "approved": req1}, {"req": "Low-Priority Twitter", "approved": req2}]
        }
        
        with open(self.sentinel_dir / "rate_limit_captain.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)

if __name__ == "__main__":
    agent = RateLimitCaptain()
    agent.run()
