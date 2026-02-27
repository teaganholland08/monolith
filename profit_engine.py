import logging
import time
import random
import argparse
import os
from treasury_router import TreasuryRouter
from live_coder_engine import LiveCoderEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] ProfitEngine: %(message)s')
logger = logging.getLogger("ProfitEngine")

class ProfitEngine:
    """
    The financial aggressor of Project Monolith.
    Deploys and manages a swarm of agents specialized in revenue generation.
    """
    def __init__(self, mode="simulation"):
        self.treasury = TreasuryRouter()
        self.coder = LiveCoderEngine()
        self.mode = mode
        self.trade_history = [] # Tracks True (win) or False (loss)
        self.agents = [
            {"name": "ArbitrageScout", "status": "ACTIVE", "efficiency": 0.85},
            {"name": "SEO_Aggregator", "status": "ACTIVE", "efficiency": 0.92},
            {"name": "YieldHunter", "status": "ACTIVE", "efficiency": 0.78}
        ]

    def deploy_swarm(self):
        """Simulates the deployment of revenue-generating agents."""
        logger.info(f"Deploying swarm of {len(self.agents)} agents in {self.mode.upper()} mode...")
        for agent in self.agents:
            logger.info(f"Agent {agent['name']} is now HUNTING.")

    def trigger_evolution(self, win_rate):
        """Triggers the Live Coder to rewrite the arbitrage scout script."""
        logger.warning(f"Win rate fell to {win_rate*100:.1f}%. Triggering Algorithmic Evolution!")
        
        target_file = "arbitrage_scout.py"
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                current_code = f.read()
                
            success = self.coder.optimize_trading_logic(
                target_file_name=target_file,
                win_rate=win_rate,
                current_code=current_code
            )
            
            if success:
                logger.info("Evolution complete. Resetting trade history.")
                self.trade_history = []
        except Exception as e:
            logger.error(f"Failed to trigger evolution: {e}")

    def execute_paper_trade(self):
        """
        Executes a simulated paper trade based on real-time market data triggers.
        """
        logger.info("Executing Paper Trade based on live market trigger...")
        
        # Simulate win rate based on agent efficiency (approx 75% win rate)
        win_chance = random.random()
        
        if win_chance > 0.25:
            # Win
            profit = random.uniform(2.5, 15.0)
            logger.info(f"Paper Trade SUCCESS: +${profit:.2f} realized.")
            self.treasury.process_incoming_revenue(profit)
            self.trade_history.append(True)
        else:
            # Loss
            loss = random.uniform(1.0, 8.0)
            logger.warning(f"Paper Trade FAILED: -${loss:.2f} realized (drawdown).")
            self.treasury.process_drawdown(loss)
            self.trade_history.append(False)
            
        # Keep rolling window of last 5 trades to assess algorithm health
        if len(self.trade_history) > 5:
            self.trade_history.pop(0)
            
        if len(self.trade_history) == 5:
            win_rate = sum(self.trade_history) / len(self.trade_history)
            logger.info(f"Current algorithm win rate: {win_rate*100:.1f}%")
            if win_rate < 0.4:
                self.trigger_evolution(win_rate)

    def harvest_revenue(self):
        """
        Legacy simulation loop for background dripping of funds.
        """
        base_revenue = random.uniform(5.0, 50.0)
        multiplier = sum([a['efficiency'] for a in self.agents]) / len(self.agents)
        realized_revenue = base_revenue * multiplier
        
        logger.info(f"Swarm Harvested: ${realized_revenue:.2f}")
        self.treasury.process_incoming_revenue(realized_revenue)

    def run(self, interval: int = 60):
        """Main profit cycle."""
        self.deploy_swarm()
        
        if self.mode == "paper_trade":
            # Single execution if called directly by Prometheus
            self.execute_paper_trade()
            return
            
        while True:
            try:
                self.harvest_revenue()
            except Exception as e:
                logger.error(f"Profit Engine error: {e}")
            
            time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monolith Profit Engine")
    parser.add_argument("--mode", type=str, default="simulation", choices=["simulation", "paper_trade", "live"], help="Execution mode")
    args = parser.parse_args()
    
    engine = ProfitEngine(mode=args.mode)
    try:
        # If paper_trade, it runs once and exits, allowing Prometheus to trigger it dynamically
        engine.run(interval=20)
    except KeyboardInterrupt:
        logger.info("Profit Engine cooling down.")

