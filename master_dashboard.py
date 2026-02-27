"""
PROJECT MONOLITH: MASTER SOVEREIGN DASHBOARD (v5.0 IMMORTAL)
The User's direct interface to the Sovereign Intelligence.
Run this to see the truth of the system without the assistant.
"""
import os
import json
import time
from pathlib import Path
from datetime import datetime

# ANSI Colors for a premium TUI experience
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_sentinel(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except:
        return None

def render_dashboard():
    root = Path(__file__).parent.parent
    sentinel_dir = root / "Sentinels"
    
    clear_screen()
    print(f"{Color.CYAN}{Color.BOLD}🦅 PROJECT MONOLITH: SOVEREIGN CONTROL DASHBOARD{Color.END}")
    print(f"{Color.YELLOW}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Mode: SOVEREIGN (DETACHED){Color.END}\n")
    
    # Define Agents to Track
    agents = [
        ("Revenue Hunter", "omnidirectional_revenue_scanner.done"),
        ("Identity Bridge", "monolith_sentinel.done"),
        ("Defi Yield", "defi_yield_agent.done"),
        ("Global Arbitrage", "global_arb_scout.done"),
        ("Bio-Link Agent", "bio_link_agent.done"),
        ("Home Orchestrator", "home_orchestrator.done"),
        ("Robotic Fleet", "robotic_fleet_manager.done"),
        ("Civic Shield", "civic_agent.done"),
        ("Social Agent", "social_agent.done"),
        ("Safety Shield", "safety_shield.done"),
        ("Accountant", "accountant_agent.done"),
        ("Legacy Sentinel", "legacy_sentinel.done")
    ]
    
    print("-" * 70)
    print(f"{'AGENT':<25} | {'STATUS':<10} | {'LAST UPDATE':<20}")
    print("-" * 70)
    
    for name, file in agents:
        data = load_sentinel(sentinel_dir / file)
        if not data:
            status_str = f"{Color.RED}OFFLINE{Color.END}"
            update_str = "N/A"
        else:
            status = data.get("status", "ACTIVE")
            color = Color.GREEN if status in ["GREEN", "ACTIVE", "SUCCESS"] else Color.YELLOW
            status_str = f"{color}{status:<10}{Color.END}"
            
            ts = data.get("timestamp", "")
            if ts:
                dt = datetime.fromisoformat(ts)
                update_str = dt.strftime("%H:%M:%S")
            else:
                update_str = "Just Now"
        
        print(f"{Color.BOLD}{name:<25}{Color.END} | {status_str} | {update_str}")
        if data and "message" in data:
            print(f"   ↳ {Color.CYAN}{data['message']}{Color.END}")

    print("-" * 70)
    print(f"\n{Color.MAGENTA}[CONTROL]{Color.END} Press {Color.BOLD}Ctrl+C{Color.END} to Detach. System will continue in background.")

if __name__ == "__main__":
    try:
        while True:
            render_dashboard()
            time.sleep(3)
    except KeyboardInterrupt:
        print(f"\n{Color.GREEN}Dashboard Detached. Project Monolith remains active.{Color.END}")
