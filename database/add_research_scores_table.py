import sqlite3

DB = "data/knowledge.db"

conn = sqlite3.connect(DB)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS research_scores
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    knowledge_id INTEGER,

    source_count INTEGER,

    article_count INTEGER,

    average_quality REAL,

    score INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

print("research_scores table created")

conn.close()
