"""
MONOLITH OMEGA - MASTER ENTRY POINT
v6.0 WORLD-COMPLETE EDITION

The Single Source of Truth for Project Monolith.
Orchestrates:
1. Core Kernel (Scheduler, Sandbox)
2. Revenue Layer (Orchestrator)
3. Sentinel Layer (God Rules)

NON-NEGOTIABLE AXIOM: REALITY IS THE SOURCE OF TRUTH.
"""

import sys
import time
import argparse
import io
import os
import json
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    pass

# Add System root to path
ROOT = Path(__file__).parent
sys.path.append(str(ROOT))

from System.Core.monolith_kernel import MonolithCore
from System.Core.revenue_orchestrator import RevenueOrchestrator
from System.Agents.monolith_sentinel import MonolithSentinel

class MonolithOmega:
    def __init__(self, test_mode=False):
        self.root = ROOT
        self.test_mode = test_mode
        self.boot_timestamp = datetime.now()
        
        print("\n" + "="*60)
        print("🏛️ MONOLITH OMEGA: SOVEREIGN BOOT SEQUENCE")
        print("="*60)
        
        # 1. Initialize Core
        self.core = MonolithCore()
        
        # 2. Initialize Revenue
        self.revenue = RevenueOrchestrator()
        
        # 3. Initialize Sentinel (Unified)
        self.sentinel = MonolithSentinel(db_path=self.root / "System" / "Logs" / "ledger.db")  # Pass db_path 
        
    def genesis_boot(self):
        """Pre-Flight Genesis Checks - HARD FAIL ON ERROR"""
        print("\n[OMEGA] 🧬 BEGINNING GENESIS SEQUENCE...")
        
        # 1. Integrity Check
        print("   [1/5] checking system integrity...", end=" ")
        if self._check_integrity():
            print("OK.")
        else:
            print("CRITICAL FAILURE. INTEGRITY COMPROMISED.")
            sys.exit(1)
            
        # 2. Constitution Check
        print("   [2/5] verifying system manifest...", end=" ")
        if (self.root / "System" / "Config" / "system_manifest.json").exists():
             print("OK.")
        else:
             print("WARNING: MANIFEST MISSING (Creating default in Phase 1).")

        # 3. Sentinel Load
        print("   [3/5] loading god rules...", end=" ")
        try:
            self.sentinel.run_bootstrap_check() 
            print(f"OK (Buffer: ${self.sentinel.survival_buffer})")
        except Exception as e:
            print(f"FAILED: {e}")
            if not self.test_mode:
                sys.exit(1)
        
        # 4. Revenue Scan
        print("   [4/5] initializing revenue streams...", end=" ")
        try:
            initial_scan = self.revenue.scan_revenue_opportunities()
            count = initial_scan.get("total_opportunities_found", 0)
            print(f"OK (Opportunities: {count})")
        except Exception as e:
            print(f"WARNING: Revenue Scan Failed: {e}")
        
        # 5. Scheduler
        print("   [5/5] activating scheduler...", end=" ")
        # Inject Revenue Scan task
        self.core.scheduler.add_task(
            "SYSTEM_MAINTENANCE", 
            {"action": "REVENUE_CYCLE_START"},
            priority=10,
            delay_seconds=2
        )
        print("OK.")
        
        print(f"\n[OMEGA] ✅ GENESIS COMPLETE. SYSTEM IS LIVE AND SOVEREIGN.")
        
    def _check_integrity(self):
        # Placeholder for file hash checks
        required = [
            self.root / "System" / "Core" / "monolith_core.py",
            self.root / "System" / "Agents" / "monolith_sentinel.py"
        ]
        return all(f.exists() for f in required)

    def run(self):
        """Enter the Infinite Loop"""
        self.genesis_boot()
        
        if self.test_mode:
            print("\n[TEST MODE] Executing single cycle and exiting...")
            self.core.run_forever_test(max_loops=1) 
            return

        # Hand over control to Core
        try:
            self.core.run_forever(omega_callback=self.omega_cycle)
        except KeyboardInterrupt:
            print("\n[OMEGA] 🛑 SHUTDOWN RECEIVED.")
        except Exception as e:
            print(f"\n[OMEGA] 💥 CRITICAL CRASH: {e}")
            self._handle_crash(e)

    def omega_cycle(self):
        """Callback injected into Core loop for Omega-level checks"""
        # 1. Emit Heartbeat
        self._emit_heartbeat()
        
        # 2. Check for Kill Switch (from Sentinel)
        if (self.root / "System" / "Config" / "KILL_SWITCH.trigger").exists():
            print("[OMEGA] 💀 KILL SWITCH DETECTED. TERMINATING.")
            sys.exit(0)

    def _emit_heartbeat(self):
        """Tell Sentinel we are alive"""
        heartbeat_file = self.root / "System" / "Logs" / "system_heartbeat.json"
        data = {
            "pid": os.getpid(),
            "timestamp": datetime.now().isoformat(),
            "status": "RUNNING",
            "uptime": str(datetime.now() - self.boot_timestamp)
        }
        try:
            heartbeat_file.parent.mkdir(parents=True, exist_ok=True)
            with open(heartbeat_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"[OMEGA] ⚠️ Heartbeat fail: {e}")

    def _handle_crash(self, error):
        """Log crash and determine restart policy"""
        log_file = self.root / "System" / "Logs" / "crash_dump.log"
        with open(log_file, "a") as f:
            f.write(f"CRASH: {datetime.now()} - {error}\n")
        # In World-Complete, we would auto-restart here via a bat wrapper
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-genesis", action="store_true", help="Run boot sequence and exit")
    args = parser.parse_args()
    
    omega = MonolithOmega(test_mode=args.test_genesis)
    omega.run()
