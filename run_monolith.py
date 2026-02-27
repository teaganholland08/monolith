import time
import sys
import threading
import os

from boss_agent import BossAgent
from sentinel_agent import SentinelAgent
from operative_agent import OperativeAgent
from cfo_agent import CFOAgent
from clo_agent import CLOAgent
from procurement_agent import ProcurementAgent
from connection_monitor import ConnectionMonitor
from ingestion_protocol import IngestionProtocol
from comm_link import CommLink
from genesis_engine import GenesisEngine

import dashboard_server

def load_environment():
    """Loads environment variables from the Secure Credentials Vault."""
    env_path = os.path.join("..", "Monolith_Archive", "CREDENTIALS_VAULT", ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

# Inject keys before boot
load_environment()

class MonolithEngine:
    """
    The Ignition Loop.
    Infinite loop wrapped in strict try/except for autonomous self-healing.
    """
    def __init__(self):
        print("Scaffolding Monolith Architecture...")
        self.boss = BossAgent()
        self.sentinel = SentinelAgent()
        self.operative = OperativeAgent()
        self.cfo = CFOAgent()
        self.clo = CLOAgent()
        self.procurement = ProcurementAgent()
        self.genesis = GenesisEngine()
        
        self.connection_monitor = ConnectionMonitor()
        self.comm_link = CommLink()
        self.ingestion = IngestionProtocol()
        self.cycles_run = 0

    def start_background_services(self):
        print("Igniting Background Services...")
        
        # 1. Dashboard Web Server
        dashboard_thread = threading.Thread(target=dashboard_server.start_server, daemon=True)
        dashboard_thread.start()

        # 2. Connection Monitor (Failsafe)
        monitor_thread = threading.Thread(target=self.connection_monitor.monitor_loop, daemon=True)
        monitor_thread.start()

        # 3. Comm-Link (Telegram)
        comm_thread = threading.Thread(target=self.comm_link.comm_loop, daemon=True)
        comm_thread.start()
        
        # 4. Background Ingestion
        ingest_thread = threading.Thread(target=self.ingestion.process_archive, daemon=True)
        ingest_thread.start()

    def engine_loop(self):
        # Strict try/except
        while True:
            try:
                # Check Kill Signal
                if os.path.exists("KILL_SIGNAL"):
                    print("KILL SIGNAL DETECTED. Terminating Monolith Swarm immediately.")
                    os.remove("KILL_SIGNAL") # Cleanup
                    sys.exit(0)

                # The heartbeat of the Swarm
                self.boss.run_cycle()
                self.sentinel.run_cycle()
                self.operative.run_cycle()
                self.cfo.run_cycle()
                self.clo.run_cycle()
                self.procurement.run_cycle()
                
                self.cycles_run += 1
                
                # Evolutionary Trigger (Zenith Protocol)
                if self.cycles_run % 3 == 0:  # Triggers every 3 cycles
                    print("\n*** ZENITH PROTOCOL ENGAGED ***")
                    mutant_class_name, mutant_file_path = self.genesis.synthesize_agent(specific_trait=random.choice(["hunter", "scraper", "analyst"]))
                    if mutant_class_name and mutant_file_path:
                        print(f"Executing Newly Synthesized DNA: {mutant_class_name}...")
                        try:
                            # Dynamic import of the newly created Python file
                            import importlib.util
                            spec = importlib.util.spec_from_file_location(mutant_class_name, mutant_file_path)
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            mutant_agent_instance = getattr(module, mutant_class_name)()
                            mutant_agent_instance.run_cycle()
                        except Exception as em:
                            print(f"Failed to execute Mutant Agent: {em}")

                time.sleep(5)  # Rest cycle

            except KeyboardInterrupt:
                print("\nManual Override Initiated. Shutting down gracefully.")
                sys.exit(0)
            except Exception as e:
                # Self-healing wrap
                print(f"CRITICAL ERROR in Ignition Loop: {e}. Executing Self-Healing Protocol.")
                # Could pass error to Sentinel here
                time.sleep(10)
                print("Rebooting components...")

if __name__ == "__main__":
    import random
    engine = MonolithEngine()
    engine.start_background_services()
    print("ALL SYSTEMS GO. ENTERING INFINITE IGNITION LOOP.")
    engine.engine_loop()
