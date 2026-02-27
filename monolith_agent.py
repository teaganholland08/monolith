import sqlite3
import json
import math
import datetime
import logging
import uuid

class LocalVectorDB:
    """
    A purely standard-library Local Vector Database for scalable memory.
    Uses SQLite to store JSON-encoded float vectors and text data.
    """
    def __init__(self, db_path="monolith_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    tag TEXT,
                    content TEXT,
                    vector TEXT
                )
            ''')
            conn.commit()

    def store_memory(self, tag, content, vector=None):
        """Stores a memory entry, optionally with a vector representation."""
        if vector is None:
            vector = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memory (timestamp, tag, content, vector) VALUES (?, ?, ?, ?)",
                (datetime.datetime.now().isoformat(), tag, content, json.dumps(vector))
            )
            conn.commit()

    def _cosine_similarity(self, vec1, vec2):
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        dot = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        mag1 = math.sqrt(sum(v1**2 for v1 in vec1))
        mag2 = math.sqrt(sum(v2**2 for v2 in vec2))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot / (mag1 * mag2)

    def search_memory(self, query_vector=None, tag=None, limit=5):
        """Searches memory by tag, or performs a simple brute-force cosine similarity search if vector is provided."""
        results = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if tag:
                cursor.execute("SELECT timestamp, tag, content, vector FROM memory WHERE tag = ? ORDER BY id DESC", (tag,))
            else:
                cursor.execute("SELECT timestamp, tag, content, vector FROM memory ORDER BY id DESC")
            
            rows = cursor.fetchall()
            for row in rows:
                v = json.loads(row[3])
                sim = self._cosine_similarity(query_vector, v) if query_vector else 1.0
                results.append({"timestamp": row[0], "tag": row[1], "content": row[2], "similarity": sim})
        
        if query_vector:
            results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]

class MonolithAgent:
    """
    Base Agent DNA for Project Monolith.
    Every specialized agent inherits from this class.
    """
    def __init__(self, name):
        self.name = name
        self.agent_uid = str(uuid.uuid4())
        self.memory = LocalVectorDB()
        self.logger = self._setup_logger()
        self.logger.info(f"[{self.name}] Agent Initialized with Zero-Trust ID: {self.agent_uid}.")

    def _setup_logger(self):
        logger = logging.getLogger(self.name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def log_action(self, action_name, result):
        self.logger.info(f"Action: {action_name} | Result: {result}")
        self.memory.store_memory(tag=self.name, content=json.dumps({"action": action_name, "result": result}))

    def run_cycle(self):
        """Standard loop cycle meant to be implemented by child classes."""
        raise NotImplementedError("run_cycle must be implemented by subclasses.")
