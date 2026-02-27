import urllib.request
import urllib.error
import urllib.parse
import json
import time
import os
import sys
from comm_link import CommLink

class RDAgent:
    def __init__(self):
        self.sandbox = "./data/rnd/"
        self.miner_sandbox = "./data/miner/"
        os.makedirs(self.sandbox, exist_ok=True)
        os.makedirs(self.miner_sandbox, exist_ok=True)
        
        self.memory_file = os.path.join(self.miner_sandbox, "brain_memory.json")
        self.core_file = "./monolith_core.py"
        self.comm_link = CommLink()
        
        self.ollama_tags_url = "http://localhost:11434/api/tags"
        self.ollama_pull_url = "http://localhost:11434/api/pull"
        self.ollama_generate_url = "http://localhost:11434/api/generate"
        self.ollama_delete_url = "http://localhost:11434/api/delete"

        # List of candidate models to hunt for (simulating scraping registry)
        self.lightweight_candidates = [
            "llama3.2",
            "llama3.1:8b",
            "phi3:mini",
            "qwen2:0.5b",
            "qwen2:1.5b",
            "gemma2:2b"
        ]

    def _read_memory(self):
        memory = {}
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            memory.update(data)
            except Exception:
                pass
        return memory

    def _write_memory(self, key, value):
        try:
            with open(self.memory_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps({key: value}) + "\n")
        except Exception as e:
            print(f"[R&D] Failed to write memory: {e}")

    def get_local_models(self):
        try:
            req = urllib.request.Request(self.ollama_tags_url)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                return [model['name'] for model in data.get('models', [])]
        except Exception as e:
            print(f"[R&D] Failed to query local Ollama models: {e}")
            return []

    def pull_model(self, model_name):
        print(f"[R&D] Pulling candidate model into sandbox: {model_name}")
        payload = {"name": model_name}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.ollama_pull_url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as response:
                print(f"[R&D] Successfully pulled {model_name}.")
                return True
        except Exception as e:
            print(f"[R&D] Model pull failed: {e}")
            return False

    def delete_model(self, model_name):
        print(f"[R&D] Deleting model from sandbox: {model_name}")
        payload = {"name": model_name}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.ollama_delete_url, data=data, headers={'Content-Type': 'application/json'}, method='DELETE')
        try:
             with urllib.request.urlopen(req) as response:
                 print(f"[R&D] Model {model_name} deleted successfully.")
        except Exception as e:
             print(f"[R&D] Deletion failed: {e}")

    def benchmark_test(self, model_name):
        print(f"[R&D] Initiating Sandbox Brawl for {model_name}. Sentinel is watching thermals...")
        prompt = "Write a comprehensive Python script that calculates the Fibonacci sequence up to 1000 and prints the ratio of consecutive numbers. Ensure comments and type hinting. Do not explain, just return code."
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.ollama_generate_url, data=data, headers={'Content-Type': 'application/json'})
        
        start_time = time.time()
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                end_time = time.time()
                
                duration = end_time - start_time
                eval_count = result.get('eval_count', 0)
                tps = eval_count / duration if duration > 0 else 0
                
                print(f"[R&D] Benchmark complete in {duration:.2f}s. TPS: {tps:.2f}")
                return True, tps
        except urllib.error.URLError as e:
            # If Sentinel killed Ollama due to temps, we'll get a connection error.
            print(f"[R&D] Benchmark failed for {model_name}. Likely thermal limit exceeded (Connection Refused): {e}")
            return False, 0
        except Exception as e:
            print(f"[R&D] Benchmark encountered an error: {e}")
            return False, 0

    def auto_accept_pipeline(self, model_name):
        print(f"[R&D] Auto-Accept Pipeline triggered for {model_name}.")
        # Update brain memory
        self._write_memory("ACTIVE_LLM_MODEL", model_name)
        
        # Hardcode the update in monolith_core.py as a permanent overwrite backup
        if os.path.exists(self.core_file):
            try:
                with open(self.core_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Overwriting the default model fallback specifically to ensure the script updates physically
                if 'model = "llama3.2"' in content:
                    content = content.replace('model = "llama3.2"', f'model = "{model_name}"')
                    with open(self.core_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"[R&D] Core orchestrator file directly overwritten with new defaults.")
            except Exception as e:
                print(f"[R&D] Failed to overwrite core file: {e}")
        
        # Send Telegram Comm-Link alert
        msg = f"System Evolved. Auto-accepted upgrade to {model_name}."
        self.comm_link.send_notification(msg)
        print("[R&D] Alert dispatched via Comm-Link.")
        
        # Restart the orchestration loop natively (assuming we run in boss supervisor)
        # Note: Boss agent auto-restarts processes if they exit.
        print("[R&D] Self-Optimization complete. The Swarm will adapt.")

    def run_radar_loop(self):
        print("[R&D] Apex R&D Protocol Initiated. Radar spinning up...")
        # Get currently active model
        active_model = self._read_memory().get("ACTIVE_LLM_MODEL", "llama3.2")
        
        # Benchmark baseline
        print(f"[R&D] Benchmarking baseline model ({active_model})...")
        baseline_success, baseline_tps = self.benchmark_test(active_model)
        
        if not baseline_success:
            print("[R&D] Baseline benchmarking failed. Retrying later.")
        else:
            print(f"[R&D] Baseline TPS: {baseline_tps:.2f}")

            # Hunt for a better model
            local_models = self.get_local_models()
            for candidate in self.lightweight_candidates:
                if candidate == active_model:
                    continue
                    
                print(f"[R&D] Evaluating candidate: {candidate}")
                # We pull it to test it if it's not present (or even if it is, we test it)
                if self.pull_model(candidate):
                    success, tps = self.benchmark_test(candidate)
                    if success:
                        if tps > baseline_tps:
                            print(f"[R&D] Candidate {candidate} is FASTER than baseline ({tps:.2f} > {baseline_tps:.2f}).")
                            self.auto_accept_pipeline(candidate)
                            active_model = candidate
                            baseline_tps = tps
                        else:
                            print(f"[R&D] Candidate {candidate} is SLOWER or equal to baseline. Discarding.")
                            if candidate not in local_models:
                                self.delete_model(candidate)
                    else:
                        print(f"[R&D] Candidate {candidate} failed the sandbox brawl. Thermals likely tripped. Deleting and aborting.")
                        self.delete_model(candidate)

    def run(self):
        while True:
            self.run_radar_loop()
            print("[R&D] Entering deep sleep for 7 days (weekly loop).")
            # 60 * 60 * 24 * 7 = 604800 seconds
            time.sleep(604800)

if __name__ == "__main__":
    rnd = RDAgent()
    rnd.run()
