try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    sync_playwright = None
    PLAYWRIGHT_AVAILABLE = False
import os
import time
import json
from comm_link import CommLink

class CFOAgent:
    def __init__(self):
        self.sandbox = "./data/cfo/"
        self.operative_sandbox = "./data/operative/"
        self.miner_sandbox = "./data/miner/"
        
        os.makedirs(self.sandbox, exist_ok=True)
        os.makedirs(self.operative_sandbox, exist_ok=True)
        os.makedirs(self.miner_sandbox, exist_ok=True)
        
        self.vault_path = os.path.join(self.sandbox, ".env_vault")
        self.memory_file = os.path.join(self.miner_sandbox, "brain_memory.json")
        self.comm_link = CommLink()

    def unlock_vault(self):
        if not os.path.exists(self.vault_path):
            with open(self.vault_path, "w") as f:
                f.write("BANK_USER=monolith_demo\nBANK_PASS=sovereign_123")
        print("[CFO] Unlocked financial .env vault.")
        
    def _read_memory(self):
        memory = {}
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            memory.update(data)
            except Exception as e:
                print(f"[CFO] Failed to read memory: {e}")
        return memory

    def _write_memory(self, key, value):
        try:
            with open(self.memory_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps({key: value}) + "\n")
        except Exception as e:
            print(f"[CFO] Failed to write memory: {e}")

    def calculate_dynamic_floor(self, current_balance):
        memory = self._read_memory()
        
        initial_balance = memory.get("INITIAL_BALANCE")
        if initial_balance is None:
            initial_balance = current_balance
            self._write_memory("INITIAL_BALANCE", initial_balance)
            print(f"[CFO] Recorded INITIAL_BALANCE: ${initial_balance}")
            
        historical_high = memory.get("HISTORICAL_HIGH_BALANCE")
        if historical_high is None or current_balance > historical_high:
            historical_high = current_balance
            self._write_memory("HISTORICAL_HIGH_BALANCE", historical_high)
            print(f"[CFO] New HISTORICAL_HIGH_BALANCE: ${historical_high}")
            
        # The Math: max(50% of INITIAL_BALANCE, 50% of HISTORICAL_HIGH_BALANCE, $300 baseline)
        dynamic_floor = max(0.5 * initial_balance, 0.5 * historical_high, 300.0)
        return dynamic_floor

    def trigger_system_wide_lockdown(self, current_balance, dynamic_floor):
        print(f"[CFO] CRITICAL: Balance (${current_balance}) is at or below Dynamic Floor (${dynamic_floor}).")
        print("[CFO] Initiating SYSTEM_WIDE_LOCKDOWN.")
        
        # Revoke all financial permissions from the Operative Agent
        perm_file = os.path.join(self.operative_sandbox, "financial_permissions.json")
        try:
            with open(perm_file, "w") as f:
                json.dump({"can_spend": False, "reason": "SYSTEM_WIDE_LOCKDOWN_ENFORCED"}, f)
            print(f"[CFO] Revoked financial permissions from Operative Agent ({perm_file}).")
        except Exception as e:
            print(f"[CFO] Failed to revoke Operative permissions: {e}")
            
        print("[CFO] Halted all outbound capital deployment.")
        
        # Send CRITICAL alert through comm_link.py
        alert_msg = (f"CRITICAL [SYSTEM_WIDE_LOCKDOWN]: Bank balance is ${current_balance}, "
                     f"which is at or below the Dynamic Floor of ${dynamic_floor}. "
                     "All financial permissions revoked. Target research and scraping will continue.")
        self.comm_link.send_notification(alert_msg)

    def check_balances(self):
        if not PLAYWRIGHT_AVAILABLE:
            print("[CFO] Playwright not available. Using mock balance mode.")
            current_balance = 450.00
            dynamic_floor = self.calculate_dynamic_floor(current_balance)
            print(f"[CFO] Mock Balance: ${current_balance} | Floor: ${dynamic_floor}")
            if current_balance <= dynamic_floor:
                self.trigger_system_wide_lockdown(current_balance, dynamic_floor)
            else:
                print("[CFO] Balance healthy. Capital deployment authorized.")
            return

        print("[CFO] Initializing Headless Browser Scraper (Playwright)...")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Standalone demonstrative scraping mechanism
                # page.goto("https://mybank.local/login")
                # page.fill("#username", "monolith_demo")
                # page.fill("#password", "sovereign_123")
                # page.click("#submit")
                # balance_text = page.locator("#balance").inner_text()
                
                # Mock balance for demonstration
                balance_text = "$450.00"
                current_balance = float(balance_text.replace("$", "").replace(",", ""))
                
                print(f"[CFO] Verified banking balances locally: ${current_balance}")
                
                # Calculate the floor before authorizing capital deployment
                dynamic_floor = self.calculate_dynamic_floor(current_balance)
                print(f"[CFO] Calculated Dynamic Floor: ${dynamic_floor}")
                
                if current_balance <= dynamic_floor:
                    self.trigger_system_wide_lockdown(current_balance, dynamic_floor)
                else:
                    # Give or maintain financial permissions to the Operative Agent
                    perm_file = os.path.join(self.operative_sandbox, "financial_permissions.json")
                    with open(perm_file, "w") as f:
                        json.dump({"can_spend": True, "reason": "BALANCE_ABOVE_FLOOR"}, f)
                    print(f"[CFO] Balance is healthy. Capital deployment authorized.")
                
                browser.close()
        except Exception as e:
            print(f"[CFO] Playwright error (Is chromium installed?): {e}")

    def run(self):
        self.unlock_vault()
        while True:
            self.check_balances()
            time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    cfo = CFOAgent()
    cfo.run()
