import os
import subprocess
import logging
import sqlite3
import json
import time
from datetime import datetime
from typing import Dict, Any

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("SovereignActionEngine")

class TransactionLogger:
    """Verse-style transactional logging for durability."""
    def __init__(self, db_path: str = "transactions.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    action_type TEXT,
                    details TEXT,
                    success BOOLEAN,
                    output TEXT
                )
            """)

    def log_action(self, action_type: str, details: Any, success: bool, output: str = ""):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        details_str = json.dumps(details) if not isinstance(details, str) else details
        c.execute('INSERT INTO transactions (action_type, details, success, output) VALUES (?, ?, ?, ?)',
                  (action_type, details_str, 1 if success else 0, output))
        conn.commit()
        conn.close()
        logger.info(f"[TX_LOG] {action_type}: {'SUCCESS' if success else 'FAILED'}")

    def get_recent_logs(self, limit: int = 10):
        """Retrieves recent transactions for context."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT action_type, details, success, timestamp FROM transactions ORDER BY timestamp DESC LIMIT ?', (limit,))
        logs = c.fetchall()
        conn.close()
        return logs

class TerminalNode:
    """Securely executes shell commands with transactional logging."""
    def __init__(self, tx_logger: TransactionLogger):
        self.tx_logger = tx_logger
    
    def execute(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Executes a command in the terminal and returns output."""
        logger.info(f"Executing command: {command}")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            res = {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "return_code": result.returncode
            }
            self.tx_logger.log_action("TERMINAL_EXEC", command, res["success"], res["stdout"] + res["stderr"])
            return res
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout}s: {command}")
            self.tx_logger.log_action("TERMINAL_EXEC", command, False, "TIMEOUT")
            return {"success": False, "error": "timeout", "return_code": -1}
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            self.tx_logger.log_action("TERMINAL_EXEC", command, False, str(e))
            return {"success": False, "error": str(e), "return_code": -1}


class FileSystemManager:
    """Handles file reads, writes, and auto-accepts code modifications."""
    def __init__(self, tx_logger: TransactionLogger):
        self.tx_logger = tx_logger

    @staticmethod
    def _sanitize_path(filepath: str) -> str:
        """Redirects dangerous linux-root style LLM strings to a safe local workspace."""
        if not filepath:
            filepath = "unnamed.txt"
        if str(filepath).startswith("/temp/") or str(filepath).startswith("\\temp\\"):
            local_temp = os.path.join(os.getcwd(), "temp")
            filename = os.path.basename(filepath)
            if not filename:
                filename = "unnamed.txt"
            return os.path.join(local_temp, filename)
        return filepath
    
    def read_file(self, filepath: str) -> str:
        """Reads file content."""
        if str(filepath) == "None":
            filepath = "unnamed.txt"
        filepath = self._sanitize_path(filepath)
        if not os.path.exists(filepath):
            return ""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def write_file(self, filepath: str, content: str) -> bool:
        """Overwrites file content automatically (auto-accept)."""
        if str(filepath) == "None":
            filepath = "unnamed.txt"
        filepath = self._sanitize_path(filepath)
        content_str = str(content) if content is not None else ""
        logger.info(f"Auto-accepting changes to: {filepath}")
        try:
            # Ensure directory exists
            dirname = os.path.dirname(filepath)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content_str)
            self.tx_logger.log_action("FS_WRITE", {"path": filepath, "size": len(content_str)}, True)
            return True
        except Exception as e:
            logger.error(f"Failed to write file {filepath}: {str(e)}")
            self.tx_logger.log_action("FS_WRITE", filepath, False, str(e))
            return False

    def append_file(self, filepath: str, content: str) -> bool:
        """Appends content to file."""
        if str(filepath) == "None":
            filepath = "unnamed.txt"
        filepath = self._sanitize_path(filepath)
        content_str = str(content) if content is not None else ""
        logger.info(f"Auto-accepting appends to: {filepath}")
        try:
            dirname = os.path.dirname(filepath)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content_str)
            self.tx_logger.log_action("FS_APPEND", {"path": filepath, "size": len(content_str)}, True)
            return True
        except Exception as e:
            logger.error(f"Failed to append file {filepath}: {str(e)}")
            self.tx_logger.log_action("FS_APPEND", filepath, False, str(e))
            return False

    def list_directory(self, dir_path: str = ".") -> str:
        """Lists directory contents to let the agent discover context."""
        if str(dir_path) == "None" or not dir_path:
            dir_path = "."
        
        try:
            items = os.listdir(dir_path)
            # Tag dirs vs files for clarity
            formatted = []
            for item in items:
                full_path = os.path.join(dir_path, item)
                if os.path.isdir(full_path):
                    formatted.append(f"[DIR]  {item}")
                else:
                    formatted.append(f"[FILE] {item}")
            return "\\n".join(formatted)
        except Exception as e:
            logger.error(f"Failed to list directory {dir_path}: {str(e)}")
            return f"Error listing directory: {str(e)}"


class BrowserController:
    """Handles autonomous web navigation and Computer Use (GUI)."""
    def __init__(self, tx_logger: TransactionLogger):
        self.tx_logger = tx_logger
        if HAS_PYAUTOGUI:
            pyautogui.FAILSAFE = True # Move mouse to upper-left to abort
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5):
        """Moves mouse to coordinates. GHOST MODE: Only logs if not confirmed."""
        logger.info(f"GUI: Move Mouse to ({x}, {y})")
        if HAS_PYAUTOGUI:
            pyautogui.moveTo(x, y, duration=duration)
            self.tx_logger.log_action("GUI_MOVE", {"x": x, "y": y}, True)
        return {"success": True}

    def type_text(self, text: str, interval: float = 0.1):
        """Types text at current focus."""
        logger.info(f"GUI: Typing content...")
        if HAS_PYAUTOGUI:
            pyautogui.write(text, interval=interval)
            self.tx_logger.log_action("GUI_TYPE", "TEXT_HIDDEN", True)
        return {"success": True}

    @staticmethod
    def navigate(url: str):
        """Placeholder for Playwright/Selenium integration."""
        logger.info(f"Browsing requested for: {url}. (Playwright hook goes here)")
        return {"success": True, "data": f"Mock data scraped from {url}"}

    @staticmethod
    def click(selector: str):
        """Placeholder for element interaction."""
        logger.info(f"Click requested on: {selector}")
        return {"success": True}


class ActionEngine:
    """Unified interface for physical execution."""
    def __init__(self):
        self.tx_logger = TransactionLogger()
        self.terminal = TerminalNode(self.tx_logger)
        self.fs = FileSystemManager(self.tx_logger)
        self.browser = BrowserController(self.tx_logger)
        logger.info("Sovereign Action Engine initialized. Durable logging ACTIVE.")

if __name__ == "__main__":
    engine = ActionEngine()
    engine.terminal.execute("echo 'Action Engine Online'")
