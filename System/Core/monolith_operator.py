"""
MONOLITH OPERATOR v2.0
The Autonomous Decision Engine.
Replaces static scheduling with dynamic goal decomposition.
"""

import json
import time
import uuid
from pathlib import Path
from datetime import datetime
import sys

# Import Factory
sys.path.append(str(Path(__file__).parents[2]))
try:
    from System.Agents.factory import AgentFactory
except ImportError:
    AgentFactory = None

class MonolithOperator:
    def __init__(self, core_ref):
        self.core = core_ref
        self.root = self.core.root
        self.config_path = self.root / "System" / "Config" / "operator_manifest.json"
        
        # Load Manifest
        self.manifest = self._load_manifest()
        
        # State
        self.goals = self.manifest.get("default_goals", [])
        self.last_cycle = 0
        self.cycle_interval = self.manifest.get("planning_parameters", {}).get("cycle_time_seconds", 60)
        
        # Tools
        self.factory = AgentFactory() if AgentFactory else None

    def _load_manifest(self):
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[OPERATOR] ⚠️ Manifest Load Error: {e}")
        return {}

    def cycle(self):
        """
        The Main Cognitive Loop:
        1. Perceive (Check State/Memory)
        2. Plan (Decompose Goals)
        3. Act (Dispatch Tasks to Scheduler)
        """
        now = time.time()
        if now - self.last_cycle < self.cycle_interval:
            return # Too soon
            
        print(f"\n[OPERATOR] 🧠 Cognitive Cycle Initiated at {datetime.now().isoformat()}")
        self.last_cycle = now
        
        # 1. Perception
        state = self._perceive_reality()
        
        # 2. Planning (Simple Heuristic for now, LLM later)
        new_tasks = self._plan_next_actions(state)
        
        # 3. Action
        if new_tasks:
            print(f"[OPERATOR] 📝 Generated {len(new_tasks)} tasks.")
            for task in new_tasks:
                self.core.scheduler.add_task(task['type'], task['data'], priority=task['priority'])
        else:
            print("[OPERATOR] 💤 No high-priority actions needed.")

    def _perceive_reality(self):
        """Gather Signal from sub-systems"""
        # Ask Sentinel for Status
        sentinel_ok = self.core.sentinel.run_bootstrap_check() if hasattr(self.core.sentinel, 'run_bootstrap_check') else True
        
        # Check Wallet (Reality)
        balance = 0.0
        if self.core.trade_protocol and self.core.trade_protocol.wallet:
             balance = self.core.trade_protocol.wallet.get_balance("ETH")
             
        return {
            "sentinel_status": sentinel_ok,
            "balance": balance,
            "active_tasks": self.core.scheduler.get_pending_count()
        }

    def _plan_next_actions(self, state):
        """Decide what to do based on state"""
        tasks = []
        
        # HEURISTIC 1: SURVIVAL
        # If balance is 0, we MUST find money.
        if state['balance'] <= 0.0001:
            print("[OPERATOR] 🚨 CRITICAL: POVERTY DETECTED. Prioritizing Revenue.")
            tasks.append({
                "type": "RUN_AGENT",
                "data": {
                    "agent_name": "omnidirectional_revenue_scanner", # Default scanner
                    "args": ["--mode", "fast"] 
                },
                "priority": 100
            })
            
        # HEURISTIC 2: MAINTENANCE
        # If no tasks are running, run a health check
        if state['active_tasks'] == 0:
            tasks.append({
                "type": "SYSTEM_MAINTENANCE",
                "data": {"action": "HEALTH_CHECK"},
                "priority": 10
            })
            
        # HEURISTIC 3: POPULATION GROWTH
        # Ensure we have our core workforce
        if self.factory:
            start_agents = ["scout_agent", "treasurer_agent"]
            for agent in start_agents:
                # Check if we know this agent (rough registry check)
                if agent + ".py" not in self.factory.registry:
                    print(f"[OPERATOR] 🐣 Missing capability '{agent}'. Ordering creation.")
                    tasks.append({
                        "type": "SPAWN_AGENT",
                        "data": {
                            "name": agent,
                            "role": "CORE_WORKER"
                        },
                        "priority": 90
                    })
            
        return tasks

    def _spawn_agent_handler(self, task_data):
        """Helper to call factory from task execution"""
        if self.factory:
            self.factory.spawn_agent(task_data['name'], task_data['role'])
