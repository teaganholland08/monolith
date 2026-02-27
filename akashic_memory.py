"""
AKASHIC MEMORY MATRIX - THE OMEGA TIER
Project Monolith vOmega
Infinite, immutable SQLite storage for all agent interactions, rules, and code snippets.
Allows the Swarm to query past conversations and self-correct across sessions.
"""
import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

class AkashicMemory:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.memory_dir = self.root / "Memory" / "Akashic"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.memory_dir / "akashic_record.db"
        self._init_db()

    def _init_db(self):
        """Builds the tables for infinite recall if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Table for learned rules and heuristics
        c.execute('''
            CREATE TABLE IF NOT EXISTS master_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_text TEXT NOT NULL UNIQUE,
                source_context TEXT,
                date_learned TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                profitability_score INTEGER DEFAULT 0
            )
        ''')
        
        # Table for conversation history / context
        c.execute('''
            CREATE TABLE IF NOT EXISTS conversation_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table for generated code snippets (the Verse/Python index)
        c.execute('''
            CREATE TABLE IF NOT EXISTS code_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                code_content TEXT NOT NULL,
                language TEXT,
                version INTEGER DEFAULT 1,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_rule(self, rule_text: str, context: str = ""):
        """Saves a new rule. Ignores duplicates automatically via UNIQUE constraint."""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('INSERT OR IGNORE INTO master_rules (rule_text, source_context) VALUES (?, ?)', 
                      (rule_text, context))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[AKASHIC] Rule Storage Error: {e}")
            return False

    def get_all_rules(self) -> list:
        """Retrieves all absolute truths learned by the Swarm."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT rule_text FROM master_rules ORDER BY profitability_score DESC, date_learned ASC')
        rules = [row[0] for row in c.fetchall()]
        conn.close()
        return rules

    def log_conversation(self, role: str, content: str):
        """Permanent record of inputs and outputs."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO conversation_log (role, content) VALUES (?, ?)', (role, content))
        conn.commit()
        conn.close()

    def get_recent_context(self, limit: int = 5) -> str:
        """Pulls the last N interactions to feed into the prompt."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT role, content FROM conversation_log ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()
        
        context = ""
        # Reverse to chronological order
        for row in reversed(rows):
            context += f"[{row[0].upper()}]: {row[1]}\n"
        return context

    def save_code(self, filename: str, code_content: str, language: str = "python"):
        """Saves physical code into the vault for the live-coder to reference or restore."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Check current version
        c.execute('SELECT MAX(version) FROM code_vault WHERE filename = ?', (filename,))
        result = c.fetchone()
        version = (result[0] or 0) + 1
        
        c.execute('INSERT INTO code_vault (filename, code_content, language, version) VALUES (?, ?, ?, ?)',
                  (filename, code_content, language, version))
        conn.commit()
        conn.close()
        return version

    def migrate_json_brain(self, json_path: str):
        """Ingests the legacy monolith_rules.json into the permanent database."""
        if not os.path.exists(json_path):
            return
            
        try:
            with open(json_path, 'r') as f:
                rules = json.load(f)
                
            for rule in rules:
                if isinstance(rule, str) and rule.strip():
                    self.add_rule(rule.strip(), "Legacy JSON Import")
                    
            # Rename the old file so we don't import it again
            os.rename(json_path, json_path + ".migrated")
            print(f"[AKASHIC] Successfully ingested {len(rules)} legacy rules into permanent memory.")
        except Exception as e:
            print(f"[AKASHIC] Migration failed: {e}")

if __name__ == "__main__":
    # Test the Matrix
    db = AkashicMemory()
    db.add_rule("Never use 3rd party UI frameworks. Build native.", "Command Center Update")
    db.log_conversation("ARCHITECT", "Make it remember forever.")
    db.log_conversation("SWARM", "Akashic Matrix Online.")
    print("Rules:", db.get_all_rules())
    print("Context:\n", db.get_recent_context())
