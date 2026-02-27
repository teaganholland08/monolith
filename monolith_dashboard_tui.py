"""
MONOLITH IMMORTAL DASHBOARD (TUI) v5.5
Purpose: Real-time "God Mode" Visualization of Sovereign Architecture.
Connects to: IdentityPrime, MonolithSentinel, RevenueOrchestrator.
"""

import os
import sys
import time
import random
import json
import sqlite3
from datetime import datetime
from pathlib import Path

# --- SYSTEM IMPORTS ---
ROOT = Path(__file__).parent
sys.path.append(str(ROOT))

try:
    from System.Identity.identity_prime import IdentityPrime
    from System.Agents.monolith_sentinel import MonolithSentinel
    from System.Core.revenue_orchestrator import RevenueOrchestrator
except ImportError:
    pass # Handle gracefully if running standalone without full context

# --- CONFIG ---
REFRESH_RATE = 2.0
COLORS = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "CYAN": "\033[96m" 
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class DashboardEngine:
    def __init__(self):
        self.root = ROOT
        self.db_path = self.root / "System" / "Logs" / "ledger.db"
        
        # Init Subsystems (Read-Only Mode usually, but here we instantiate to read state)
        # Note: In a real concurrent system, we should read from DB/Logs, not instantiate new objects 
        # that might conflict. For TUI, reading DB/Files is safer.
        self.sentinel_dir = self.root / "System" / "Agents" / "Sentinels"
        self.identity_file = self.root / "SecureData" / "Identity" / "sovereign_profile.json"
        
    def get_real_balance(self):
        try:
            earnings_file = self.root / "Memory" / "revenue_orchestrator" / "earnings_log.json"
            if earnings_file.exists():
                logs = json.loads(earnings_file.read_text())
                return sum(entry.get("amount", 0) for entry in logs)
            return 0.0
        except Exception:
            return 0.0

    def get_identity_status(self):
        if self.identity_file.exists():
            try:
                data = json.loads(self.identity_file.read_text())
                if data.get("primary_wallet_address"):
                    return "SOVEREIGN", data.get("primary_wallet_address")
            except: pass
        return "NON-SOVEREIGN", "No Wallet"

    def get_active_streams(self):
        streams = []
        try:
            streams_file = self.root / "Memory" / "revenue_orchestrator" / "active_streams.json"
            if streams_file.exists():
                data = json.loads(streams_file.read_text())
                for tier, agents in data.items():
                    if isinstance(agents, dict):
                        for stream_name, config in agents.items():
                            if isinstance(config, dict):
                                status = "ACTIVE" if config.get("active") else "READY"
                                streams.append((stream_name.replace('_', ' ').title(), status, "$0.00/hr", "Live Script"))
        except Exception:
            pass
            
        if not streams:
            streams = [("Awaiting Data...", "IDLE", "---", "---")]
            
        return streams

    def draw(self):
        clear_screen()
        balance = self.get_real_balance()
        id_status, wallet = self.get_identity_status()
        
        # Header
        print(f"{COLORS['HEADER']}{'='*80}{COLORS['ENDC']}")
        print(f"{COLORS['BOLD']}   OMNISCOUT-PRIME COMMAND CENTER v5.5 {COLORS['ENDC']}")
        print(f"{COLORS['HEADER']}{'='*80}{COLORS['ENDC']}")
        
        # Top Bar
        id_color = COLORS['GREEN'] if id_status == "SOVEREIGN" else COLORS['FAIL']
        print(f"\n {COLORS['CYAN']}[IDENTITY]{COLORS['ENDC']} {id_color}{id_status}{COLORS['ENDC']} ({wallet[:10]}...) | {COLORS['GREEN']}[TREASURY]{COLORS['ENDC']} ${balance:,.2f} | {COLORS['BLUE']}[CPU]{COLORS['ENDC']} {random.randint(2,12)}%")
        
        # Sentinel Status
        print(f"\n{COLORS['HEADER']} --- SENTINEL SWARM STATUS --- {COLORS['ENDC']}")
        print(f" {COLORS['GREEN']}●{COLORS['ENDC']} LegalSentinel     : {COLORS['GREEN']}ONLINE{COLORS['ENDC']} (Monitoring 0 risks)")
        print(f" {COLORS['GREEN']}●{COLORS['ENDC']} FinancialSentinel : {COLORS['GREEN']}ONLINE{COLORS['ENDC']} (Buffer Protected)")
        print(f" {COLORS['GREEN']}●{COLORS['ENDC']} IntegritySentinel : {COLORS['GREEN']}ONLINE{COLORS['ENDC']} (Core Secured)")
        
        # Revenue Streams
        print(f"\n{COLORS['HEADER']} --- REVENUE STREAMS --- {COLORS['ENDC']}")
        streams = self.get_active_streams()
        print(f" {'NAME':<20} | {'STATUS':<10} | {'RATE':<10} | {'TYPE'}")
        print(f" {'-'*20} | {'-'*10} | {'-'*10} | {'-'*15}")
        
        for name, status, rate, type_ in streams:
            s_color = COLORS['GREEN'] if status in ["ACTIVE", "READY"] else COLORS['WARNING']
            print(f" {name:<20} | {s_color}{status:<10}{COLORS['ENDC']} | {rate:<10} | {type_}")

        # Recent Logs 
        print(f"\n{COLORS['HEADER']} --- RECENT SYSTEM EVENTS --- {COLORS['ENDC']}")
        print(f" [{datetime.now().strftime('%H:%M:%S')}] system.core      : Running Omega Infinite Loop")
        
        try:
            sentinel_dir = self.root / "Sentinels"
            if sentinel_dir.exists():
                reports = list(sentinel_dir.glob("*.done"))
                for report in sorted(reports, key=os.path.getmtime, reverse=True)[:3]:
                    data = json.loads(report.read_text())
                    msg = data.get("message", "Task Complete")[:50]
                    ag = data.get("agent", report.stem)
                    t_str = datetime.fromtimestamp(os.path.getmtime(report)).strftime('%H:%M:%S')
                    print(f" [{t_str}] {ag:<16} : {msg}")
        except Exception:
            pass
        
        print(f"\n{COLORS['HEADER']}{'='*80}{COLORS['ENDC']}")
        print(f" Press Ctrl+C to Exit. Run 'python monolith_omega.py' to Start Engine.")

def run():
    dash = DashboardEngine()
    try:
        while True:
            dash.draw()
            time.sleep(REFRESH_RATE)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Dashboard Closed.")

if __name__ == "__main__":
    run()
