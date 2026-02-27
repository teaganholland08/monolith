"""
THE VERSE PROTOCOL: LIVE AUTO-CODER
Project Monolith vOmega
Allows the Monolith to write new Python or Verse code, save it to disk, 
and dynamically hot-reload the changes into its running memory without shutting down.
"""
import importlib
import sys
import os
import traceback
from pathlib import Path

class LiveCoderEngine:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.agents_dir = self.root / "System" / "Agents"
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure Agents dir is in path so we can import dynamically
        if str(self.agents_dir) not in sys.path:
            sys.path.append(str(self.agents_dir))

    def write_and_load_python(self, module_name: str, code_content: str):
        """
        Writes a new Python file to disk, then forcefully imports or reloads it
        so the active loop can immediately use the new code.
        """
        # Ensure valid module name (no .py)
        module_name = module_name.replace(".py", "")
        file_path = self.agents_dir / f"{module_name}.py"
        
        try:
            # 1. Write the code to disk
            print(f"[VERSE PROTOCOL] ✍️ Writing new logic to {module_name}.py...")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code_content)
                
            # 2. Invalidate caches so Python sees the new file
            importlib.invalidate_caches()
            
            # 3. Dynamic Hot-Reload
            if module_name in sys.modules:
                print(f"[VERSE PROTOCOL] 🔄 Hot-reloading existing module: {module_name}...")
                reloaded_module = importlib.reload(sys.modules[module_name])
                return {"status": "SUCCESS", "action": "RELOAD", "module": reloaded_module}
            else:
                print(f"[VERSE PROTOCOL] 📥 Importing brand new module: {module_name}...")
                new_module = importlib.import_module(module_name)
                return {"status": "SUCCESS", "action": "IMPORT", "module": new_module}
                
        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"[VERSE PROTOCOL] 💥 FATAL COMPILATION ERROR in {module_name}:")
            print(error_trace)
            return {"status": "ERROR", "traceback": error_trace}

    def write_core_verse(self, module_name: str, code_content: str):
        """
        Saves native Verse architectural logic to the System/Verse_Modules directory.
        These modules provide robust, concurrent logic for the Monolith Swarm.
        """
        try:
            verse_dir = self.root / "System" / "Verse_Modules"
            verse_dir.mkdir(parents=True, exist_ok=True)
                
            module_name = module_name.replace(".verse", "")
            file_path = verse_dir / f"{module_name}.verse"
            
            print(f"[VERSE PROTOCOL] 🧬 Generating Core Architectural Logic: {module_name}.verse")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code_content)
                
            return {"status": "SUCCESS", "path": str(file_path)}
            
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def execute_self_healing(self, original_code: str, error_traceback: str, ai_client, model="qwen2.5:0.5b"):
        """
        Takes broken code, feeds it back to the local AI to fix based on the traceback, 
        and returns the fixed code string so `write_and_load_python` can hot-reload it.
        """
        print("[VERSE PROTOCOL] 🩹 Triggering Self-Healing Mechanism...")
        
        prompt = (
            "You are the self-healing engine of Project Monolith.\n"
            f"The following Python code crashed with this traceback:\n\n"
            f"Traceback:\n{error_traceback}\n\n"
            f"Code:\n```python\n{original_code}\n```\n\n"
            "Identify the bug and completely rewrite the script to fix it. "
            "Respond ONLY with the raw python code. No markdown, no explanations."
        )
        
        try:
            import urllib.request
            import json
            
            api_url = "http://127.0.0.1:11434/api/generate"
            data = {"model": model, "prompt": prompt, "stream": False}
            req = urllib.request.Request(api_url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req) as response:
                fixed_code = json.loads(response.read().decode('utf-8')).get("response", "")
                
                # Strip backticks if the AI hallucinated them
                import re
                fixed_code = re.sub(r'```python|```', '', fixed_code).strip()
                return fixed_code
                
        except Exception as e:
            print(f"[VERSE PROTOCOL] 🩹 Self-Healing Failed: {e}")
            return None

if __name__ == "__main__":
    # Internal Test
    coder = LiveCoderEngine()
    
    test_code = '''
def hello_monolith():
    print("This function was written and hot-reloaded locally without a restart!")
    return True
'''
    res = coder.write_and_load_python("demo_hot_reload", test_code)
    if res["status"] == "SUCCESS":
        mod = res["module"]
        mod.hello_monolith()
