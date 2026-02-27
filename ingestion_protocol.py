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

if __name__ == "__main__":
    miner = DataMiner()
    miner.run()
