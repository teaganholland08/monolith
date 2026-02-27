"""
MONOLITH SENTINEL SWARM
Specialized Security Modules.
"""

import json
from pathlib import Path
from datetime import datetime

class FinancialSentinel:
    def __init__(self, config):
        self.limits = config.get("financial_limits", {})
        
    def check(self, action, payload, current_balance):
        """
        Enforce Law 1: Solvency.
        """
        if action not in ["SPEND", "INVEST"]:
            return True, "N/A"
            
        amount = payload.get("amount", 0.0)
        
        # 1. Absolute Solvency
        if amount > current_balance:
            return False, f"INSOLVENCY_RISK: Cost ({amount}) > Balance ({current_balance})"
            
        # 2. Daily Limit (Mock implementation for now)
        if amount > self.limits.get("max_daily_spend", 0.01):
             return False, f"LIMIT_BREACH: Amount ({amount}) > Daily Limit"
             
        return True, "APPROVED"

class RealitySentinel:
    def __init__(self):
        pass
        
    def check(self, action, payload):
        """
        Enforce Law 2: Reality.
        Check for citation/sources in generated content.
        """
        if action == "PUBLISH_FACT":
            source = payload.get("source")
            if not source or source == "generated":
                 return False, "HALLUCINATION_RISK: No source provided."
                 
        return True, "APPROVED"

class SystemIntegritySentinel:
    def __init__(self, root_path):
        self.root = root_path
        self.protected_files = ["monolith_omega.py", "System/Core/monolith_core.py"]
        
    def check(self, action, payload):
        """
        Enforce Law 3: Self-Preservation.
        """
        if action == "DELETE_FILE":
            target = payload.get("path", "")
            for protected in self.protected_files:
                if protected in target:
                     return False, f"VIOLATION: Cannot delete critical file {protected}"
                     
        return True, "APPROVED"
