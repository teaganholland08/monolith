"""
PAYOUT TRACKER - Project Monolith v5.5
Centralized tracking of ALL revenue streams and payouts.
Monitors earnings, triggers reinvestment, reports to dashboard.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict

class PayoutTracker:
    """
    Central tracking system for all revenue streams.
    Monitors earnings, calculates totals, triggers reinvestment milestones.
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory"
        self.revenue_memory = self.memory_dir / "revenue_orchestrator"
        
        for d in [self.sentinel_dir, self.revenue_memory]:
            d.mkdir(parents=True, exist_ok=True)
        
        self.earnings_log = self._load_earnings_log()
    
    def _load_earnings_log(self) -> List[Dict]:
        """Load all earnings"""
        log_file = self.revenue_memory / "earnings_log.json"
        if log_file.exists():
            return json.loads(log_file.read_text())
        return []
    
    def get_total_earnings(self) -> float:
        """Calculate total earnings all-time"""
        return sum(e.get("amount", 0) for e in self.earnings_log)
    
    def get_earnings_by_stream(self) -> Dict[str, float]:
        """Get earnings breakdown by stream"""
        by_stream = defaultdict(float)
        for earning in self.earnings_log:
            stream = earning.get("stream", "unknown")
            amount = earning.get("amount", 0)
            by_stream[stream] += amount
        return dict(by_stream)
    
    def get_earnings_today(self) -> float:
        """Get earnings for today"""
        today = datetime.now().strftime("%Y-%m-%d")
        return sum(
            e.get("amount", 0) for e in self.earnings_log
            if e.get("timestamp", "").startswith(today)
        )
    
    def get_earnings_this_week(self) -> float:
        """Get earnings for this week"""
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        return sum(
            e.get("amount", 0) for e in self.earnings_log
            if e.get("timestamp", "") >= week_ago
        )
    
    def get_earnings_this_month(self) -> float:
        """Get earnings for this month"""
        this_month = datetime.now().strftime("%Y-%m")
        return sum(
            e.get("amount", 0) for e in self.earnings_log
            if e.get("timestamp", "").startswith(this_month)
        )
    
    def get_best_performing_streams(self, limit: int = 5) -> List[Dict]:
        """Get top performing revenue streams"""
        by_stream = self.get_earnings_by_stream()
        
        ranked = [
            {"stream": stream, "total_earned": amount}
            for stream, amount in by_stream.items()
        ]
        
        ranked.sort(key=lambda x: x["total_earned"], reverse=True)
        return ranked[:limit]
    
    def check_reinvestment_milestones(self) -> List[Dict]:
        """Check if any reinvestment milestones have been hit"""
        total = self.get_total_earnings()
        
        milestones = [
            {"amount": 100, "trigger": "Activate CEX trading"},
            {"amount": 500, "trigger": "Upgrade hardware/API credits"},
            {"amount": 1000, "trigger": "Activate DeFi yield farming"},
            {"amount": 5000, "trigger": "Scale to advanced trading"}
        ]
        
        reached = []
        for milestone in milestones:
            if total >= milestone["amount"]:
                reached.append({
                    **milestone,
                    "reached_at": total,
                    "status": "READY"
                })
        
        return reached
    
    def generate_report(self) -> Dict:
        """Generate comprehensive revenue report"""
        total = self.get_total_earnings()
        today = self.get_earnings_today()
        week = self.get_earnings_this_week()
        month = self.get_earnings_this_month()
        by_stream = self.get_earnings_by_stream()
        top_streams = self.get_best_performing_streams()
        milestones = self.check_reinvestment_milestones()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_earnings": total,
            "earnings": {
                "today": today,
                "this_week": week,
                "this_month": month
            },
            "by_stream": by_stream,
            "top_performers": top_streams,
            "milestones_reached": milestones,
            "total_transactions": len(self.earnings_log)
        }
        
        return report
    
    def run(self):
        """Main execution"""
        print("[PAYOUT] 💰 Generating revenue report...")
        
        report = self.generate_report()
        
        # Display summary
        print(f"\n📊 REVENUE SUMMARY")
        print(f"   Total All-Time: ${report['total_earnings']:.2f}")
        print(f"   Today: ${report['earnings']['today']:.2f}")
        print(f"   This Week: ${report['earnings']['this_week']:.2f}")
        print(f"   This Month: ${report['earnings']['this_month']:.2f}")
        
        print(f"\n🏆 TOP PERFORMING STREAMS:")
        for idx, stream in enumerate(report['top_performers'][:3], 1):
            print(f"   {idx}. {stream['stream']}: ${stream['total_earned']:.2f}")
        
        if report['milestones_reached']:
            print(f"\n🎯 MILESTONES REACHED:")
            for milestone in report['milestones_reached']:
                print(f"   ✅ ${milestone['amount']}: {milestone['trigger']}")
        
        # Save report
        self._save_report(report)
        self._report("GREEN", f"${report['total_earnings']:.2f} total earnings")
        
        return report
    
    def _save_report(self, report: Dict):
        """Save report to memory"""
        report_file = self.revenue_memory / "latest_report.json"
        report_file.write_text(json.dumps(report, indent=2))
    
    def _report(self, status, message):
        """Report to sentinel"""
        data = {
            "agent": "payout_tracker",
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "payout_tracker.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    tracker = PayoutTracker()
    report = tracker.run()
    
    print("\n" + "=" * 60)
    print("💰 PAYOUT TRACKER - COMPLETE")
    print("=" * 60)
    print(f"Total Transactions: {report['total_transactions']}")
    print(f"Total Earnings: ${report['total_earnings']:.2f}")
    print(f"Active Streams: {len(report['by_stream'])}")
    print("=" * 60)
