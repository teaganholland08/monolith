"""
MONOLITH CORE v2.0 (SOVEREIGN)
The Sovereign Kernel.
Merges Agent Creation (Architect) with Task Execution (Executive).
NOW WITH REAL FINANCIAL EXECUTION.
"""

import sys
import time
import json
import sqlite3
from pathlib import Path
from datetime import datetime

# Import Core Subsystems
# Ensure System/Core is in path
sys.path.append(str(Path(__file__).parent))
try:
    from scheduler import MonolithScheduler
    from sandbox_win import MonolithSandbox
except ImportError:
    # Fallback for direct execution testing
    sys.path.append(str(Path(__file__).parent / "System" / "Core"))
    from scheduler import MonolithScheduler
    from sandbox_win import MonolithSandbox

# Import Sentinel (from Agents dir)
sys.path.append(str(Path(__file__).parent.parent / "Agents"))
from monolith_sentinel import MonolithSentinel

# Import Finance (Real Execution)
sys.path.append(str(Path(__file__).parent.parent / "Finance"))
try:
    from trade_protocol import TradeProtocol
except ImportError:
    TradeProtocol = None

# Import Operator (The Brain)
try:
    from monolith_operator import MonolithOperator
except ImportError:
    # Fallback if running from root vs Core
    try:
        from System.Core.monolith_operator import MonolithOperator
    except:
        MonolithOperator = None
        print("⚠️ [CORE] Operator NOT Found. Running in Passive Mode.")

class MonolithCore:
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.db_path = self.root / "System" / "Logs" / "ledger.db"
        
        # Initialize Subsystems
        self.scheduler = MonolithScheduler(self.db_path)
        self.sandbox = MonolithSandbox()
        self.sentinel = MonolithSentinel(self.db_path)
        
        # Finance Hook
        # Finance Hook
        self.trade_protocol = TradeProtocol() if TradeProtocol else None
        
        # Operational Intelligence
        self.operator = MonolithOperator(self) if MonolithOperator else None
        
        # State
        self.running = False
        
    def bootstrap(self):
        """System Initialization"""
        print("\n" + "="*60)
        print("🌌 MONOLITH CORE: IGNITION")
        print("="*60)
        
        # 1. Verify DB
        self._verify_db()
        
        # 2. Sentinel Check
        print(f"[CORE] 🛡️ Sentinel Status: ONLINE (Buffer: ${self.sentinel.survival_buffer})")
        
        # 3. Reality Check (Wallet)
        self._check_wallet_connectivity()
        
        # 4. Resume Pending Tasks
        print("[CORE] 🔄 Resuming Scheduler...")
        
    def _check_wallet_connectivity(self):
        """Verify connection to Real World Financial Layer"""
        if self.trade_protocol and self.trade_protocol.wallet:
            try:
                # Simple connectivity check - address existence isn't enough, 
                # but TradeProtocol init should handle basic setup. 
                # Here we try to fetch balance as a ping.
                bal = self.trade_protocol.wallet.get_balance("ETH")
                print(f"[CORE] 💰 Wallet Connected. Balance: {bal:.6f} ETH")
            except Exception as e:
                print(f"[CORE] ⚠️ Wallet Connectivity Issue: {e}")
        else:
             print("[CORE] ⚠️ Trade Protocol/Wallet DOWN. Financial actions forbidden.")
        
    def _verify_db(self):
        """Ensure Tables Exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Transaction Table (Ledger)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                type TEXT,
                action TEXT,
                amount REAL,
                asset TEXT,
                timestamp TEXT,
                tx_hash TEXT
            )
        """)
        
        # Agent Registry (from Prime)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_registry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT UNIQUE NOT NULL,
                purpose TEXT,
                status TEXT DEFAULT 'ACTIVE',
                created_at TEXT,
                last_run TEXT,
                earnings_generated REAL DEFAULT 0.0,
                script_path TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    def run_forever(self, omega_callback=None):
        """Main Infinite Loop"""
        self.running = True
        self.bootstrap()
        
        print("[CORE] 🚀 Entering Sovereign Loop... (Ctrl+C to stop)")
        
        try:
            while self.running:
                # 0. Omega Callback (for high-level orchestration/checks)
                if omega_callback:
                    omega_callback()

                # 1. Get Task
                task = self.scheduler.get_next_task()
                
                if task:
                    self.execute_task(task)
                else:
                    # IDLE STATE -> TRIGGER OPERATOR
                    if self.operator:
                        self.operator.cycle()
                    
                    time.sleep(1) # Sleep to save CPU
                    
        except KeyboardInterrupt:
            print("\n[CORE] 🛑 Manual Shutdown Initiated.")
            raise # Re-raise for Omega to handle shutdown cleanly

    def run_forever_test(self, max_loops=5):
        """Test Loop Mechanism"""
        self.running = True
        self.bootstrap()
        print(f"[CORE] 🧪 Entering Test Loop ({max_loops} cycles)...")
        
        loops = 0
        while self.running and loops < max_loops:
            dt = self.scheduler.get_next_task()
            if dt:
                self.execute_task(dt)
            else:
                if self.operator:
                    self.operator.cycle()
                else:
                    print(f"[CORE] 💤 Idle call {loops+1}")
                time.sleep(0.5)
            loops += 1
        print("[CORE] 🧪 Test Loop Complete.")
    
    def execute_task(self, task):
        """Execute a single task with Sentinel Oversight"""
        print(f"\n[CORE] ⚡ Executing Task: {task['type']} (ID: {task['id'][:8]})")
        
        data = task['data']
        
        # 1. Sentinel Verification
        # Construct action for Sentinel
        action_type = "GENERIC"
        if task['type'] == "SPEND": action_type = "SPEND"
        if task['type'] == "INVEST": action_type = "INVEST"
        elif task['type'] == "SYSTEM_UPDATE": action_type = "MODIFY_SYSTEM"
        
        allowed, reason = self.sentinel.verify_action("monolith_core", action_type, data)
        
        if not allowed:
            print(f"   ⛔ BLOCKED by Sentinel: {reason}")
            self.scheduler.fail_task(task['id'], f"Sentinel Block: {reason}")
            # Log violation
            self.sentinel.log_violation("monolith_core", "SENTINEL_BLOCK", f"Task {task['id']} blocked: {reason}")
            return
            
        # 2. Dispatch
        try:
            # If it's a script/agent execution task
            if task['type'] == "RUN_AGENT":
                agent_name = data.get("agent_name")
                self._run_agent_task(task, agent_name, data.get("args", []))
            elif task['type'] in ["SPEND", "INVEST"]:
                 # Real spending execution
                 self._execute_spend(task)
            elif task['type'] == "SYSTEM_MAINTENANCE":
                 print("   🔧 Performing System Maintenance...")
                 self.scheduler.complete_task(task['id'], "Maintenance Complete")
            
            elif task['type'] == "SPAWN_AGENT":
                if self.operator and self.operator.factory:
                    print(f"   🏭 Factory Spawning: {data.get('name')}")
                    self.operator.factory.spawn_agent(
                        data.get('name'), 
                        data.get('role')
                    )
                    self.scheduler.complete_task(task['id'], {"status": "spawned"})
                else:
                    self.scheduler.fail_task(task['id'], "Factory Unavailable")
            
            else:
                print(f"   ⚠️ Unknown Task Type: {task['type']}")
                self.scheduler.complete_task(task['id'], {"status": "UNKNOWN_TYPE"})
        except Exception as e:
            print(f"   ❌ Execution Error: {e}")
            self.scheduler.fail_task(task['id'], str(e))

    def _run_agent_task(self, task, agent_name, args):
        """Run an agent script via Sandbox"""
        script_path = self._resolve_agent_path(agent_name)
        
        if not script_path:
             print(f"   ❌ Agent '{agent_name}' not found.")
             self.scheduler.fail_task(task['id'], "Agent not found")
             return

        print(f"   🤖 Launching Agent: {agent_name}")
        result = self.sandbox.run_agent(script_path, args)
        
        if result['success']:
            print("   ✅ Agent Success")
            self.scheduler.complete_task(task['id'], {"stdout": result['stdout']})
        else:
            print("   ❌ Agent Failed/Timeout")
            self.scheduler.fail_task(task['id'], result['stderr'] or "Timeout/Error")

    def _execute_spend(self, task):
        """Execute a financial transaction (REAL EXECUTION)"""
        if not self.trade_protocol:
             print("   ⚠️ Trade Protocol not loaded. Cannot spend.")
             self.scheduler.fail_task(task['id'], "TradeProtocol Missing")
             return

        amount = task['data'].get('amount', 0)
        item = task['data'].get('asset', 'Unknown') # Changed 'item' to 'asset' for clarity
        if not item: item = task['data'].get('item', 'Unknown')
        
        print(f"   💸 INITIATING SPEND: ${amount} on {item}")
        
        # Call Trade Protocol
        # This assumes TradeProtocol has a Unified 'execute_trade' or similar
        # For now, we simulate the internal call structure:
        result = self.trade_protocol.execute_order(
            asset=item,
            amount_usd=amount,
            side="BUY" # Assume buy for spends
        )
        
        if result.get("success"):
            print(f"   ✅ Transaction Confirmed: {result.get('tx_hash')}")
            # Log to Ledger
            self._log_transaction("EXPENSE", "PURCHASE", amount, item, result.get("tx_hash"))
            self.scheduler.complete_task(task['id'], result)
        else:
             print(f"   ❌ Transaction Failed: {result.get('error')}")
             self.scheduler.fail_task(task['id'], f"Trade Failed: {result.get('error')}")

    def _log_transaction(self, tx_type, action, amount, asset, tx_hash):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (source, type, action, amount, asset, timestamp, tx_hash) VALUES (?,?,?,?,?,?,?)",
                      ("CORE", tx_type, action, amount, asset, datetime.now().isoformat(), tx_hash))
        conn.commit()
        conn.close()

    def _resolve_agent_path(self, agent_name):
        """Find agent script"""
        registry_path = self.root / "System" / "Agents" / f"{agent_name}.py"
        if registry_path.exists():
            return registry_path
        return None

if __name__ == "__main__":
    core = MonolithCore()
    # If run with --test, just do a bootstrap check
    if "--test" in sys.argv:
        print("🧪 RUNNING DIAGNOSTIC TEST")
        core.bootstrap()
        # Add a test task
        tid = core.scheduler.add_task("RUN_AGENT", {"agent_name": "hello_world_agent"}, priority=10)
        print(f"   Test Task Added: {tid}")
        
        # Execute the task to verify dispatch
        # Execute Test Loop involved Operator
        core.run_forever_test(max_loops=15)
        
        print("   Checking Sentinel with fake spend...")
        allowed, reason = core.sentinel.verify_action("test", "SPEND", {"amount": 1000000})
        print(f"   Sentinel Check (Should Block): {not allowed} -> {reason}")
    else:
        core.run_forever()
