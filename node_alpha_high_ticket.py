"""
NODE ALPHA: HIGH TICKET CLIENT SNIPER
Status: LIVE
Target: $3,000+ Contracts (Development, Automation, AI Consulting)
Mechanism: Real-time keyword monitoring on Reddit/Twitter/LinkedIn
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class HighTicketSniper:
    """
    Node Alpha: The Hunter.
    Scans for direct "I need help" signals.
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "node_alpha_sniper"
        self.config_dir = self.root / "Config"
        
        for d in [self.sentinel_dir, self.memory_dir]:
            d.mkdir(parents=True, exist_ok=True)
            
        self.keywords = [
            "hiring ai developer",
            "looking for automation expert",
            "need python developer",
            "build me a chatbot",
            "fix my scraper",
            "seeking llm engineer"
        ]
        
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration"""
        target_file = self.config_dir / "node_alpha_config.json"
        if not target_file.exists():
            default = {
                "enabled": True,
                "min_budget_signal": 1000,
                "platforms": ["Reddit", "Twitter"],
                "keywords": self.keywords
            }
            target_file.write_text(json.dumps(default, indent=2))
            return default
        return json.loads(target_file.read_text())

    def scan_reddit(self):
        """Scan Reddit for hiring signals (using public JSON feeds)"""
        print("[NODE ALPHA] 🦅 Scanning Reddit for high-ticket signals...")
        leads = []
        subreddits = ["forhire", "hiring", "freelance_forhire", "Python", "MachineLearning"]
        
        headers = {'User-Agent': 'MonolithSniper/1.0'}
        
        for sub in subreddits:
            try:
                url = f"https://www.reddit.com/r/{sub}/new.json?limit=25"
                resp = requests.get(url, headers=headers, timeout=5)
                
                if resp.status_code == 200:
                    data = resp.json()
                    for post in data.get("data", {}).get("children", []):
                        p_data = post.get("data", {})
                        title = p_data.get("title", "").lower()
                        text = p_data.get("selftext", "").lower()
                        
                        # Filter for hiring
                        if "hiring" in title or "looking for" in title:
                            # Filter for keywords
                            if any(k in title or k in text for k in self.keywords):
                                leads.append({
                                    "source": f"Reddit r/{sub}",
                                    "title": p_data.get("title"),
                                    "url": f"https://reddit.com{p_data.get('permalink')}",
                                    "budget_signal": "Unknown" # NLP would extract this later
                                })
            except Exception as e:
                print(f"   ⚠️ Reddit scan error ({sub}): {e}")
                
        return leads

    def run(self):
        print(f"[NODE ALPHA] 🚀 High Ticket Sniper Active")
        
        leads = self.scan_reddit()
        
        if leads:
            print(f"[NODE ALPHA] 🎯 Found {len(leads)} POTENTIAL HIGH-TICKET LEADS")
            for lead in leads:
                print(f"   💰 {lead['title']}")
                print(f"      {lead['url']}")
        
        status = {
            "node": "Alpha",
            "type": "High Ticket Sniper",
            "status": "GREEN",
            "leads_found": len(leads),
            "message": f"Found {len(leads)} leads. Engagement required.",
            "leads": leads,
            "timestamp": datetime.now().isoformat()
        }
        
        self._report(status)
        return status

    def _report(self, data):
        with open(self.sentinel_dir / "node_alpha.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    sniper = HighTicketSniper()
    sniper.run()
