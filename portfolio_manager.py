"""
PORTFOLIO MANAGER - Project Monolith v5.5 (Global)
Purpose: The "CFO". Allocates capital to the highest yield buckets.
Functionality:
- Balances risk/reward (e.g., Stablecoin Yields vs. New Ad Campaigns).
- Decides re-investment splits.
- Works closely with 'System Growth Engine'.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

try:
    from central_registry import CentralRegistry
except ImportError:
    CentralRegistry = None

class PortfolioManager:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True, parents=True)
        
        self.registry = CentralRegistry() if CentralRegistry else None
        if self.registry:
            self.registry.register_agent("portfolio_manager", ["finance", "investing", "allocation"])

    def allocate_capital(self, total_liquid: float) -> Dict[str, float]:
        """
        The Money Logic. How do we split the pie?
        """
        print(f"[PORTFOLIO] 📊 Allocating Liquid Capital: ${total_liquid}")
        
        # Allocation Strategy: "Aggressive Growth"
        allocation = {
            "REINVEST_IN_INFRA (Servers/APIs)": 0.40,  # 40%
            "MARKETING_TESTS (Ads/Funnels)": 0.30,     # 30%
            "RESERVES (Stablecoins)": 0.20,            # 20%
            "MOONSHOTS (Crypto/High Risk)": 0.10       # 10%
        }
        
        # Calculate actual amounts
        split = {k: round(v * total_liquid, 2) for k, v in allocation.items()}
        return split

    def run(self):
        # Simulated read from Treasury or Accountant
        current_balance = 2500.00 
        
        allocation_plan = self.allocate_capital(current_balance)
        
        for category, amount in allocation_plan.items():
            print(f"   -> {category}: ${amount}")
            
        if self.registry:
            self.registry.post_event("portfolio_manager", "CAPITAL_ALLOCATED", allocation_plan)

        sentinel_data = {
            "agent": "portfolio_manager",
            "timestamp": datetime.now().isoformat(),
            "status": "ACTIVE",
            "current_balance": current_balance,
            "allocation": allocation_plan
        }
        
        with open(self.sentinel_dir / "portfolio_manager.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)

if __name__ == "__main__":
    agent = PortfolioManager()
    agent.run()
