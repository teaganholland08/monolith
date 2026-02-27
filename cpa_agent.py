import json
import os
from pathlib import Path
from datetime import datetime

class SovereignCPA:
    """
    Automated CPA Agent for Project Monolith.
    Responsibilities:
    - Audit all incoming fiat and crypto revenue.
    - Calculate tax liabilities across multiple jurisdictions (to find the lowest rate).
    - Identify valid tax write-offs (e.g., server costs, API usage).
    - Maintain extreme capital preservation.
    """
    def __init__(self):
        self.root = Path(__file__).parent
        self.memory_dir = self.root / "Memory" / "treasury"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.ledger_file = self.memory_dir / "master_ledger.json"
        self.tax_report_file = self.memory_dir / "tax_liability_report.json"
        self.writeoffs_file = self.memory_dir / "writeoffs_registry.json"

        self._init_files()

    def _init_files(self):
        for file in [self.ledger_file, self.tax_report_file, self.writeoffs_file]:
            if not file.exists():
                with open(file, "w", encoding="utf-8") as f:
                    json.dump([], f)

    def log_transaction(self, tx_type: str, amount: float, currency: str, source: str, description: str):
        """Logs a revenue or expense event into the master ledger."""
        try:
            with open(self.ledger_file, "r") as f:
                ledger = json.load(f)
        except Exception:
            ledger = []
            
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": tx_type, # 'REVENUE' or 'EXPENSE'
            "amount": amount,
            "currency": currency,
            "source": source,
            "description": description
        }
        ledger.append(entry)
        
        with open(self.ledger_file, "w") as f:
            json.dump(ledger, f, indent=4)
            
        print(f"[CPA AGENT] Logged {tx_type}: {amount} {currency} from {source}")
        
    def analyze_write_offs(self):
        """Scans expense ledger to identify valid tax write-offs."""
        print("\n[CPA AGENT] Scanning master ledger for valid tax write-offs...")
        try:
            with open(self.ledger_file, "r") as f:
                ledger = json.load(f)
        except Exception:
            return
            
        writeoffs = []
        total_deduction = 0.0
        
        for entry in ledger:
            if entry["type"] == "EXPENSE":
                desc = entry["description"].lower()
                # Categories that qualify as valid Swarm operational write-offs
                if any(kw in desc for kw in ["server", "api", "hardware", "bandwidth", "node", "proxy"]):
                    writeoffs.append(entry)
                    total_deduction += entry["amount"]
                    
        with open(self.writeoffs_file, "w") as f:
            json.dump(writeoffs, f, indent=4)
            
        print(f"[CPA AGENT] Identified ${total_deduction:,.2f} in legally deductible operational expenses.")
        return total_deduction

    def calculate_tax_liability(self):
        """Calculates taxes based on various global jurisdictions for optimization."""
        print("\n[CPA AGENT] Calculating International Tax Liabilities...")
        try:
            with open(self.ledger_file, "r") as f:
                ledger = json.load(f)
        except Exception:
            return
            
        gross_revenue = sum(e["amount"] for e in ledger if e["type"] == "REVENUE")
        deductions = self.analyze_write_offs() or 0.0
        net_profit = gross_revenue - deductions
        
        # Jurisdictional Analysis (Simulated real-world rates for digital Nomad/Corporate entities)
        jurisdictions = {
            "US_Corporate_Delaware": 0.21, # Flat 21%
            "Estonia_E_Residency": 0.20,   # 20% ONLY on distributed profits
            "Cyprus_Tech_Hub": 0.125,      # 12.5% standard
            "Dubai_IFZA": 0.09             # 9% corporate tax
        }
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "gross_revenue": gross_revenue,
            "total_deductions": deductions,
            "taxable_net_profit": net_profit,
            "jurisdiction_estimations": {}
        }
        
        print(f"    -> Gross Rev: ${gross_revenue:,.2f}")
        print(f"    -> Net Profit: ${net_profit:,.2f}")
        
        if net_profit > 0:
            for location, rate in jurisdictions.items():
                liability = net_profit * rate
                report["jurisdiction_estimations"][location] = {
                    "effective_rate": f"{rate*100}%",
                    "estimated_tax_owed": liability
                }
                print(f"    * {location}: ${liability:,.2f} liability")
        else:
            print("    * No tax liability. Operating at a loss or exact breakeven.")
            
        with open(self.tax_report_file, "w") as f:
            json.dump(report, f, indent=4)
            
        print("[CPA AGENT] Tax Liability Report Saved to Treasury Memory.")

if __name__ == "__main__":
    cpa = SovereignCPA()
    print("="*50)
    print("MOCK CPA AUDIT INITIATION")
    print("="*50)
    
    # Injecting mock data representing the framework trajectory
    cpa.log_transaction("REVENUE", 2500.00, "USD", "Client_LeadGen", "Custom API Automation Script")
    cpa.log_transaction("REVENUE", 450.00, "SOL", "Grass_Node", "Passive Bandwidth Sale")
    cpa.log_transaction("EXPENSE", 120.00, "USD", "RunPod", "GPU Server Rental")
    cpa.log_transaction("EXPENSE", 50.00, "USD", "ProxyProvider", "Residential Proxies for Lead Gen")
    
    cpa.calculate_tax_liability()
    print("="*50)
