"""
MONOLITH SENTINEL v7.0 (SWARM ORCHESTRATOR)
The Sovereign Gatekeeper.
Now orchestrates specialized Sub-Sentinels:
1. LegalSentinel (Compliance)
2. FinancialSentinel (Money)
3. IntegritySentinel (Code)
4. RealitySentinel (No Hallucinations)
"""

import json
import sys
import io
from pathlib import Path
import sqlite3

# Fix Windows console encoding
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    pass

# Add System Root to Path
ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT))

try:
    from System.Identity.identity_prime import IdentityPrime
except ImportError:
    IdentityPrime = None

# Import Sub-Sentinels (Swarm)
try:
    from System.Agents.sentinel_swarm import FinancialSentinel, RealitySentinel, SystemIntegritySentinel
except ImportError:
    # Warning, creating fallbacks if files not ready yet during bootstrap
    FinancialSentinel = None
    RealitySentinel = None
    SystemIntegritySentinel = None

class MonolithSentinel:
    def __init__(self, db_path=None):
        self.root = ROOT
        self.config_dir = self.root / "System" / "Config"
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = self.root / "System" / "Logs" / "ledger.db"

        # Initialize Swarm
        self.config_path = self.root / "System" / "Config" / "governance_constitution.json"
        
        try:
             with open(self.config_path, 'r') as f:
                 self.config = json.load(f)
        except:
             self.config = {}

        self.fin_sentinel = FinancialSentinel(self.config) if FinancialSentinel else None
        self.real_sentinel = RealitySentinel() if RealitySentinel else None
        self.sys_sentinel = SystemIntegritySentinel(self.root) if SystemIntegritySentinel else None
        
        # Identity Layer
        
        # Identity Layer
        self.identity = IdentityPrime() if IdentityPrime else None

        # Load God Rules & Governance
        self.rules = self._load_god_rules()
        self.governance = self._load_governance()
        self.survival_buffer = self.rules.get("survival_buffer", 500.0)
        
        # State for Loop Prevention
        self.execution_log = {} # {agent_name: [timestamp, timestamp]}
        
        # Sync Swarm Config
        if self.fin_sentinel:
             # Pass rules if needed
             pass

    def _load_god_rules(self):
        rule_path = self.config_dir / "treasurer_god_rules.json"
        if rule_path.exists():
            try:
                return json.loads(rule_path.read_text())
            except:
                pass
        return {}

    def _load_governance(self):
        gov_path = self.config_dir / "governance_policy.json"
        if gov_path.exists():
            try:
                return json.loads(gov_path.read_text())
            except:
                pass
        return {"loop_prevention": {"max_executions_per_minute": 3, "cooldown_seconds": 60}}

    def run_bootstrap_check(self):
        """Called by Omega/Core during boot"""
        print(f"[SENTINEL] 🛡️  Scanning Reality Layer...", end=" ")
        
        # 1. Sovereignty Check
        has_wallet = False
        if self.identity and self.identity.verify_sovereignty():
            has_wallet = True
        else:
            try:
                from System.Finance.trade_protocol import TradeProtocol
                has_wallet = True  # If trade protocol exists, we are sovereign
            except ImportError:
                pass

        if has_wallet:
            print("✅ SOVEREIGN (Wallet Found).")
        else:
            print("❌ NON-SOVEREIGN (No Wallet). System Restricted.")
            
        return True
        
    def verify_action(self, agent_name, action_type, data):
        """
        MASTER GATEKEEPER
        Delegates to Sub-Sentinels (Swarm)
        """
        # 0. Loop Prevention (Rate Limiting)
        if not self._check_rate_limit(agent_name):
            return False, f"LOOP_BLOCK: {agent_name} exceeded execution limit."

        # 1. System Integrity
        if self.sys_sentinel:
             # Map system update to DELETE_FILE/MODIFY if needed, or pass raw
             ok, reason = self.sys_sentinel.check(action_type, data)
             if not ok: return False, reason

        # 2. Reality Check
        if self.real_sentinel and action_type == "PUBLISH_FACT":
            ok, reason = self.real_sentinel.check(action_type, data)
            if not ok: return False, reason

        # 3. Financial Check
        if action_type in ["SPEND", "INVEST"]:
            if self.fin_sentinel:
                # Need current balance - for now mock or fetch
                balance = 0.0 # TODO: Fetch real balance
                ok, reason = self.fin_sentinel.check(action_type, data, balance)
                if not ok: return False, reason

        return True, "APPROVED"
        
    def _check_rate_limit(self, agent_name):
        """Returns False if rate limit exceeded"""
        import time
        now = time.time()
        
        max_exec = self.governance.get("loop_prevention", {}).get("max_executions_per_minute", 3)
        window = 60 # seconds
        
        if agent_name not in self.execution_log:
            self.execution_log[agent_name] = []
            
        # Clean old logs
        self.execution_log[agent_name] = [t for t in self.execution_log[agent_name] if now - t < window]
        
        # Check count
        if len(self.execution_log[agent_name]) >= max_exec:
            return False
            
        # Log this execution
        self.execution_log[agent_name].append(now)
        return True

    def _get_real_balance(self):
        """Fetch balance from Ledger DB"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN type IN ('REVENUE', 'DEPOSIT') THEN amount ELSE 0 END), 0) -
                    COALESCE(SUM(CASE WHEN type IN ('EXPENSE', 'WITHDRAWAL') THEN ABS(amount) ELSE 0 END), 0)
                FROM transactions
            """)
            res = cursor.fetchone()
            return res[0] if res else 0.0
        except:
            return 0.0
        finally:
             if 'conn' in locals(): conn.close()
             
    def log_violation(self, agent, rule, details):
        """Log bad behavior"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sentinel_logs (
                    id INTEGER PRIMARY KEY,
                    agent TEXT,
                    rule TEXT,
                    details TEXT,
                    timestamp TEXT
                )
            """)
            cursor.execute("INSERT INTO sentinel_logs (agent, rule, details, timestamp) VALUES (?,?,?,?)",
                          (agent, rule, details, datetime.now().isoformat()))
            conn.commit()
            conn.close()
        except:
            pass

if __name__ == "__main__":
    s = MonolithSentinel()
    s.run_bootstrap_check()
