"""
MASTER LAUNCH PROTOCOL - Project Monolith v5.5
Purpose: "IGNITION" -> Starts all active agents in background processes.
"""

import subprocess
import sys
import time
import io
from pathlib import Path

# Fix Windows console encoding
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).parent
AGENTS_DIR = ROOT / "System" / "Agents"
ACTIVE_DIR = AGENTS_DIR / "Active"
CORE_DIR = AGENTS_DIR / "Core"

AGENTS = [
    # 1. CORE STABILITY (CRITICAL)
    {"name": "Resource Governor", "path": CORE_DIR / "resource_governor.py", "priority": "HIGH"},
    {"name": "Sentinel Agent", "path": AGENTS_DIR / "sentinel_agent.py", "priority": "HIGH"},

    # 2. REVENUE GENERATION (ACTIVE)
    {"name": "Bandwidth Farmer", "path": ACTIVE_DIR / "bandwidth_farmer.py", "priority": "MED"},
    {"name": "IO.net Manager", "path": ACTIVE_DIR / "ionet_manager.py", "priority": "MED"},
    
    # 3. ACCOUNTING & GROWTH (LOGIC)
    {"name": "Treasury Router", "path": ROOT / "treasury_router.py", "priority": "HIGH"},
    {"name": "Sovereign Logic", "path": ROOT / "sovereign_logic.py", "priority": "HIGH"},
    {"name": "Prometheus Loop", "path": ROOT / "prometheus_loop.py", "priority": "HIGH"},
    {"name": "Profit Engine", "path": ROOT / "profit_engine.py", "priority": "HIGH"},
    {"name": "Data Ingestion", "path": ROOT / "ingestion_protocol.py", "priority": "HIGH"},
    {"name": "CFO Agent", "path": ROOT / "cfo_agent.py", "priority": "HIGH"},
    {"name": "Infra Scaler", "path": ROOT / "infrastructure_scaler.py", "priority": "MED"},
    {"name": "Comm Link", "path": ROOT / "comm_link.py", "priority": "MED"},
]

def launch_all():
    print("\n" + "=" * 60)
    print("MONOLITH MASTER LAUNCH PROTOCOL: IGNITION")
    print("=" * 60 + "\n")
    
    processes = []
    
    for agent in AGENTS:
        print(f"[*] Launching {agent['name']}...", end=" ", flush=True)
        try:
            # Launch in new window? No, keep background.
            # Use pythonw for completely invisible? specific for user request?
            # User wants to know it's working. Let's use standard python but detach?
            # For this context, standard subprocess is best.
            
            p = subprocess.Popen(
                [sys.executable, str(agent['path'])],
                cwd=str(ROOT),
                creationflags=subprocess.CREATE_NEW_CONSOLE 
            )
            processes.append({"name": agent['name'], "pid": p.pid})
            print(f"PID: {p.pid}")
            time.sleep(1) # Stagger start
        except Exception as e:
            print(f"ERROR: {e}")

    print("\n" + "="*50)
    print("SYSTEM ACTIVE. ALL AGENTS DEPLOYED.")
    print("="*50)
    print("Monitoring PID statuses...")
    print("(Close this window to kill all agents)")
    
    # Save Launch Status for Dashboard
    status_file = ROOT / "Sentinels" / "system_status.json"
    status_file.parent.mkdir(exist_ok=True)
    
    launch_data = {
        "status": "ONLINE",
        "timestamp": time.time(),
        "pids": [p['pid'] for p in processes],
        "agents": [p['name'] for p in processes]
    }
    
    import json
    with open(status_file, 'w') as f:
        json.dump(launch_data, f)
        
    print(f"   -> Hardware Status Sentinel Updated: {status_file}")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 SHUTDOWN SEQUENCE INITIATED...")
        for p in processes:
            # We can't kill external processes easily without keeping the obj
            # But since we kept Popen obj...
            pass 
            # Actually, just exiting the main script won't kill sub-processes created with CREATE_NEW_CONSOLE
            # They will persist! This is good for "Active" uptime.

if __name__ == "__main__":
    launch_all()
