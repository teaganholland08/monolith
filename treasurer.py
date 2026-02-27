"""
TREASURER AGENT - v6.0 (Phase Omega)
Status: LIVE EXTRACTION -> AUTONOMOUS ALLOCATION.
Protocol:
- Tier I (Survival): <$500 -> 100% Reinvest (Proxies/APIs)
- Tier II (Expansion): $500-$5k -> Buy GPU Nodes (Token Burn Reduction)
- Tier III (Fortress): >$5k -> Cold Storage (XMR) + Physical Nodes
"""
import json
import random
import sys
import io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class TreasurerAgent:
    """
    The Financial Governor.
    Automates the 'Phase Omega' Reinvestment Protocol AND Tax Compliance.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        self.vault_path = self.root.parent / "Data" / "Vault" # Hypothetical Vault
        self.vault_path.mkdir(parents=True, exist_ok=True)

    # --- REAL WEALTH LOGIC ---
    def get_real_balance(self):
        """
        Queries the IdentityBridge -> AgenticWallet for confirmed on-chain balance.
        No projections. No estimates.
        """
        try:
            # Lazy import to avoid circular dependency if not careful, 
            # though sentinel is usually safe.
            sys.path.append(str(self.root))
            from System.Agents.monolith_sentinel import IdentityBridge
            
            # Initialize Bridge (mock SIN/Cert is fine here creates the obj, 
            # but it reads the REAL wallet file)
            bridge = IdentityBridge("INTERNAL_SYS", "ROOT") 
            wallet = bridge.create_agentic_wallet()
            
            # In current implementation, wallet.balance is "UNKNOWN" or 0.0 until API active.
            # We treat "UNKNOWN" as 0.0 for safety.
            if isinstance(wallet.balance, str):
                return 0.0
            return float(wallet.balance)
        except Exception as e:
            print(f"[TREASURER] ⚠️ Wallet Connection Failed: {e}")
            return 0.0

    def get_revenue_streams(self):
        """
        Legacy Stream Aggregator - Modified to only report, NOT sum projections.
        """
        details = []
        
        # We process the files just for the 'Memo/Log', but we do NOT add to balance.
        # Balance must come from the Chain (via AgenticWallet).
        
        # 1. Bounty Swarm
        bounty_file = self.sentinel_dir / "bounty_arbitrageur.done"
        if bounty_file.exists():
            try:
                data = json.loads(bounty_file.read_text(encoding='utf-8'))
                if "vulnerabilities" in data:
                    for v in data["vulnerabilities"]:
                        val = v.get("bounty_est", "0")
                        details.append(f"POTENTIAL BOUNTY: {v['target']} ({val}) - PENDING PAYOUT")
            except: pass

        # 2. Compute Arbitrage
        cloud_file = self.sentinel_dir / "cloud_arbitrage.done"
        if cloud_file.exists():
            try:
                data = json.loads(cloud_file.read_text(encoding='utf-8'))
                count = data.get("opportunities_found", 0)
                details.append(f"COMPUTE LEADS: {count} Nodes found - PENDING MARKET EXECUTION")
            except: pass

        # Return 0.0 as revenue because `get_real_balance` is the source of truth.
        return 0.0, details

    # --- TAX LOGIC (NEW) ---
    def detect_write_offs(self, expenditures):
        """
        Scans potential expenses for Tax Deductibility.
        Source: CRA Guidelines for Self-Employed / Business Use of Home.
        """
        updates = []
        for expense in expenditures:
            memo = ""
            category = ""
            
            # Logic: Categorize
            name = expense['item'].lower()
            cost = expense['cost']
            
            if "gpu" in name or "server" in name or "node" in name:
                category = "CCA Class 50 (Computer Equipment)"
                memo = f"Sovereign Infrastructure: {expense['item']} used for AI Compute Operations operations."
                
            elif "api" in name or "subscription" in name or "hosting" in name:
                category = "Software & Subscriptions"
                memo = f"Current Expense: {expense['item']} necessary for automated revenue generation."
                
            elif "wifi" in name or "internet" in name:
                category = "Business-Use-of-Home (Utilities)"
                memo = f"Connectivity: {expense['item']} - Pro-rated business portion."
                
            if category:
                updates.append({
                    "item": expense['item'],
                    "cost": cost,
                    "category": category,
                    "justification": memo,
                    "audit_risk": "LOW" # Automated assumption
                })
                
        return updates

    def get_tax_shield_data(self):
        """Integrates external Tax Shield Agent findings"""
        ts_file = self.sentinel_dir / "tax_shield_agent.done"
        if ts_file.exists():
            try:
                return json.loads(ts_file.read_text(encoding='utf-8'))
            except: 
                pass
        return {}

    # --- ALLOCATION LOGIC ---
    def execute_phase_omega(self, balance):
        """Applies the Tiered Reinvestment Logic"""
        allocation = {}
        
        print(f"[TREASURER] 📊 Current Balance (Est): ${balance:,.2f}")
        
        if balance < 500:
            tier = "I: SURVIVAL"
            allocation = {
                "Proxies (Residential)": balance * 0.60,
                "API_Credits (OpenAI/Anthropic)": balance * 0.40
            }
            action = "🔌 REINVESTING 100% into High-Speed Infra"
            
        elif 500 <= balance < 5000:
            tier = "II: EXPANSION"
            node_cost = 1200 # Cost of a dedicated GPU slice
            nodes_to_buy = int(balance // node_cost)
            remainder = balance % node_cost
            
            allocation = {
                "New_GPU_Nodes": nodes_to_buy,
                "Reserve_Carryover": remainder
            }
            action = f"🚀 ACQUIRING {nodes_to_buy} DEDICATED NODES"
            
        else: # > $5000
            tier = "III: FORTRESS"
            cold_storage = balance * 0.30
            physical_infra = balance * 0.50
            liquid_ops = balance * 0.20
            
            allocation = {
                "Monolith_Cold_Reserve (XMR)": cold_storage,
                "Physical_Node_Hardening": physical_infra,
                "Liquid_Ops": liquid_ops
            }
            action = "🏰 FORTIFYING ASSETS + COLD STORAGE TRANSFER"
            
        return tier, action, allocation

    def run(self):
        print("[TREASURER] 🏛️  PHASE OMEGA PROTOCOL INITIATED...")
        
        # 1. Real Wealth Check
        real_balance = self.get_real_balance()
        print(f"[TREASURER] 💰 VERIFIED WALLET BALANCE: ${real_balance:,.2f}")
        
        # 2. Activity Real-Money Check (Streams)
        # We log them, but don't add them unless they are in the wallet.
        _, sources = self.get_revenue_streams()
        for s in sources:
            print(f"   -> {s}")
            
        # Use Real Balance for allocation, not projected
        rev = real_balance

        # 2. Tax Loop (Real Ledger Check)
        write_offs = []
        
        # Load Real Expenses from CSV if exists
        expense_file = self.root.parent / "Data" / "financial_ledger.csv"
        if expense_file.exists():
            # Basic CSV parsing logic
            try:
                import csv
                with open(expense_file, 'r') as f:
                    reader = csv.DictReader(f)
                    real_expenses = [row for row in reader]
                    write_offs = self.detect_write_offs(real_expenses)
                    print(f"[TREASURER] 📉 Processed {len(real_expenses)} real expense records.")
            except Exception as e:
                print(f"[TREASURER] ⚠️ Ledger Error: {e}")
        else:
            print("[TREASURER] ℹ️  No financial_ledger.csv found. Waiting for real spending data.")

        tax_shield_data = self.get_tax_shield_data()
        
        if write_offs:
            print("\n[TREASURER] 🛡️  Tax Optimization Layer:")
            for w in write_offs:
                 print(f"   TYPE: {w['justification']}")
             
        if tax_shield_data:
            print(f"   EXT: Integrated Tax Shield Data (${tax_shield_data.get('total_writeoff_potential', 0):,.2f} detected)")

        # 3. Allocation
        tier, action, alloc = self.execute_phase_omega(rev)
        
        print(f"\n[TREASURER] 🛡️  STATUS: {tier}")
        print(f"[TREASURER] ⚡ ACTION: {action}")
        print(f"[TREASURER] 📝 Allocation Map: {json.dumps(alloc, indent=2)}")
        
        report = {
            "agent": "treasurer",
            "version": "v7.0-TaxAware",
            "status": "GREEN",
            "tier": tier,
            "balance_est": rev,
            "allocation": alloc,
            "tax_ops": {
                "write_offs_identified": write_offs,
                "tax_shield_integration": tax_shield_data.get("status", "OFFLINE")
            },
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "treasurer.done", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

if __name__ == "__main__":
    TreasurerAgent().run()
