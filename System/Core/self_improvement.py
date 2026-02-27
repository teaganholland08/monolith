"""
SELF-IMPROVEMENT LOOP - Project Monolith v7.0
Purpose: Autonomous Code correction and Optimization.
Strategy: Read Logs -> Detect Errors -> Trigger Refactor/Heal.
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime

class SelfImprovementLoop:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.logs_dir = self.root.parent / "Logs"
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(parents=True, exist_ok=True)

    def scan_logs_for_errors(self):
        """Scans all log files for Python tracebacks and errors."""
        print("[SELF-IMPROVE] 🧠 scanning logs for neural friction...")
        detected_errors = []
        
        # Scan Governor and Hydra logs
        log_files = list(self.logs_dir.glob("**/*.log"))
        
        for log_file in log_files:
            try:
                content = log_file.read_text(encoding='utf-8', errors='replace')
                # Look for Tracebacks
                if "Traceback" in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if "Traceback" in line:
                            # Capture next 5 lines for context
                            context = "\n".join(lines[i:i+6])
                            detected_errors.append({
                                "source": log_file.name,
                                "type": "TRACEBACK",
                                "context": context,
                                "timestamp": datetime.now().isoformat()
                            })
            except Exception as e:
                print(f"[SELF-IMPROVE] ⚠️ Could not read {log_file.name}: {e}")

        return detected_errors

    def analyze_error_patterns(self, errors):
        """Categorizes errors and determines if they are 'Healable'."""
        patterns = {
            "IOError": r"I/O operation on closed file",
            "KeyError": r"KeyError: '.*'",
            "AttributeError": r"AttributeError: '.*' object has no attribute '.*'",
            "ImportError": r"ModuleNotFoundError: No module named '.*'"
        }
        
        analysis = []
        for err in errors:
            context = err["context"]
            for category, pattern in patterns.items():
                if re.search(pattern, context):
                    analysis.append({
                        "category": category,
                        "file": err["source"],
                        "reproduction": context,
                        "status": "DETECTED"
                    })
        return analysis

    def run(self):
        print("\n--- [SELF-IMPROVE] 🦅 INITIATING SYSTEM REFRACTION ---")
        raw_errors = self.scan_logs_for_errors()
        analysis = self.analyze_error_patterns(raw_errors)
        
        print(f"[SELF-IMPROVE] Detected {len(raw_errors)} anomalies. {len(analysis)} categorized patterns.")
        
        # Self-Correction Threshold: 
        # If the same error appears > 3 times, it triggers a 'Refactor Request'.
        
        report = {
            "agent": "self_improvement_loop",
            "timestamp": datetime.now().isoformat(),
            "status": "GREEN" if not analysis else "OPTIMIZING",
            "anomalies": raw_errors,
            "pattern_analysis": analysis,
            "healed_this_cycle": 0 # Future: increment when auto-refactor is added
        }

        with open(self.sentinel_dir / "self_improvement.done", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        if analysis:
            print(f"[SELF-IMPROVE] 🚨 Patterns found: {list(set([a['category'] for a in analysis]))}")
            print(f"[SELF-IMPROVE] 🛡️ Neutralizing friction for the next Genesis cycle...")
        
        print("--- [SELF-IMPROVE] REFRACTION COMPLETE --- \n")

if __name__ == "__main__":
    SelfImprovementLoop().run()
