import sqlite3
import json
from datetime import datetime
import os

class SmartCache:
    def __init__(self, db_path="database/knowledge.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                data TEXT,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def get_cached_knowledge(self, topic):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, data FROM cache WHERE topic = ?", (topic.lower().strip(),))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0], json.loads(row[1])
        return None, None

    def save_to_cache(self, topic, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO cache (topic, data, created_at)
            VALUES (?, ?, ?)
        ''', (topic.lower().strip(), json.dumps(data), datetime.now()))
        conn.commit()
        conn.close()
