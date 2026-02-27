import urllib.request
import time
import logging

class ConnectionMonitor:
    """
    The Off-Grid Failsafe.
    Triggers a 'Dead Man's Switch' if the grid drops, shifting API endpoints 
    to localhost to run on local open-source AI models.
    """
    def __init__(self):
        self.logger = logging.getLogger("ConnectionMonitor")
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)
        self.grid_online = True
        self.api_endpoint = "https://api.openai.com/v1/"
        self.local_endpoint = "http://localhost:8080/v1/"

    def check_connection(self):
        try:
            # Check a highly available endpoint (like Google or Cloudflare DNS)
            urllib.request.urlopen('http://1.1.1.1', timeout=3)
            return True
        except Exception:
            return False

    def dead_mans_switch(self):
        """Shifts operation to local inference models."""
        self.logger.error("GRID DROPPED. DEAD MAN'S SWITCH ENGAGED.")
        self.api_endpoint = self.local_endpoint
        self.grid_online = False
        self.logger.info(f"API Endpoints shifted to {self.api_endpoint} (Local AI Models).")
        # Could also trigger Sentinel Scorched Earth here if required.

    def restore_grid(self):
        """Restores operation back to cloud APIs."""
        self.logger.info("GRID RESTORED. DISENGAGING DEAD MAN'S SWITCH.")
        self.api_endpoint = "https://api.openai.com/v1/"
        self.grid_online = True

    def monitor_loop(self):
        self.logger.info("Connection Monitor starting...")
        while True:
            online = self.check_connection()
            if online and not self.grid_online:
                self.restore_grid()
            elif not online and self.grid_online:
                self.dead_mans_switch()
            
            time.sleep(10) # Check every 10 seconds

if __name__ == "__main__":
    monitor = ConnectionMonitor()
    monitor.monitor_loop()
