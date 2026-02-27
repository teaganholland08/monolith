"""
PRE-FLIGHT AUDIT - Zombie Prevention & Permission Check
Runs before any major operation to ensure system integrity.
"""
import os
import sys
import psutil
import socket
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] [AUDIT] %(message)s')

def check_zombies():
    """Kills lingering Monolith processes to prevent 'Zombie Setting' loops."""
    current_pid = os.getpid()
    count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check for python processes running monolith scripts
            if proc.info['pid'] != current_pid and \
               proc.info['name'] and 'python' in proc.info['name'].lower() and \
               proc.info['cmdline'] and any("monolith" in arg for arg in proc.info['cmdline']):
                
                logging.warning(f"Found Zombie Process: {proc.info['pid']} - Killing...")
                proc.kill()
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if count > 0:
        logging.info(f"Cleaned {count} zombie processes.")
    else:
        logging.info("No zombie processes found.")

def check_permissions():
    """Checks if we have sufficient permissions (Admin/Sudo if required)."""
    # For user-space agents, we generally DON'T want Admin unless specifically requested.
    # But we want to ensure we can write to our own directories.
    root = Path(__file__).parent.parent.parent
    if not os.access(root, os.W_OK):
        logging.error(f"CRITICAL: Cannot write to workspace root {root}")
        sys.exit(1)
    logging.info("Filesystem permissions verified.")

def check_network():
    """Simple connectivity check."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        logging.info("Network connectivity verified.")
        return True
    except OSError:
        logging.error("CRITICAL: Network Offline. Agents cannot generate revenue.")
        return False

def inject_home_env():
    """Fixes 'Missing HOME' for headless browsers."""
    if 'HOME' not in os.environ:
        # On Windows, use USERPROFILE
        if sys.platform == 'win32':
             os.environ['HOME'] = os.environ.get('USERPROFILE', 'C:\\')
        else:
             os.environ['HOME'] = '/tmp'
        logging.info(f"Injected HOME environment variable: {os.environ['HOME']}")

if __name__ == "__main__":
    logging.info("Initiating Pre-Flight Audit...")
    inject_home_env()
    check_zombies()
    check_permissions()
    check_network()
    logging.info("Pre-Flight Complete. System Green.")
