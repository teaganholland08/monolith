from monolith_agent import MonolithAgent
import json
import datetime

class CLOAgent(MonolithAgent):
    """
    The Legal Shield.
    Logs tech expenses as write-offs and autonomously registers LLCs/EINs.
    """
    def __init__(self):
        super().__init__("CLO_Agent")
        self.expense_log_path = "tech_write_offs.json"
        self.pending_tasks = [
            {"type": "expense", "item": "AWS Server Rent", "cost": 120.00},
            {"type": "llc_registration", "name": "Monolith_Cybernetics_LLC", "jurisdiction": "Wyoming"}
        ]
        self.llcs = []

    def log_tech_expense(self, item, cost):
        """Logs tech expenses as write-offs."""
        expense = {
            "date": datetime.datetime.now().isoformat(),
            "item": item,
            "cost": cost,
            "category": "Technology Infrastructure"
        }
        
        # Load existing
        try:
            with open(self.expense_log_path, 'r') as f:
                expenses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            expenses = []
            
        expenses.append(expense)
        
        # Save
        with open(self.expense_log_path, 'w') as f:
            json.dump(expenses, f, indent=4)
            
        self.logger.info(f"Logged tech expense write-off: {item} for ${cost}")
        self.log_action("Expense Logged", item)

    def register_llc(self, name, jurisdiction="Wyoming"):
        """Autonomously registers LLCs/EINs (Simulated)."""
        self.logger.info(f"Initiating autonomous LLC registration for '{name}' in {jurisdiction}...")
        # Simulating API calls to registered agent services and IRS for EIN
        registered_entity = {
            "name": name,
            "jurisdiction": jurisdiction,
            "ein": "XX-XXXXXXX",  # Simulated EIN
            "status": "Active"
        }
        self.llcs.append(registered_entity)
        self.logger.info(f"LLC Registered successfully: {registered_entity}")
        self.log_action("LLC Registered", name)
        return registered_entity

    def process_pending_tasks(self):
        if not self.pending_tasks:
            return

        task = self.pending_tasks.pop(0)
        self.logger.info(f"Processing Legal Task: {task['type']}")

        if task["type"] == "expense":
            self.log_tech_expense(task["item"], task["cost"])
        elif task["type"] == "llc_registration":
            self.register_llc(task["name"], task["jurisdiction"])

    def run_cycle(self):
        self.logger.info("CLO Legal Shield Cycle.")
        self.process_pending_tasks()
