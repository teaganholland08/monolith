import time
import json
import logging
import os
from sovereign_logic import SovereignLogic
from akashic_memory import AkashicMemory

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] Prometheus: %(message)s')
logger = logging.getLogger("PrometheusLoop")

class PrometheusLoop:
    """
    The 'Spark of Life' for Project Monolith.
    Continuously observes system state, reasons through goals, and executes via SovereignLogic.
    """
    def __init__(self, reasoning_interval: int = 30):
        self.logic = SovereignLogic()
        self.memory = AkashicMemory()
        self.interval = reasoning_interval
        self.active = True

    def observe(self):
        """Gather current system context including live market data."""
        latest_market_data = []
        memory_file = os.path.join("./data/miner/", "brain_memory.json")
        if os.path.exists(memory_file):
            try:
                # Read the last 50 lines of memory to find recent market data
                with open(memory_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[-50:]
                    for line in lines:
                        if "MARKET DATA" in line:
                            data = json.loads(line)
                            for filename, content in data.items():
                                latest_market_data.append(content)
            except Exception as e:
                logger.error(f"Failed to read market memory: {e}")

        context = {
            "objective": self.logic.state.get("current_objective", "IDLE"),
            "last_logs": self.logic.engine.tx_logger.get_recent_logs(5),
            "balances": self.logic.treasury.operations_wallet_balance,
            "rules": self.memory.get_all_rules()[:5],
            "market_data": latest_market_data[-3:] # Last 3 ticker updates
        }
        return context

    def think(self, context):
        """
        In a full deployment, this would call a Cloud LLM (Gemini/Groq/Claude).
        For now, we implement a 'Heuristic Reasoner' that prioritizes growth and stability.
        """
        logger.info(f"Thinking... Context: {context['objective']} | Signals: {len(context['market_data'])}")
        
        # Heuristic 0: React to Live Market Data
        if context["market_data"]:
            logger.info(f"Market Signal Detected: {context['market_data'][0]}")
            return {
                "decision": "EXECUTE_ARBITRAGE_TRADE",
                "reasoning": f"Live market data ingested. Triggering Profit Engine to analyze: {context['market_data'][0]}",
                "steps": [
                    {"type": "TERMINAL", "description": "Trigger Live Trading / Arbitrage", "cmd": "python profit_engine.py --mode paper_trade"}
                ]
            }

        # Heuristic 1: If idle, look for revenue
        if context["objective"] == "IDLE":
            return {
                "decision": "START_REVENUE_HUNT",
                "reasoning": "System is idle. Treasury requires replenishment for growth.",
                "steps": [
                    {"type": "TERMINAL", "description": "Scan for arbitrage opportunities", "cmd": "python arbitrage_scout.py --scan"}
                ]
            }
        
        # Heuristic 2: If healthy, optimize code
        if context["balances"] > 200.00:
             return {
                "decision": "CODE_SELF_OPTIMIZATION",
                "reasoning": "High liquidity detected. Optimizing core routines for speed.",
                "steps": [
                    {"type": "TERMINAL", "description": "Run diagnostic suite", "cmd": "python omni_diagnostic.py"}
                ]
            }

        return {"decision": "WAIT", "reasoning": "Stable operations. Awaiting external triggers or state changes."}

    def act(self, plan):
        """Execute the decision via SovereignLogic."""
        if plan["decision"] == "WAIT":
            return
            
        logger.info(f"Decision: {plan['decision']} | {plan['reasoning']}")
        self.logic.run_objective(plan["decision"], plan["steps"])
        
        # Store successful patterns in Akashic Memory
        self.memory.add_rule(f"Objective {plan['decision']} executed successfully.", "Prometheus Feedback Loop")

    def run(self):
        """The eternal loop."""
        logger.info("Prometheus Loop IGNITED. The Monolith is now thinking.")
        while self.active:
            try:
                context = self.observe()
                plan = self.think(context)
                self.act(plan)
            except Exception as e:
                logger.error(f"Prometheus Loop encountered an error: {e}")
                time.sleep(10) # Failsafe delay
            
            time.sleep(self.interval)

if __name__ == "__main__":
    prometheus = PrometheusLoop()
    try:
        prometheus.run()
    except KeyboardInterrupt:
        logger.info("Prometheus Loop extinguished.")
