"""
DIGITAL PRODUCT UPLOADER - Project Monolith v5.5
Automates upload of AI-generated digital products to marketplaces.
Target: $100-1000/month from passive digital product sales.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict

class DigitalProductUploader:
    """Uploads AI-generated products to Gumroad, Etsy, etc."""
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "digital_product_uploader"
        self.config_dir = self.root / "Config"
        
        for d in [self.sentinel_dir, self.memory_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        config_file = self.config_dir / "digital_products_config.json"
        
        if config_file.exists():
            return json.loads(config_file.read_text())
        
        default_config = {
            "enabled": False,
            "platforms": {
                "gumroad": {"api_key": None, "enabled": False},
                "etsy": {"api_key": None, "enabled": False},
                "redbubble": {"username": None, "enabled": False}
            },
            "product_types": ["templates", "artwork", "printables", "courses"],
            "setup_instructions": "1. Sign up for platforms\n2. Get API keys\n3. Add here"
        }
        
        config_file.write_text(json.dumps(default_config, indent=2))
        return default_config
    
    def run(self):
        if not self.config.get("enabled"):
            self._report("YELLOW", "Setup required")
            return {"status": "setup_required"}
        
        enabled_platforms = sum(1 for p in self.config["platforms"].values() if p.get("enabled"))
        self._report("GREEN", f"{enabled_platforms} platforms connected")
        return {"status": "active", "platforms": enabled_platforms}
    
    def _report(self, status, message):
        with open(self.sentinel_dir / "digital_product_uploader.done", 'w') as f:
            json.dump({"agent": "digital_product_uploader", "status": status, "message": message, "timestamp": datetime.now().isoformat()}, f, indent=2)

if __name__ == "__main__":
    DigitalProductUploader().run()
