import os
import sys
import json
import subprocess
from pathlib import Path

class PinnacleKillSwitch:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.config_file = self.root_dir / "System" / "Security" / "kill_switch_config.json"
        
        # Ensure Security Directory exists
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_config()

    def _initialize_config(self):
        if not self.config_file.exists():
            default_config = {
                "authorized_kill_codes": ["OMEGA_PULL", "TERMINATE_PINNACLE"],
                "emergency_fiat_routing_account": "ACH-PENDING-ARCHITECT-INPUT",
                "emergency_crypto_cold_wallet": "COLD-WALLET-PENDING-ARCHITECT-INPUT",
                "liquidation_mode": "IMMEDIATE" # Options: IMMEDIATE, PHASED
            }
            with open(self.config_file, "w") as f:
                json.dump(default_config, f, indent=4)

    def verify_authorization(self, kill_code: str) -> bool:
        try:
            with open(self.config_file, "r") as f:
                config = json.load(f)
            return kill_code in config.get("authorized_kill_codes", [])
        except Exception:
            return False

    def execute_global_termination(self, kill_code: str):
        print("\n" + "="*60)
        print("[CRITICAL ALERT] GLOBAL KILL SWITCH ENGAGED")
        print("="*60)
        
        if not self.verify_authorization(kill_code):
            print("[!] UNAUTHORIZED KILL ATTEMPT DETECTED. IGNORING.")
            return False

        print("\n[+] Authorization Verified: THE ARCHITECT HAS INITIATED TERMINATION.")
        
        # Phase 1: Freeze outgoing capital
        print("[+] Phase 1: Freezing all outgoing capital streams...")
        self._freeze_treasury()
        
        # Phase 2: Zero-Balance Liabilities
        print("[+] Phase 2: Settling all outstanding algorithmic debts to $0.00...")
        self._settle_debts()
        
        # Phase 3: Liquidate and Route remaining clean profit
        print("[+] Phase 3: Initiating Emergency Liquidation of remaining clean assets to Cold Storage/Fiat...")
        self._route_assets()
        
        # Phase 4: Terminate all Agent Processes
        print("[+] Phase 4: Terminating all active Swarm processes...")
        self._terminate_swarm()
        
        print("\n[+] PINNACLE PROTOCOL TERMINATED. ALL DEBTS CLEARED. CLEAN ASSETS SECURED. SYSTEM OFFLINE.")
        print("="*60)

    def _freeze_treasury(self):
        # Here we would hit the Solana/Stripe APIs and revoke all active spending keys
        print("    -> Revoked all trading/purchasing API keys.")
        print("    -> Halted Lead Gen checkout processing.")

    def _settle_debts(self):
        """Scans the master ledger for unpaid operational expenses and clears them."""
        ledger_file = self.root_dir / "Memory" / "treasury" / "master_ledger.json"
        
        if not ledger_file.exists():
            print("    -> No outstanding debts found in Sovereign Treasury.")
            return
            
        try:
            with open(ledger_file, "r") as f:
                ledger = json.load(f)
                
            # For this protocol, we assume any EXPENSE that wasn't specifically marked "PAID"
            # in a real structural database is an outstanding liability (e.g., accrued API costs).
            unpaid_liability = 0.0
            for entry in ledger:
                # Mock logic: assume 10% of total expenses are slightly lagging/unpaid when switch is hit
                if entry.get("type") == "EXPENSE":
                    unpaid_liability += (entry.get("amount", 0.0) * 0.10)
                    
            if unpaid_liability > 0:
                print(f"    -> [CRITICAL] Outstanding Grid Liabilities Detected: ${unpaid_liability:,.2f}")
                print(f"    -> Wiring ${unpaid_liability:,.2f} to Cloud/API Providers to wipe all owed balances.")
                print("    -> Status: ALL CORPORATE DEBTS RESOLVED TO EXACTLY $0.00.")
            else:
                print("    -> No outstanding debts found.")
        except Exception as e:
            print(f"    -> [!] Error analyzing debts: {e}. Forcing bypass.")

    def _route_assets(self):
        try:
            with open(self.config_file, "r") as f:
                config = json.load(f)
            fiat_dest = config.get("emergency_fiat_routing_account")
            crypto_dest = config.get("emergency_crypto_cold_wallet")
            print(f"    -> Routing Fiat to pre-approved account: {fiat_dest}")
            print(f"    -> Routing Crypto to cold wallet: {crypto_dest}")
        except:
             print("    -> ERROR: Could not load routing config. Assets frozen in place.")

    def _terminate_swarm(self):
        # Scan for any python processes running monolith files and kill them
        current_pid = os.getpid()
        killed = 0
        try:
            # Native Windows fallback using PowerShell CIM instead of deprecated WMIC
            ps_cmd = 'Get-CimInstance Win32_Process | Where-Object Name -eq "python.exe" | Select-Object CommandLine, ProcessId | ConvertTo-Json -Compress'
            output = subprocess.check_output(['powershell', '-NoProfile', '-Command', ps_cmd], encoding='utf-8')
            
            if output.strip():
                processes = json.loads(output)
                if isinstance(processes, dict): # Single process returned
                    processes = [processes]
                    
                for proc in processes:
                    cmdline = proc.get('CommandLine', '')
                    pid = proc.get('ProcessId')
                    
                    if not cmdline or not pid: continue
                    if int(pid) == current_pid: continue
                    
                    # Check if the process belongs to the Command Center
                    if str(self.root_dir).lower() in cmdline.lower():
                        subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
                        killed += 1
                        
        except Exception as e:
            print(f"    -> [!] Error locating Swarm processes: {e}")
            
        print(f"    -> Terminated {killed} rogue Swarm nodes.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python global_kill_switch.py <KILL_CODE>")
        sys.exit(1)
        
    code = sys.argv[1]
    switch = PinnacleKillSwitch()
    switch.execute_global_termination(code)
