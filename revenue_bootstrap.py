"""
REVENUE BOOTSTRAP - Project Monolith
Master Switch to Activate "Real Money" Streams.
"""

import sys
import subprocess
import time
import json
from pathlib import Path
import webbrowser

ROOT = Path(__file__).parent.parent.parent
AGENTS_DIR = ROOT / "System" / "Agents"
CONFIG_DIR = ROOT / "System" / "Config"

def log(msg):
    print(f"[BOOTSTRAP] {msg}")

def check_dependencies():
    log("Checking dependencies...")
    try:
        import solders
        import ecdsa
        import bip_utils
        log("✅ Crypto libraries found.")
    except ImportError:
        log("⚠️ Missing crypto libraries. Attempting install...")
        subprocess.run([sys.executable, "-m", "pip", "install", "solders", "ecdsa", "bip_utils"], check=True)

def step_1_financial_identity():
    log("STEP 1: Financial Identity (Wallet Gen)")
    # Check if wallet exists
    config = CONFIG_DIR / "ionet_config.json"
    if config.exists():
        try:
            data = json.loads(config.read_text())
            if "wallet_address" in data:
                log(f"✅ Wallet found: {data['wallet_address']}")
                return
        except: pass
    
    log("🚀 Generating Sovereign Wallet...")
    subprocess.run([sys.executable, str(AGENTS_DIR / "wallet_generator.py")], check=True)

def step_2_activate_ionet():
    log("STEP 2: Activating IO.NET (GPU Monetization)")
    # We call the agent's run method
    log("... Invoking IoNetGPUManager ...")
    subprocess.run([sys.executable, str(AGENTS_DIR / "ionet_gpu_manager.py")], check=False)

def step_3_activate_grass():
    log("STEP 3: Activating Grass (Bandwidth Monetization)")
    subprocess.run([sys.executable, str(AGENTS_DIR / "grass_node_manager.py")], check=False)

def main():
    print("="*60)
    print("💸 MONOLITH REVENUE BOOTSTRAP PROTOCOL")
    print("="*60)
    
    check_dependencies()
    step_1_financial_identity()
    step_2_activate_ionet()
    step_3_activate_grass()
    
    print("="*60)
    print("✅ BOOTSTRAP COMPLETE. Agents are active.")
    print("   - Check IO.Net worker status in browser/docker.")
    print("   - Ensure Grass extension is running.")
    print("="*60)

if __name__ == "__main__":
    main()
