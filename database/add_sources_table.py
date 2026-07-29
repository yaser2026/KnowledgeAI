import sqlite3


DB = "data/knowledge.db"


conn = sqlite3.connect(DB)

cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS knowledge_sources
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    knowledge_id INTEGER,

    title TEXT,

    url TEXT,

    domain TEXT,

    quality_score INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


conn.commit()

conn.close()


print(
    "knowledge_sources table created"
)
