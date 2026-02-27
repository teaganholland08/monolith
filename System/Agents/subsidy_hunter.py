"""
SUBSIDY HUNTER AGENT - Project Monolith v5.5 (LEVERAGE EDITION)
Purpose: Identify and track "Free Money" (Government Benefits) and Leverage (Loans).
Targeting: BC Income Assistance, GST/HST, CWB, PacifiCan Grants.
"""
import json
import logging
from pathlib import Path
from datetime import datetime

class SubsidyHunter:
    """
    The Capital Acquisition Engine.
    Tracks status of government benefits and loan applications.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
    def load_tracker(self):
        tracker_file = self.root.parent / "Data" / "subsidy_tracker.json"
        if not tracker_file.exists():
            return []
        try:
            return json.loads(tracker_file.read_text(encoding='utf-8'))
        except:
            return []

    def check_eligibility(self):
        """
        Reads the dynamic tracker instead of hardcoded lists.
        """
        tracker = self.load_tracker()
        active_claims = [item for item in tracker if item.get("status") in ["APPLY_NOW", "QUALIFIED", "PENDING"]]
        return active_claims

    def run(self):
        print("[SUBSIDY] 🏛️  Scanning Government & Loan Tracker (Real-Mode)...")
        
        opportunities = self.check_eligibility()
        tracker = self.load_tracker()
        
        # Filter loans
        loans = [item for item in tracker if item.get("type") == "LOAN"]
        
        status = "GREEN"
        if not opportunities:
             message = "No immediate subsidies pending action."
        else:
             message = f"Action Required: {len(opportunities)} items pending (e.g. {opportunities[0]['name']})"
        
        data = {
            "agent": "subsidy_hunter",
            "status": status,
            "message": message,
            "opportunities": opportunities,
            "potential_loans": loans,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "subsidy_hunter.done", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"[SUBSIDY] Tracker loaded. {len(opportunities)} items require attention.")
        if opportunities:
            print(f"[SUBSIDY] 🚨 ACTION: Check 'Data/subsidy_tracker.json' and complete applications.")

if __name__ == "__main__":
    SubsidyHunter().run()
