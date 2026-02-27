import os
import json
import logging
import time
from action_engine import ActionEngine
from treasury_router import TreasuryRouter

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] SovereignLogic: %(message)s')
logger = logging.getLogger("SovereignLogic")

class SovereignLogic:
    """
    The 'Brain' that coordinates 'Hands' (ActionEngine) and 'Wallet' (Treasury).
    Implements a Durable Protocol for autonomous state recovery.
    """
    def __init__(self):
        self.engine = ActionEngine()
        self.treasury = TreasuryRouter(target_operations_float=100.00)
        self.state_file = "sovereign_state.json"
        self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {"current_objective": "INITIALIZATION", "last_pulse": time.time()}
            self._save_state()

    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=4)

    def pulse(self):
        """Main decision loop."""
        logger.info(f"System Pulse: Current Objective - {self.state['current_objective']}")
        
        # 1. Check for revenue events (Simulated)
        # In a real scenario, this would check an API or log
        # self.treasury.process_incoming_revenue(0.0) 

        # 2. Update state
        self.state["last_pulse"] = time.time()
        self._save_state()

    def run_objective(self, objective: str, instructions: list):
        """
        Executes a complex objective transactionally.
        Example objective: 'UPGRADE_ENVIRONMENT'
        """
        self.state["current_objective"] = objective
        self._save_state()
        
        logger.info(f"Executing Objective: {objective}")
        for step in instructions:
            logger.info(f"Step: {step['description']}")
            if step['type'] == 'TERMINAL':
                res = self.engine.terminal.execute(step['cmd'])
                if not res['success']:
                    logger.error(f"Step failed: {res['stderr']}")
                    break
            elif step['type'] == 'FS_WRITE':
                self.engine.fs.write_file(step['path'], step['content'])
        
        self.state["current_objective"] = "IDLE"
        self._save_state()

if __name__ == "__main__":
    logic = SovereignLogic()
    
    # Example "Verse" Transaction:
    demo_steps = [
        {"type": "TERMINAL", "description": "Verify Python version", "cmd": "python --version"},
        {"type": "FS_WRITE", "description": "Update system manifest", "path": "system_manifest.json", "content": '{"version": "5.5-Sovereign", "status": "ALIVE"}'}
    ]
    
    logic.run_objective("INITIAL_MANIFEST_SYNC", demo_steps)
    
    try:
        while True:
            logic.pulse()
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("Sovereign Logic shutting down.")
