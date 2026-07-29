from core.database import Database


db = Database()

db.cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS jobs
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        status TEXT DEFAULT 'created',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)

db.conn.commit()

print("jobs table created")
