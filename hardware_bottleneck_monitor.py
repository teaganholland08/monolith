import time
import logging
import psutil
from typing import Dict, Any
from treasury_router import TreasuryRouter

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] Hardware Monitor: %(message)s')
logger = logging.getLogger("HardwareBottleneckMonitor")

class HardwareBottleneckMonitor:
    """
    Monitors the 'Body' (local machine). 
    When local CPU or RAM is consistently maxed out, it triggers the
    Physical Upgrade Protocol, sending funds/requests to order new parts.
    You (the human) are the 'Hands' that installs them.
    """
        # Number of checks required to trigger (checking if it's sustained, not just a spike)
        self.required_strikes = int((sustained_minutes * 60) / check_interval)
        self.current_strikes = 0
        self.treasury = TreasuryRouter()

    def check_system_resources(self) -> Dict[str, float]:
        """Checks current CPU and RAM usage percentages."""
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        return {"cpu": cpu_usage, "ram": ram_usage}

    def trigger_physical_upgrade_request(self):
        """
        The system realizes it needs a bigger body.
        It generates a request to order parts (GPU, RAM, etc.) to your door.
        """
        logger.warning(f"SUSTAINED BOTTLENECK DETECTED! Current Hardware is limiting AI revenue generation.")
        logger.info("Initiating Physical Upgrade Protocol...")
        
        upgrade_manifest = {
            "part_type": "GPU / RAM Expansion",
            "justification": "Sustained >90% resource saturation restricting API operations.",
            "estimated_budget_allocation": 800.00,
            "action": "Deducting from Operations Wallet. Preparing auto-order sequence to shipping address."
        }
        
        logger.info(f"Upgrade Request Generated: {upgrade_manifest}")
        
        # In a real scenario, this would trigger a treasury deduction event
        # self.treasury.process_incoming_revenue(-800.00) 
        
        logger.info("Awaiting HUMAN AVATAR (You) to perform physical installation upon delivery.")
        
        # Reset strikes so we don't spam orders
        self.current_strikes = 0

    def monitoring_loop(self):
        """Continuous evaluation of local hardware limitations."""
        logger.info(f"Starting Hardware Monitor. Bottleneck triggers at CPU > {self.cpu_threshold}% OR RAM > {self.ram_threshold}%")
        logger.info(f"Condition must be sustained for {self.required_strikes} consecutive checks.")
        
        try:
            while True:
                metrics = self.check_system_resources()
                logger.debug(f"Metrics - CPU: {metrics['cpu']}%, RAM: {metrics['ram']}%")
                
                if metrics["cpu"] > self.cpu_threshold or metrics["ram"] > self.ram_threshold:
                    self.current_strikes += 1
                    logger.warning(f"Resource spike detected. Strike {self.current_strikes}/{self.required_strikes}")
                    
                    if self.current_strikes >= self.required_strikes:
                        self.trigger_physical_upgrade_request()
                else:
                    if self.current_strikes > 0:
                        logger.info("Resources stabilized. Resetting strike counter.")
                    self.current_strikes = 0
                    
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("Hardware Monitor shutdown requested.")

if __name__ == "__main__":
    monitor = HardwareBottleneckMonitor(
        cpu_threshold=90.0, 
        ram_threshold=90.0, 
        check_interval=2, 
        sustained_minutes=0.1  # Very short for testing
    )
    
    # Run the loop. You can artificially spike CPU to see it trigger.
    monitor.monitoring_loop()
