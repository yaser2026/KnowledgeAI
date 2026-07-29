import sqlite3
from pathlib import Path


DB = Path(__file__).resolve().parent.parent / "data" / "knowledge.db"


conn = sqlite3.connect(DB)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS knowledge_articles
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    title TEXT,
    summary TEXT,
    content TEXT,
    keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


conn.commit()

conn.close()


print("knowledge_articles table created")
