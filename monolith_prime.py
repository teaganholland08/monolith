"""
MONOLITH PRIME v2.0 - SOVEREIGN ORCHESTRATOR
Recursive Agentic Architecture with Goal Decomposition.

Features:
- Goal -> Plan -> Task Decomposition
- Dynamic Task Graph (DAG)
- Integration with Memory Engine
- Sentinel-Gated Execution
"""

import sqlite3
import json
import subprocess
import time
import sys
import os
import io
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- Imports ---
ROOT = Path(__file__).parent
sys.path.append(str(ROOT / "System" / "Core"))
sys.path.append(str(ROOT / "System" / "Agents"))

try:
    from memory_engine import get_memory
    from monolith_sentinel import MonolithSentinel
except ImportError:
    print("⚠️ Prime Import Warning: Core modules not found in expected path.")
    get_memory = None
    MonolithSentinel = None

class MonolithPrime:
    def __init__(self):
        self.root = ROOT
        self.db_path = self.root / "System" / "Logs" / "ledger.db"
        self.agents_dir = self.root / "System" / "Agents"
        
        # Initialize Memory & Sentinel
        self.memory = get_memory("monolith_prime") if get_memory else None
        self.sentinel = MonolithSentinel(str(self.db_path)) if MonolithSentinel else None
        
        self.active_plans = {}  # {plan_id: plan_data}
        self.boot_time = datetime.now()
        
        self._init_db()
        
    def _init_db(self):
        """Ensure core tables exist (Registry + Task Graph)"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Agent Registry
        c.execute("""
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
        
        # Task Graph (New in v2)
        c.execute("""
            CREATE TABLE IF NOT EXISTS task_graph (
                task_id TEXT PRIMARY KEY,
                parent_goal TEXT,
                description TEXT,
                assigned_agent TEXT,
                status TEXT DEFAULT 'PENDING',
                dependencies TEXT,
                created_at TEXT,
                completed_at TEXT,
                result TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    def submit_goal(self, goal: str) -> str:
        """
        Entry Point: Submit a high-level goal.
        Returns: plan_id
        """
        print(f"\n🎯 PRIME: Received Goal -> '{goal}'")
        plan_id = str(uuid.uuid4())[:8]
        
        # 1. Store in Memory
        if self.memory:
            self.memory.remember_event(f"Goal submitted: {goal}", importance=0.9, metadata={"plan_id": plan_id})
            
        # 2. Decompose (Simulated LLM for now)
        plan = self._decompose_goal(goal)
        self.active_plans[plan_id] = plan
        
        print(f"   📋 Decomposed into {len(plan['tasks'])} tasks.")
        
        # 3. Schedule Tasks
        for task in plan['tasks']:
            self._schedule_task(plan_id, task)
            
        return plan_id

    def _decompose_goal(self, goal: str) -> Dict:
        """
        Heuristic Planner (Placeholder for LLM).
        Breaks common goals into agent tasks.
        """
        tasks = []
        
        if "audit" in goal.lower() or "check" in goal.lower():
            tasks.append({"id": "t1", "desc": "Scan system integrity", "agent": "monolith_sentinel"})
            tasks.append({"id": "t2", "desc": "Check revenue streams", "agent": "omnidirectional_revenue_scanner", "deps": []})
            
        elif "revenue" in goal.lower():
            tasks.append({"id": "t1", "desc": "Scan for opportunities", "agent": "omnidirectional_revenue_scanner"})
            tasks.append({"id": "t2", "desc": "Activate best stream", "agent": "revenue_executor", "deps": ["t1"]})
            
        elif "upgrade" in goal.lower():
             tasks.append({"id": "t1", "desc": "Check hardware stats", "agent": "hardware_sentinel"})
             tasks.append({"id": "t2", "desc": "Research components", "agent": "purchasing_agent", "deps": ["t1"]})
             
        else:
            # Default fallback
            tasks.append({"id": "t1", "desc": f"Research: {goal}", "agent": "scout_agent"})
            
        return {"goal": goal, "tasks": tasks, "status": "IN_PROGRESS"}

    def _schedule_task(self, plan_id: str, task: Dict):
        """Add task to DB Graph"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO task_graph 
            (task_id, parent_goal, description, assigned_agent, status, dependencies, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            f"{plan_id}_{task['id']}", 
            plan_id, 
            task['desc'], 
            task['agent'], 
            "PENDING", 
            json.dumps(task.get("deps", [])),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

    def run_cycle(self):
        """
        Main Orchestration Loop (called by Omega).
        Executor of the Task Graph.
        """
        # 1. Fetch Pending Tasks
        pending = self._get_runnable_tasks()
        
        if not pending:
            return
            
        print(f"\n⚙️ PRIME: Processing {len(pending)} tasks...")
        
        for task in pending:
            self._execute_task(task)

    def _get_runnable_tasks(self) -> List[Dict]:
        """Find tasks where dependencies are met"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Get all pending
        c.execute("SELECT * FROM task_graph WHERE status='PENDING'")
        rows = c.fetchall()
        runnable = []
        
        for row in rows:
            deps = json.loads(row['dependencies'])
            # Check if all deps are COMPLETED
            ready = True
            for dep_id in deps:
                # Assuming dep_id is local task id, construct full id
                full_dep_id = f"{row['parent_goal']}_{dep_id}"
                c2 = conn.cursor()
                c2.execute("SELECT status FROM task_graph WHERE task_id=?", (full_dep_id,))
                res = c2.fetchone()
                if not res or res[0] != 'COMPLETED':
                    ready = False
                    break
            
            if ready:
                runnable.append(dict(row))
        
        conn.close()
        return runnable

    def _execute_task(self, task: Dict):
        """Execute a single task via Sub-Agent"""
        print(f"   ▶ Executing: {task['description']} (Agent: {task['assigned_agent']})")
        
        # 1. Sentinel Check
        if self.sentinel:
            allowed, reason = self.sentinel.verify_action(task['assigned_agent'], "EXECUTE_TASK", task)
            if not allowed:
                 print(f"      ⛔ SENTINEL BLOCK: {reason}")
                 self._update_task_status(task['task_id'], "BLOCKED", result=reason)
                 return

        # 2. Run Agent
        success, output = self._invoke_agent(task['assigned_agent'], task['description'])
        
        # 3. Update Result
        status = "COMPLETED" if success else "FAILED"
        self._update_task_status(task['task_id'], status, result=output[:500]) # Truncate log
        
        if success:
            print("      ✅ Task Complete")
        else:
            print(f"      ❌ Task Failed: {output[:300]}...") # Print first 300 chars of error

    def _invoke_agent(self, agent_name: str, context: str) -> (bool, str):
        """
        Low-level agent invocation (Sandboxed).
        """
        script_path = self.agents_dir / f"{agent_name}.py"
        if not script_path.exists():
            return False, "Agent script not found"
            
        # FIX: Inject HOME
        env = os.environ.copy()
        if "HOME" not in env:
            env["HOME"] = str(Path.home())
            
        try:
            # We can pass context via args or stdin
            # For now, just run it
            res = subprocess.run(
                ["python", str(script_path), "--goal", context],
                capture_output=True,
                text=True,
                timeout=60,
                env=env,
                encoding='utf-8'
            )
            return (res.returncode == 0), (res.stdout + res.stderr)
        except Exception as e:
            return False, str(e)

    def _update_task_status(self, task_id, status, result=""):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            UPDATE task_graph 
            SET status=?, result=?, completed_at=? 
            WHERE task_id=?
        """, (status, result, datetime.now().isoformat(), task_id))
        conn.commit()
        conn.close()

    def bootstrap(self):
        """Initial Boot Sequence"""
        print("\n" + "="*60)
        print("🧠 PRIME v2.0: SOVEREIGN ORCHESTRATOR ONLINE")
        print("="*60)
        self.scan_and_register_agents()

    def scan_and_register_agents(self):
        """Discover agents on disk"""
        print("[PRIME] 🔎 Scanning System/Agents...")
        count = 0 
        for f in self.agents_dir.glob("*.py"):
            self._register_agent_db(f.stem, "Auto-Discovered", str(f))
            count += 1
        print(f"[PRIME] Registered {count} agents.")

    def _register_agent_db(self, name, purpose, path):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT OR IGNORE INTO agent_registry (agent_name, purpose, script_path)
            VALUES (?, ?, ?)
        """, (name, purpose, path))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    prime = MonolithPrime()
    prime.bootstrap()
    
    # Test Goal
    prime.submit_goal("Perform System Audit")
    prime.run_cycle()
