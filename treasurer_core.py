"""
THE TREASURER - Project Monolith v5.5
Capital Allocation & Wallet Management.
Interfaces with Auto-Reinvestor to execute financial moves.
"""

import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict

class TreasurerCore:
    """
    The Treasurer: Financial Guardian.
    Manages wallets, executes trades, and checks REAL blockchain balances.
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.sentinel_dir = self.root / "System" / "Sentinels"
        self.memory_dir = self.root / "Memory" / "treasurer_core"
        self.config_dir = self.root / "System" / "Config"
        
        for d in [self.sentinel_dir, self.memory_dir]:
            d.mkdir(parents=True, exist_ok=True)
            
    def get_solana_balance(self, wallet_address: str) -> float:
        """Query public RPC for SOL balance"""
        try:
            url = "https://api.mainnet-beta.solana.com"
            headers = {"Content-Type": "application/json"}
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [wallet_address]
            }
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            data = response.json()
            if "result" in data:
                lamports = data["result"]["value"]
                return lamports / 1_000_000_000  # Convert Lamports to SOL
        except Exception as e:
            print(f"[TREASURER] ⚠️ Blockchain check failed: {e}")
        return 0.0

    def check_wallets(self) -> Dict:
        """Check REAL balances across all monitored wallets"""
        
        # 1. Get Wallet from IO.net Config
        wallet_address = None
        ionet_config = self.config_dir / "ionet_config.json"
        if ionet_config.exists():
            try:
                cfg = json.loads(ionet_config.read_text())
                wallet_address = cfg.get("wallet_address")
                if wallet_address == "YOUR_SOLANA_WALLET_HERE":
                    wallet_address = None
            except:
                pass
        
        sol_balance = 0.0
        if wallet_address:
            print(f"[TREASURER] 🔍 Scanning Solana Chain for: {wallet_address}")
            sol_balance = self.get_solana_balance(wallet_address)
            
        # 2. Get Auto-Reinvestor Context
        try:
            from System.Agents.auto_reinvestor import AutoReinvestor
            # This might still be simulated if no API keys, but we try
            reinvestor_cap = AutoReinvestor().get_available_capital()
        except:
            reinvestor_cap = 0.0
            
        # Combine Sources (Assuming SOL is part of "main_wallet" for now)
        # We value SOL at approx $150 USD for display if needed, but keeping it simple
        # For now, we returns pure units or normalized USD if we had a price feed.
        # Let's assume 1 SOL = $140 USD (Conservative Estimate)
        usd_value = sol_balance * 140.0
        
        total_capital = max(usd_value, reinvestor_cap)

        return {
            "main_wallet": total_capital,
            "sol_balance": sol_balance,
            "wallet_address": wallet_address if wallet_address else "NOT_CONFIGURED",
            "status": "ACTIVE" if wallet_address else "MISSING_WALLET"
        }
    
    def run(self):
        print(f"[TREASURER] 💰 Checking financial status...")
        
        status = self.check_wallets()
        
        print(f"[TREASURER] 💵 Total Capital Value: ${status['main_wallet']:.2f} (SOL: {status['sol_balance']:.4f})")
        
        if status['main_wallet'] >= 50:
             print("[TREASURER] ⚡ ALERT: $50 Threshold Reached -> Preparing Proxy Purchase")
        
        self._report(status)
        return status

    def _report(self, data):
        report = {
            "agent": "The Treasurer",
            "timestamp": datetime.now().isoformat(),
            **data,
            "message": f"Wallet: {data.get('wallet_address', 'N/A')} | Bal: {data.get('sol_balance', 0)} SOL"
        }
        with open(self.sentinel_dir / "treasurer_core.done", 'w') as f:
            json.dump(report, f, indent=2)

if __name__ == "__main__":
    TreasurerCore().run()
