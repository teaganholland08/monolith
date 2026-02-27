"""
CORE VERSE INTEGRATION OPERATIVE
Project Monolith vOmega
Harnesses Epic's Verse programming language for its massive concurrency and rollback capabilities
to construct robust financial and architectural logic for the Swarm entirely autonomously.
"""
import os
import json
import urllib.request
from pathlib import Path

class CoreVerseCoder:
    def __init__(self, ai_model="llama3.2:1b"):
        # We try to use a slightly larger model for complex Verse syntax if available
        self.ai_model = ai_model
        self.api_url = "http://127.0.0.1:11434/api/generate"
        self.root = Path(__file__).parent.parent.parent
        self.config_dir = self.root / "System" / "Config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = self.config_dir / "uefn_config.json"
        
        # Pull LiveCoder
        import sys
        if str(self.root / "System" / "Core") not in sys.path:
            sys.path.append(str(self.root / "System" / "Core"))
            
        try:
            from live_coder_engine import LiveCoderEngine
            self.coder_engine = LiveCoderEngine()
        except ImportError:
            print("[UEFN] ⚠️ Live Coder Engine missing. Operating in Text-Only mode.")
            self.coder_engine = None

    def _think_verse(self, system_logic_prompt: str) -> str:
        """Asks the local AI to write strictly valid Verse code for System Architecture."""
        prompt = (
            "You are the Core Architect of Project Monolith.\n"
            "You are writing logic in Epic's Verse programming language (a strongly-typed, highly concurrent language).\n"
            f"Write a complete, valid .verse module for the following system capability:\n{system_logic_prompt}\n\n"
            "REQUIREMENTS:\n"
            "1. Output ONLY the raw Verse code.\n"
            "2. Do NOT use markdown code blocks (```verse ... ```). Return just the text.\n"
            "3. Leverage Verse's <suspends> and <sync> capabilities for large scale concurrency, API polling, or parallel data execution.\n"
            "4. Do NOT include UEFN game logic (no creative_device inheritance)."
        )
        data = {"model": self.ai_model, "prompt": prompt, "stream": False}
        req = urllib.request.Request(self.api_url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as response:
                code = json.loads(response.read().decode('utf-8')).get("response", "")
                
                # Double check to strip any rogue markdown
                import re
                code = re.sub(r'```verse|```', '', code).strip()
                return code
        except Exception as e:
            return f"# ERROR GENERATING VERSE: {e}"

    def write_system_logic(self, concept_description: str, module_name: str):
        print(f"\n[VERSE DEV] ⚙️ Architect requested System Architecture: '{concept_description}'")
        print(f"[VERSE DEV] 🧠 Thinking in Verse syntax... (Model: {self.ai_model})")
        
        verse_code = self._think_verse(concept_description)
        
        if verse_code.startswith("# ERROR"):
            print("[VERSE DEV] ❌ Failed to compile AI logic.")
            return False
            
        print("[VERSE DEV] ✅ Verse Logic Compiled.")
        
        if self.coder_engine:
            # Inject directly into the command center
            res = self.coder_engine.write_core_verse(module_name, verse_code)
            if res.get("status") == "SUCCESS":
                print(f"[VERSE DEV] ⚡ Deployed -> {res.get('path')}")
                return True
            else:
                print(f"[VERSE DEV] ⚠️ Could not inject: {res.get('message')}")
                print("[VERSE DEV] 💾 Code Output:\n")
                print(verse_code)
                return False
        else:
            print("[VERSE DEV] 💾 Standalone Output:\n")
            print(verse_code)
            return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Core Verse Auto-Coder")
    parser.add_argument("--module", type=str, default="data_scraper", help="Name of the Verse module")
    parser.add_argument("--concept", type=str, default="Create a concurrent loop that polls 5 API endpoints simultaneously.", help="System logic description")
    args = parser.parse_args()
    
    coder = CoreVerseCoder()
    coder.write_system_logic(args.concept, args.module)
