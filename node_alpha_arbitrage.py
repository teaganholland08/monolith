"""
NODE ALPHA: DATA ARBITRAGE ENGINE - Project Monolith v7.0
Status: ACTIVE
Mechanism: Scans Free Public APIs -> Normalizes Data -> Packages for Resale/Usage.
Target: High-Quality JSON Datasets (Weather, Crypto, Government).
"""

import json
import requests
import time
from pathlib import Path
from datetime import datetime

class DataArbitrageNode:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.data_dir = self.root.parent / "Data" / "Arbitrage" / "Packages"
        
        self.sentinel_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Free, No-Auth APIs for Proof-of-Concept
        self.targets = [
            {
                "id": "coingecko_trending",
                "url": "https://api.coingecko.com/api/v3/search/trending",
                "value_prop": "Trending Crypto Dataset for Trading Bots"
            },
            {
                "id": "open_meteo",
                "url": "https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01&hourly=temperature_2m",
                "value_prop": "Hyper-Local Weather Data for Logistics"
            },
            {
                "id": "random_user",
                "url": "https://randomuser.me/api/?results=10",
                "value_prop": "Synthetic User Data for UI Testing"
            },
            {
                "id": "universities",
                "url": "http://universities.hipolabs.com/search?country=United+States",
                "value_prop": "Global Education Database for CRMs"
            }
        ]

    def acquire_data(self, target):
        """Fetches real data from the source."""
        print(f"[ARBITRAGE] 🌍 Connecting to {target['id']} ({target['url']})...")
        try:
            response = requests.get(target['url'], timeout=10)
            if response.status_code == 200:
                data = response.json()
                size_kb = len(response.content) / 1024
                print(f"   ✅ ACQUIRED: {size_kb:.2f} KB of raw data.")
                return data
            else:
                print(f"   ❌ FAILED: Status {response.status_code}")
                return None
        except Exception as e:
            print(f"   ⚠️ ERROR: {e}")
            return None

    def package_dataset(self, target, raw_data):
        """Normalizes and saves the dataset."""
        if not raw_data: return None
        
        package_id = f"{target['id']}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        filename = self.data_dir / f"{package_id}.json"
        
        package = {
            "meta": {
                "source": target['url'],
                "timestamp": datetime.now().isoformat(),
                "value_proposition": target['value_prop'],
                "usage_rights": "Public Domain / CC0 (Assumed for Test)"
            },
            "data": raw_data
        }
        
        filename.write_text(json.dumps(package, indent=2))
        print(f"   📦 PACKAGED: {filename.name}")
        return filename

    def run(self):
        print("[ARBITRAGE] 🦅 Starting Data Acquisition Cycle...")
        
        acquired_count = 0
        latest_package = ""
        
        for target in self.targets:
            data = self.acquire_data(target)
            if data:
                path = self.package_dataset(target, data)
                if path:
                    acquired_count += 1
                    latest_package = path.name
            time.sleep(1) # Be polite
            
        status = {
            "agent": "node_alpha_arbitrage",
            "status": "GREEN",
            "datasets_acquired": acquired_count,
            "latest_package": latest_package,
            "storage_path": str(self.data_dir),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "node_alpha_arbitrage.done", 'w') as f:
            json.dump(status, f, indent=2)
            
        print(f"[ARBITRAGE] ✅ Cycle Complete. {acquired_count} Datasets secured.")

if __name__ == "__main__":
    DataArbitrageNode().run()
