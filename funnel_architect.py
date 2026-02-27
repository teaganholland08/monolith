"""
FUNNEL ARCHITECT - Project Monolith v5.5 (Global)
Purpose: The "Builder". Constructs the traps (funnels) to capture value.
Functionality:
- Uses Trend Scout data (via Registry) to decide WHAT to sell.
- Generates high-conversion landing page copy (Simulated).
- Designs "Hooks" for social media.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

try:
    from central_registry import CentralRegistry
except ImportError:
    CentralRegistry = None

class FunnelArchitect:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True, parents=True)
        
        self.registry = CentralRegistry() if CentralRegistry else None
        if self.registry:
            self.registry.register_agent("funnel_architect", ["marketing", "copywriting", "funnel_design"])

    def generate_hook(self, trend_keyword: str) -> str:
        """
        Creates a 'Scroll-Stopper' headline.
        """
        templates = [
            f"Why {trend_keyword} is Dead (And What's Coming Next)",
            f"How to Master {trend_keyword} in 24 Hours",
            f"The Secret {trend_keyword} Tool Nobody Talks About",
            f"Verify your {trend_keyword} strategy instantly."
        ]
        return templates[0] # Pick the contrarian one for high CTR

    def design_landing_page(self, trend: Dict) -> Dict:
        """
        Blueprints a simple high-conversion page.
        """
        keyword = trend.get("keyword", "New Opportunity")
        print(f"[FUNNEL] 🏗️ Designing funnel for '{keyword}'...")
        
        hook = self.generate_hook(keyword)
        
        structure = {
            "headline": hook,
            "subheadline": f"Join 10,000+ others mastering {keyword} with Monolith.",
            "cta_button": "Get Access Now",
            "social_proof": "Rated 4.9/5 by Early Adopters",
            "urgency": "Offer expires in 12 hours."
        }
        
        return structure

    def run(self):
        # 1. Look for trends (Simulated check against Sentinel or Registry)
        # In a real run, it would query the Registry for 'trend_scout' output.
        print("[FUNNEL] 📥 Checking for hot trends...")
        
        # Mocking input from Trend Scout
        active_trend = {"keyword": "AI Personal Assistants", "velocity": 95}
        
        funnel_plan = self.design_landing_page(active_trend)
        print(f"[FUNNEL] ✨ Generated Hook: '{funnel_plan['headline']}'")
        
        if self.registry:
            self.registry.post_event("funnel_architect", "FUNNEL_CREATED", {"target": active_trend["keyword"]})

        sentinel_data = {
            "agent": "funnel_architect",
            "timestamp": datetime.now().isoformat(),
            "status": "ACTIVE",
            "latest_funnel": funnel_plan
        }
        
        with open(self.sentinel_dir / "funnel_architect.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)

if __name__ == "__main__":
    agent = FunnelArchitect()
    agent.run()
