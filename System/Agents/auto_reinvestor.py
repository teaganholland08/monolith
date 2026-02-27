"""
AUTO-REINVESTOR - Project Monolith v5.5
Automatically reinvests profits to scale revenue streams.
Implements smart capital allocation based on ROI and milestones.
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Fix Windows console encoding
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class AutoReinvestor:
    """
    Autonomous reinvestment engine.
    Monitors earnings, allocates capital to highest-ROI opportunities.
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory"
        self.revenue_memory = self.memory_dir / "revenue_orchestrator"
        
        for d in [self.sentinel_dir, self.revenue_memory]:
            d.mkdir(parents=True, exist_ok=True)
        
        self.allocation_rules = self._load_allocation_rules()
        self.reinvestment_log = self._load_reinvestment_log()
    
    def _load_allocation_rules(self) -> Dict:
        """Load capital allocation rules"""
        return {
            "default_split": {
                "reinvest": 100, # 100% back into revenue streams per blueprint
                "reserve": 0,    
                "human": 0       
            },
            "milestones": {
                50: {
                    "unlock": ["proxy_rotation_service"],
                    "allocate": {"proxy_service": 50},
                    "description": "Purchase high-speed proxy rotation for Node Gamma (SDR) scaling"
                },
                100: {
                    "unlock": ["cex_trading"],
                    "allocate": {"cex_trading": 100}
                },
                500: {
                    "unlock": ["api_credits", "hardware_upgrade"],
                    "allocate": {"api_credits": 50, "hardware_upgrade": 50}
                },
                1000: {
                    "unlock": ["defi_yield"],
                    "allocate": {"defi_yield": 500, "scaling": 500}
                },
                5000: {
                    "unlock": ["advanced_trading", "team_expansion"],
                    "allocate": {"advanced_trading": 2000, "team_expansion": 2000, "reserve": 1000}
                }
            },
            "roi_targets": {
                "micro_tasks": {"expected_roi": 1.5, "priority": "high"},
                "gpu_rental": {"expected_roi": 2.0, "priority": "high"},
                "cex_trading": {"expected_roi": 1.2, "priority": "medium"},
                "defi_yield": {"expected_roi": 1.15, "priority": "medium"}
            }
        }
    
    def _load_reinvestment_log(self) -> List[Dict]:
        """Load past reinvestments"""
        log_file = self.revenue_memory / "reinvestment_log.json"
        if log_file.exists():
            return json.loads(log_file.read_text())
        return []
    
    def get_available_capital(self) -> float:
        """Get capital available for reinvestment"""
        earnings_file = self.revenue_memory / "earnings_log.json"
        
        if not earnings_file.exists():
            return 0.0
        
        earnings = json.loads(earnings_file.read_text())
        total_earned = sum(e.get("amount", 0) for e in earnings)
        
        # Subtract already reinvested amount
        total_reinvested = sum(r.get("amount", 0) for r in self.reinvestment_log)
        
        available = total_earned - total_reinvested
        return max(0, available)
    
    def calculate_allocation(self, capital: float) -> Dict:
        """Calculate how to allocate capital"""
        
        rules = self.allocation_rules["default_split"]
        
        allocation = {
            "reinvest_amount": capital * (rules["reinvest"] / 100),
            "reserve_amount": capital * (rules["reserve"] / 100),
            "human_amount": capital * (rules["human"] / 100)
        }
        
        # Check milestones
        total_earned = capital + sum(r.get("amount", 0) for r in self.reinvestment_log)
        
        unlocked_streams = []
        milestone_allocations = {}
        
        for threshold, config in sorted(self.allocation_rules["milestones"].items()):
            if total_earned >= threshold:
                unlocked_streams.extend(config.get("unlock", []))
                milestone_allocations.update(config.get("allocate", {}))
        
        allocation["unlocked_streams"] = unlocked_streams
        allocation["milestone_allocations"] = milestone_allocations
        
        return allocation
    
    def execute_reinvestment(self, allocation: Dict) -> Dict:
        """Execute reinvestment based on allocation"""
        
        reinvest_amt = allocation["reinvest_amount"]
        
        if reinvest_amt < 1:
            return {
                "status": "skipped",
                "reason": "Insufficient capital for reinvestment"
            }
        
        print(f"[AUTO-REINVEST] 💎 Reinvesting ${reinvest_amt:.2f}...")
        
        # Log reinvestment
        reinvestment = {
            "timestamp": datetime.now().isoformat(),
            "amount": reinvest_amt,
            "allocation": allocation,
            "strategy": "milestone_based"
        }
        
        self.reinvestment_log.append(reinvestment)
        self._save_reinvestment_log()
        
        # Trigger stream activations if milestones reached
        if allocation.get("unlocked_streams"):
            print(f"[AUTO-REINVEST] 🔓 Unlocked: {', '.join(allocation['unlocked_streams'])}")
        
        return {
            "status": "completed",
            "reinvested": reinvest_amt,
            "unlocked": allocation.get("unlocked_streams", [])
        }
    
    def _save_reinvestment_log(self):
        """Save reinvestment history"""
        log_file = self.revenue_memory / "reinvestment_log.json"
        log_file.write_text(json.dumps(self.reinvestment_log, indent=2))
    
    def run(self):
        """Main execution"""
        print("[AUTO-REINVEST] 🔄 Checking reinvestment opportunities...")
        
        capital = self.get_available_capital()
        
        if capital < 1:
            print("[AUTO-REINVEST] ⏸️ No capital available for reinvestment")
            self._report("YELLOW", "Waiting for earnings")
            return {"status": "waiting", "capital": capital}
        
        print(f"[AUTO-REINVEST] 💰 Available capital: ${capital:.2f}")
        
        allocation = self.calculate_allocation(capital)
        result = self.execute_reinvestment(allocation)
        
        print(f"[AUTO-REINVEST] ✅ Reinvestment: {result['status']}")
        
        self._report("GREEN", f"Reinvested ${result.get('reinvested', 0):.2f}")
        
        return result
    
    def _report(self, status, message):
        """Report to sentinel"""
        data = {
            "agent": "auto_reinvestor",
            "status": status,
            "message": message,
            "total_reinvested": sum(r.get("amount", 0) for r in self.reinvestment_log),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "auto_reinvestor.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    reinvestor = AutoReinvestor()
    result = reinvestor.run()
    
    print("\n" + "=" * 60)
    print("🔄 AUTO-REINVESTOR - COMPLETE")
    print("=" * 60)
    print(f"Status: {result['status']}")
    if result.get("reinvested"):
        print(f"💰 Reinvested: ${result['reinvested']:.2f}")
        if result.get("unlocked"):
            print(f"🔓 Unlocked: {', '.join(result['unlocked'])}")
    print("=" * 60)
