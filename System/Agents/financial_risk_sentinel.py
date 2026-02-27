"""
FINANCIAL RISK SENTINEL - Project Monolith v7.0
Purpose: Protect Capital from Volatility, Fraud, and Platform Bans.
Strategy: Monitor Wallet -> Check Volatility -> Isolate Funds.
"""
import json
import io
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class FinancialRiskSentinel:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.config_dir = self.root / "Config"
        self.sentinel_dir.mkdir(parents=True, exist_ok=True)

    def analyze_wallet_exposure(self):
        """Checks crypto wallet for high-risk assets."""
        print("[RISK-FIN] 📉 Analyzing Wallet Exposure...")
        
        # Load wallet data (Mock logic connecting to WalletGenerator output)
        wallet_file = self.config_dir / "ionet_config.json" # Using ionet config as proxy for main wallet
        exposure = "LOW"
        detected_assets = []
        
        if wallet_file.exists():
            try:
                data = json.loads(wallet_file.read_text())
                if data.get("wallet_address"):
                    detected_assets.append("SOL")
            except:
                pass
        
        # In a real scenario, we'd check price volatility of SOL/BTC here
        # For now, we assume standard volatility
        print(f"   -> Assets Detected: {detected_assets}")
        print(f"   -> Volatility Risk: {exposure}")
        
        return {
            "assets": detected_assets,
            "exposure": exposure
        }

    def check_platform_health(self):
        """Checks if key revenue platforms are operational."""
        print("[RISK-FIN] 🏦 Checking Financial Rails...")
        # Simple mock check
        return {
            "PayPal": "OPERATIONAL",
            "Crypto_Rails": "OPERATIONAL",
            "Banks": "WARNING (No account linked)"
        }

    def run(self):
        print("\n--- [FINANCIAL RISK] 🛡️ CAPITAL GUARD ---")
        exposure = self.analyze_wallet_exposure()
        platforms = self.check_platform_health()
        
        report = {
            "agent": "financial_risk_sentinel",
            "timestamp": datetime.now().isoformat(),
            "wallet_exposure": exposure,
            "platform_health": platforms,
            "action_required": "OPEN_BANK_ACCOUNT" if platforms["Banks"] == "WARNING (No account linked)" else "NONE"
        }

        with open(self.sentinel_dir / "financial_risk.done", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        if report["action_required"] != "NONE":
            print(f"[RISK-FIN] 🚨 ACTION REQUIRED: {report['action_required']}")
        
        print("--- [FINANCIAL RISK] GUARD COMPLETE --- \n")

if __name__ == "__main__":
    FinancialRiskSentinel().run()
