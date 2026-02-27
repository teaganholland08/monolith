"""
MONOLITH SCHEDULER
Persistent SQLite-based task queue for Monolith Core.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
import uuid

class MonolithScheduler:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to System/Logs/ledger.db standard
            self.db_path = Path(__file__).parent.parent.parent / "System" / "Logs" / "ledger.db"
        else:
            self.db_path = Path(db_path)
            
        self._init_db()
        
    def _init_db(self):
        """Ensure task table exists"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                data TEXT,
                priority INTEGER DEFAULT 1,
                status TEXT DEFAULT 'PENDING',
                created_at TEXT,
                scheduled_for TEXT,
                completed_at TEXT,
                result TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    def add_task(self, task_type, data={}, priority=1, delay_seconds=0):
        """Add a new task to queue"""
        task_id = str(uuid.uuid4())
        scheduled_for = (datetime.now() + timedelta(seconds=delay_seconds)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks 
            (id, type, data, priority, status, created_at, scheduled_for)
            VALUES (?, ?, ?, ?, 'PENDING', ?, ?)
        """, (
            task_id, 
            task_type, 
            json.dumps(data), 
            priority, 
            datetime.now().isoformat(),
            scheduled_for
        ))
        
        conn.commit()
        conn.close()
        return task_id
        
    def get_next_task(self):
        """Get highest priority pending task that is ready to run"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            SELECT id, type, data, priority
            FROM tasks
            WHERE status = 'PENDING' AND scheduled_for <= ?
            ORDER BY priority DESC, scheduled_for ASC
            LIMIT 1
        """, (now,))
        
        row = cursor.fetchone()
        
        if row:
            # Mark as RUNNING immediately so no other worker grabs it
            cursor.execute("UPDATE tasks SET status = 'RUNNING' WHERE id = ?", (row[0],))
            conn.commit()
            
            conn.close()
            return {
                "id": row[0],
                "type": row[1],
                "data": json.loads(row[2]) if row[2] else {},
                "priority": row[3]
            }
            
        conn.close()
        return None
        
    def complete_task(self, task_id, result=None):
        """Mark task as complete"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks 
            SET status = 'COMPLETE', completed_at = ?, result = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), json.dumps(result) if result else None, task_id))
        
        conn.commit()
        conn.close()
        
    def fail_task(self, task_id, error_message):
        """Mark task as failed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks 
            SET status = 'FAILED', completed_at = ?, result = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), json.dumps({"error": error_message}), task_id))
        
        conn.commit()
        conn.close()

    def get_pending_count(self):
        """Return number of pending tasks (for Operator Perception)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'PENDING'")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
