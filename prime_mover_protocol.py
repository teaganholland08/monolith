import time
import logging
import json
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] Prime Mover: %(message)s')
logger = logging.getLogger("PrimeMoverProtocol")

class PrimeMoverProtocol:
    """
    Biological Optimization Engine.
    Monitors the 'Human Avatar' to prevent burnout during massive scaling phases.
    Tracks Fuel (hydration/nutrition), Chassis (physical movement), and flow state momentum.
    """
    def __init__(self, log_path: str = "biological_telemetry.json"):
        self.log_path = log_path
        self.start_time = time.time()
        
        # Intervals in seconds
        self.hydration_interval = 60 * 45     # 45 minutes
        self.chassis_interval = 60 * 90       # 90 minutes
        self.fuel_interval = 60 * 60 * 4      # 4 hours
        
        self.last_hydration = self.start_time
        self.last_chassis = self.start_time
        self.last_fuel = self.start_time
        
        logger.info("Prime Mover Protocol Initiated. Syncing with Biological Avatar.")

    def log_telemetry(self, event_type: str, details: str):
        """Saves physical milestones to local telemetry log."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "details": details
        }
        
        data = []
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    pass
                    
        data.append(entry)
        
        with open(self.log_path, 'w') as f:
            json.dump(data, f, indent=4)

    def evaluate_biological_status(self):
        """Checks if the avatar requires maintenance."""
        current_time = time.time()
        
        # 1. Hydration
        if current_time - self.last_hydration > self.hydration_interval:
            logger.warning("BIOLOGICAL ALERT: Cognitive Output Degraded. Consume 16oz H2O immediately.")
            self.log_telemetry("PROMPT_HYDRATION", "Avatar prompted for water.")
            self.last_hydration = current_time

        # 2. Chassis Maintenance (Stretching/Movement)
        if current_time - self.last_chassis > self.chassis_interval:
            logger.warning("BIOLOGICAL ALERT: Chassis Integrity Compromised. Stand, stretch, or execute 20 pushups.")
            self.log_telemetry("PROMPT_CHASSIS", "Avatar prompted for physical exertion.")
            self.last_chassis = current_time

        # 3. High-Octane Fuel
        if current_time - self.last_fuel > self.fuel_interval:
            logger.warning("BIOLOGICAL ALERT: Fuel Empty. Required: High-protein, nutrient-dense meal to maintain coding momentum.")
            self.log_telemetry("PROMPT_FUEL", "Avatar prompted to refuel.")
            self.last_fuel = current_time

    def log_uninterrupted_flow(self):
        """Logs the momentum of the current coding session."""
        elapsed_hours = (time.time() - self.start_time) / 3600
        logger.info(f"Avatar Flow State Metrics: {elapsed_hours:.2f} uninterrupted tracking hours.")
        self.log_telemetry("FLOW_STATE", f"Sustained deep work session: {elapsed_hours:.2f} hours.")

    def monitoring_loop(self):
        """The eternal loop tracking the human."""
        logger.info("Engaging biological telemetry loop...")
        try:
            while True:
                self.evaluate_biological_status()
                
                # Every 30 minutes, log the flow state success
                if int((time.time() - self.start_time) % 1800) < 10:
                    self.log_uninterrupted_flow()
                    
                time.sleep(10)  # Check every 10 seconds
                
        except KeyboardInterrupt:
            self.log_telemetry("SHUTDOWN", "Avatar physically disconnected from terminal.")
            logger.info("Prime Mover Protocol offline.")

if __name__ == "__main__":
    protocol = PrimeMoverProtocol()
    
    # For testing purposes, force the alerts to trigger immediately 
    # by backdating the last tracked events.
    protocol.last_hydration -= 3000
    protocol.last_chassis -= 6000
    protocol.last_fuel -= 20000
    
    protocol.monitoring_loop()
