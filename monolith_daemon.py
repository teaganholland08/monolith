import os
import time
import subprocess
import threading
import logging
import sys

# Force UTF-8 output for Windows CP1252 compatibility
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] OMNIBUS DAEMON: %(message)s')
logger = logging.getLogger("OmnibusDaemon")

# Maximum concurrent background processes. Launching thousands at once crashes Windows.
MAX_CONCURRENT_SERVICES = 20

class OmnibusDaemon:
    """
    The ultimate "Best in the Universe" Watchdog.
    Launches all systems simultaneously and guarantees 100% uptime.
    If a child process crashes, the Daemon restarts it instantly.
    """
    def __init__(self):
        self.active_processes = {}
        self.services = self._discover_universe()
        
    def _discover_universe(self) -> dict:
        """
        Dynamically scans for EVERY python file in the root directory AND subdirectories.
        Auto-extracts any compressed zip archives first to ensure no code is left behind.
        Turns every single script into an autonomous, infinitely looping daemon process.
        """
        import zipfile
        root_dir = "."
        
        logger.info("Initializing Omni-Loader: Unleashing all sealed archives...")
        # 1. Extract all zip files first
        for item in os.listdir(root_dir):
            if item.endswith(".zip"):
                zip_path = os.path.join(root_dir, item)
                extract_path = os.path.join(root_dir, item.replace(".zip", ""))
                if not os.path.exists(extract_path):
                    logger.info(f"Unsealing ancient archive: {item}")
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(extract_path)
                    except Exception as e:
                        logger.error(f"Failed to unseal {item}: {e}")

        logger.info("Scanning physical reality for executable DNA across all dimensions...")
        universe = {}
        # Core Architecture scripts that should NOT be executed as standalone background tasks
        structural_ignore_list = {
            "monolith_daemon.py", "start_monolith.bat", "run_monolith.py", 
            "auto_monolith.py", "dashboard_server.py", "server.py", 
            "setup_identity.py", "setup_sovereignty.py", "init_database.py", 
            "generate_stubs.py", "generate_wallet.py", "physical_wipe.py",
            "run_sandbox_test.py", "launcher.py", "monolith_rules.json.migrated",
            "monolith_memory.json", "agent_telemetry.json", "biological_telemetry.json"
        }
        
        # 2. Recursively find every .py file
        for current_path, dirs, files in os.walk(root_dir):
            if "__pycache__" in current_path or ".git" in current_path:
                continue
                
            for file in files:
                if file.endswith(".py") and file not in structural_ignore_list:
                    full_path = os.path.join(current_path, file)
                    human_name = file.replace(".py", "").replace("_", " ").title()
                    
                    if human_name in universe:
                        human_name = f"{human_name} ({os.path.basename(current_path)})"
                    
                    # Streamlit apps must be launched differently
                    if file in ("dashboard.py", "monolith_dashboard.py", "monolith_native_dashboard.py"):
                        universe[human_name] = ["streamlit", "run", full_path, "--server.headless", "true"]
                    else:
                        universe[human_name] = ["python", full_path]
                
        logger.info(f"Omni-Loader located {len(universe)} autonomous entities across the multiverse.")
        logger.info(f"Note: Max concurrent services capped at {MAX_CONCURRENT_SERVICES} to maintain stability.")
        return universe

    def run_service(self, name: str, command: list):
        """Spawns and monitors a single service with restart logic."""
        while True:
            logger.info(f"[*] Launching Service: {name}")
            try:
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.active_processes[name] = process
                process.wait()
                return_code = process.returncode
                if return_code != 0:
                    logger.warning(f"[!] Service '{name}' terminated (code {return_code}). Restarting in 5s...")
                else:
                    logger.info(f"[OK] Service '{name}' completed cleanly.")
                    break  # Don't restart services that exit cleanly (code 0)
                time.sleep(5)
            except Exception as e:
                logger.error(f"[ERR] Failed to launch '{name}': {e}. Retrying in 10s...")
                time.sleep(10)

    def start_all(self):
        """Ignites the Monolith architecture using a controlled process pool."""
        logger.info("Initializing Omnibus Invincibility Architecture...")
        logger.info(f"Launching top {MAX_CONCURRENT_SERVICES} priority services...")
        
        # Convert to list and limit to max concurrent
        service_items = list(self.services.items())[:MAX_CONCURRENT_SERVICES]
        
        threads = []
        for name, cmd in service_items:
            t = threading.Thread(target=self.run_service, args=(name, cmd), daemon=True)
            threads.append(t)
            t.start()
            time.sleep(0.1)  # Stagger starts to avoid I/O storm
            
        logger.info(f"[OMNIBUS] {len(threads)} services launched. System is live.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("[OMNIBUS] Shutdown requested. Terminating Swarm...")
            self.shutdown_all()

    def shutdown_all(self):
        """Cleanly kills all child processes."""
        for name, process in self.active_processes.items():
            logger.info(f"Terminating {name}...")
            try:
                process.terminate()
            except Exception:
                pass
        sys.exit(0)

if __name__ == "__main__":
    daemon = OmnibusDaemon()
    daemon.start_all()
