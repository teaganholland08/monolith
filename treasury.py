import json

class Treasury:
    def __init__(self):
        self.balance = 0.0
        self.phase = "PHASE_0" # Starting from $0
        self.allocation_rules = {
            "PHASE_0": {"reinvest": 1.0, "profit": 0.0},
            "PHASE_1": {"reinvest": 0.9, "profit": 0.1}
        }

    def deposit(self, amount, source):
        print(f"💰 DEPOSIT RECEIVED: ${amount} from {source}")
        self.balance += amount
        self.allocate()

    def allocate(self):
        # Logic defined in Layer 6.3 of Spec
        rules = self.allocation_rules[self.phase]
        reinvest_amt = self.balance * rules["reinvest"]
        profit_amt = self.balance * rules["profit"]
        
        print(f"   ↳ 🔄 REINVEST (Upgrade Systems): ${reinvest_amt:.2f}")
        print(f"   ↳ 🏦 VAULT (Cold Storage): ${profit_amt:.2f}")

        # Check for Phase Upgrade
        if self.balance > 100:
            self.phase = "PHASE_1"
            print("🚀 SYSTEM UPGRADE: Entering Phase 1 ($100+ revenue)")

# Initialize Treasury
monolith_treasury = Treasury()
