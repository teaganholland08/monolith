import os
import hashlib
import time
import shutil
import json

class DataMiner:
    def __init__(self):
        self.inbox = "./data/inbox/"
        self.assets = "./assets/"
        self.sandbox = "./data/miner/"
        os.makedirs(self.inbox, exist_ok=True)
        os.makedirs(self.assets, exist_ok=True)
        os.makedirs(self.sandbox, exist_ok=True)
        
        self.memory_file = os.path.join(self.sandbox, "brain_memory.json")
        self.known_hashes = set()

    def get_sha256(self, filepath):
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except:
            return None

    def process_inbox(self):
        print("[DataMiner] Ingestion cycle started.")
        processed_count = 0
        
        for filename in os.listdir(self.inbox):
            if processed_count >= 50:
                print("[DataMiner] Throttled intake applied: 50 files limit reached.")
                break
                
            filepath = os.path.join(self.inbox, filename)
            if not os.path.isfile(filepath):
                continue
                
            file_hash = self.get_sha256(filepath)
            if not file_hash:
                continue
                
            if file_hash in self.known_hashes:
                print(f"[DataMiner] Deleting identical file (SHA-256 match): {filename}")
                os.remove(filepath)
                continue
                
            self.known_hashes.add(file_hash)
            lower_name = filename.lower()
            
            # Detect car/bike imagery
            if any(ext in lower_name for ext in ['.jpg', '.png', '.jpeg', '.gif']):
                if 'car' in lower_name or 'bike' in lower_name:
                    print(f"[DataMiner] Moving asset: {filename}")
                    shutil.move(filepath, os.path.join(self.assets, filename))
                else:
                    os.remove(filepath)
                    
            elif lower_name.endswith('.txt'):
                self.parse_text(filepath)
                os.remove(filepath)
            else:
                os.remove(filepath) # Discard unrecognized files
            
            processed_count += 1

    def parse_text(self, filepath):
        print(f"[DataMiner] Parsing text into Local Memory: {os.path.basename(filepath)}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                memory_entry = {os.path.basename(filepath): content}
                
                # Append raw JSON line to brain_memory.json
                with open(self.memory_file, 'a', encoding='utf-8') as mem:
                    mem.write(json.dumps(memory_entry) + "\n")
        except Exception as e:
            print(f"[DataMiner] Failed to parse {filepath}: {e}")

    def run(self):
        while True:
            self.process_inbox()
            time.sleep(3600)  # Check every hour


import requests
import threading

class LiveMarketIngester:
    """Pulls real-time financial market data into the Swarm's inbox."""
    def __init__(self):
        self.inbox = "./data/inbox/"
        self.endpoints = [
            # Binance public API (no key needed for simple public tickers)
            "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
            "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT",
            "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
        ]

    def fetch_market_data(self):
        print("[LiveMarketIngester] Fetching real-time market data...")
        for url in self.endpoints:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    symbol = data.get("symbol", "UNKNOWN")
                    price = data.get("price", "0")
                    
                    filename = f"market_data_{symbol}_{int(time.time())}.txt"
                    filepath = os.path.join(self.inbox, filename)
                    
                    # Create a structured text file for DataMiner to ingest into memory
                    content = f"MARKET DATA: {symbol} is currently priced at ${price} USDT."
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                        
            except Exception as e:
                print(f"[LiveMarketIngester] Failed to fetch {url}: {e}")

    def run(self):
        while True:
            self.fetch_market_data()
            time.sleep(30) # Fetch every 30 seconds

if __name__ == "__main__":
    miner = DataMiner()
    market_ingester = LiveMarketIngester()
    
    # Run both on separate threads
    miner_thread = threading.Thread(target=miner.run, daemon=True)
    market_thread = threading.Thread(target=market_ingester.run, daemon=True)
    
    miner_thread.start()
    market_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ingestion Protocol shut down.")
