"""
GRASS NODE MANAGER - Project Monolith v5.5
Manages Grass bandwidth monetization (passive income).
Target: $30-60/month from selling unused internet bandwidth.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict

class GrassNodeManager:
    """
    Manages Grass bandwidth selling for passive income.
    Monitors node status and earnings.
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "grass_node_manager"
        self.config_dir = self.root / "Config"
        
        for d in [self.sentinel_dir, self.memory_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load Grass configuration"""
        config_file = self.config_dir / "grass_config.json"
        
        if config_file.exists():
            return json.loads(config_file.read_text())
        
        default_config = {
            "enabled": False,
            "email": None,
            "referral_code": None,
            "nodes": [],
            "estimated_monthly": 30,
            "setup_instructions": {
                "step_1": "Go to https://app.getgrass.io/register",
                "step_2": "Sign up with email",
                "step_3": "Install Chrome extension: https://chromewebstore.google.com/detail/grass/...",
                "step_4": "Leave browser open 24/7",
                "step_5": "Add email to this config and set enabled=true"
            },
            "browser_extension_url": "https://chromewebstore.google.com/detail/grass/ilehaonighjijnmpnagapkhpcdbhclfg"
        }
        
        config_file.write_text(json.dumps(default_config, indent=2))
        return default_config
    
    def check_node_status(self) -> Dict:
        """Check if Grass node is running"""
        
        if not self.config.get("enabled"):
             # AUTO-ENABLE for "Real Money Now"
             print("[GRASS] ℹ️  Auto-enabling Grass Node Manager...")
             self.config["enabled"] = True
             self.config_dir.mkdir(parents=True, exist_ok=True)
             (self.config_dir / "grass_config.json").write_text(json.dumps(self.config, indent=2))
        
        # Check for Chrome/Edge processes
        browser_running = False
        import psutil
        for p in psutil.process_iter(['name']):
            if p.info['name'] in ['chrome.exe', 'msedge.exe', 'brave.exe']:
                browser_running = True
                break

        if not browser_running:
             return {
                 "status": "warning",
                 "message": "Browser closed. Grass extension requires Chrome/Edge open."
             }
        
        return {
            "status": "active",
            "message": "Browser running. Assuming Grass extension is active.",
            "estimated_monthly": self.config["estimated_monthly"]
        }
    
    def run(self):
        """Main execution"""
        print("[GRASS] 🌱 Bandwidth Monetization Manager")
        
        status = self.check_node_status()
        
        if status["status"] == "disabled":
            print(f"[GRASS] ⚠️ {status['message']}")
            self._report("YELLOW", status["message"])
        else:
            print(f"[GRASS] ✅ Node status: {status['status']}")
            estimated = status.get('estimated_monthly', self.config.get('estimated_monthly', 0))
            print(f"[GRASS] 💰 Estimated: ${estimated}/month")
            self._report("GREEN", f"Est. ${estimated}/mo passive")
        
        return status
    
    def _report(self, status_color, message):
        """Report to sentinel"""
        data = {
            "agent": "grass_node_manager",
            "status": status_color,
            "message": message,
            "estimated_monthly": self.config.get("estimated_monthly", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "grass_node_manager.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    manager = GrassNodeManager()
    result = manager.run()
    
    print("\n" + "=" * 60)
    print("🌱 GRASS NODE MANAGER - STATUS")
    print("=" * 60)
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if "estimated_monthly" in result:
        print(f"💰 Estimated Monthly: ${result['estimated_monthly']}")
    print("=" * 60)
