import urllib.request
import json
import os
import subprocess
import re
import time
from akashic_memory import AkashicMemory
import sys
from pathlib import Path

# Ensure Agents path is loaded for UEFN Coder
sys.path.append(str(Path(__file__).parent / "System" / "Agents"))

class MonolithApex:
    def __init__(self):
        self.api_url = "http://127.0.0.1:11434/api/generate"
        self.akashic = AkashicMemory()
        
        # Migrate old JSON brain to SQLite if it still exists
        self.akashic.migrate_json_brain("monolith_rules.json")
        
        self.rules = self.akashic.get_all_rules()
        self.model = "qwen2.5:0.5b"
        self.operative_file = "temp_operative.py"
        print("\n[SYSTEM] OMEGA TIER ONLINE. Infinite Akashic Memory & Verse Protocol Active.")
        self.auto_upgrade_engine()

    def auto_upgrade_engine(self):
        try:
            output = subprocess.check_output(['wmic', 'computersystem', 'get', 'totalphysicalmemory'])
            ram_gb = int(output.decode().split()[1]) / (1024**3)
            print(f"[+] Hardware Scan: {ram_gb:.1f} GB RAM detected.")

            target_model = "qwen2.5:0.5b"
            if ram_gb >= 12.0: target_model = "llama3:8b"
            elif ram_gb >= 6.0: target_model = "llama3.2:1b"

            if self.model != target_model:
                print(f"[!] UPGRADE: Evolving to {target_model}...")
                subprocess.run(["ollama", "pull", target_model])
                self.model = target_model
            print(f"[+] Optimal engine locked: {self.model}.")
        except Exception as e:
            print("[!] Scan failed. Defaulting to lightweight survival mode.")

    def save_rules(self, new_rules_list):
        self.rules = new_rules_list
        # The Akashic Database naturally deduplicates via UNIQUE constraint
        for rule in self.rules:
            self.akashic.add_rule(rule)

    def think(self, prompt_data):
        data = {"model": self.model, "prompt": prompt_data, "stream": False}
        req = urllib.request.Request(self.api_url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8')).get("response", "Error")
        except: return "ERROR_500"

    def prune_memory(self):
        print("\n[SYSTEM] PRUNING ENGINE ENGAGED: Scanning memories for duplicates and garbage data...")
        if len(self.rules) < 2:
            print("[!] Not enough memory to prune yet. Feed me more targets.")
            return

        rules_str = " | ".join(self.rules)
        prune_prompt = f"Act as a ruthless editor. Here are my current rules: '{rules_str}'. Delete any duplicates, remove useless advice, and combine them into a single, punchy, highly profitable master rule. Keep it under 25 words."

        new_master_rule = self.think(prune_prompt).replace('\n', '').strip()

        if new_master_rule and "ERROR" not in new_master_rule:
            print(f"\n[-] OLD MEMORIES DELETED. \n[+] NEW CONSOLIDATED MASTER RULE: {new_master_rule}\n")
            self.save_rules([new_master_rule])

    def execute_operative(self, code_str):
        print("\n[SYSTEM] Spawning Temp Operative Script...")
        # Strip markdown formatting the AI might hallucinate
        clean_code = re.sub(r'```python|```', '', code_str).strip()
        
        with open(self.operative_file, "w") as f:
            f.write(clean_code)

        try:
            print("[+] Executing Process...\n")
            result = subprocess.run(["python", self.operative_file], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                print("[SUCCESS] Operative Output:\n" + result.stdout)
                return result.stdout
            else:
                print(f"[FAIL] Operative Crash. Error:\n {result.stderr}")
                return result.stderr
        except subprocess.TimeoutExpired:
            print("[!] FATAL: Script took too long. Terminated.")
            return "Timeout"
        except Exception as e:
            print(f"[!] FATAL: Hardware rejection: {e}")
            return str(e)

    def run_loop(self):
        print("\n[SYSTEM] COMMAND DECK: OMEGA TIER.")
        print("Commands: /exit | /rules | /prune | /verse <system_logic>")
        
        while True:
            # Check context from previous loops
            context_log = self.akashic.get_recent_context(limit=3)
            
            mission = input("\n[ARCHITECT] >> ")
            if mission.lower() in ["/exit", "/quit"]: break
            if mission.lower() == "/rules":
                print(f"\n[Akashic Records]:\n" + "\n".join(self.rules))
                continue
            if mission.lower() == "/prune":
                self.prune_memory()
                continue
            if mission.lower().startswith("/verse "):
                mechanic = mission[7:]
                print("[Monolith] Delegating to Core Verse Architect Operative...")
                try:
                    from core_verse_coder import CoreVerseCoder
                    coder = CoreVerseCoder(ai_model=self.model)
                    coder.write_system_logic(mechanic, "auto_generated_architecture")
                except Exception as e:
                    print(f"[!] Verse Engine Error: {e}")
                self.akashic.log_conversation("ARCHITECT", f"Requested Architectural Verse Code: {mechanic}")
                self.akashic.log_conversation("SWARM", "Generated and saved pure Verse module natively.")
                continue
                
            if not mission.strip(): continue

            self.akashic.log_conversation("ARCHITECT", mission)
            
            print(f"\n[Monolith] Syncing Akashic Matrix ({len(self.rules)} Master Rules)...")
            context = "Core Rules: " + " | ".join(self.rules) if self.rules else ""
            recent_context = f"\nRecent Context:\n{context_log}" if context_log else ""
            
            prompt = f"{context}{recent_context}\nArchitect Orders: {mission}. Give a highly profitable step-by-step plan. Ensure to write Python code if requested."
            
            response = self.think(prompt)
            if response == "ERROR_500":
                print("[!] FATAL: Hardware Cannot Process. Please free up RAM.")
                continue
                    
            print("\n[SWARM RESPONSE]:\n" + response)
            self.akashic.log_conversation("SWARM", response)
            
            # Simple critique loop
            print("\n[Monolith] Critiquing output for Akashic Matrix...")
            critique_prompt = f"Review this response: '{response}'. Extract one strict, profitable rule. Under 15 words."
            new_rule = self.think(critique_prompt).replace('\n', '').strip()
            
            if new_rule and "ERROR" not in new_rule:
                if self.akashic.add_rule(new_rule):
                    self.rules.append(new_rule)
                    print(f"[+] AKASHIC RECORD UPDATED. New Rule: {new_rule}")

            # Optionally trigger orchestrator automatically if the prompt implied executing trades/revenue
            if any(kw in mission.lower() for kw in ["run", "start", "revenue", "money", "execute"]):
                print("\n[Monolith] Triggering Revenue Orchestrator Cycle...")
                try:
                    result = subprocess.run(["python", "revenue_orchestrator.py"], capture_output=True, text=True, encoding="utf-8")
                    lines = result.stdout.strip().split('\n')
                    for line in lines[-10:]: print("  " + line)
                except Exception as e:
                    print(f"[!] Warning: Revenue Orchestrator crash: {e}")

if __name__ == "__main__":
    MonolithApex().run_loop()
