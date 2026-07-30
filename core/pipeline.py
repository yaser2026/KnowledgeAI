import sqlite3

class Pipeline:
    def __init__(self, db_path="knowledge.db"):
        self.db_path = db_path
        self.last_job_id = 1

    def run(self, topic, max_results=5):
        print(f"[Pipeline] Simulating web research and collecting articles for: {topic}")
        
        # تولید مقالات شبیه‌سازی شده معتبر برای پر شدن بخش منابع
        articles = [
            {
                "title": f"Introduction to {topic}",
                "snippet": f"This article covers the fundamental concepts and core principles of {topic}.",
                "url": f"https://example.com/research/{topic.lower().replace(' ', '-')}-1"
            },
            {
                "title": f"Advanced Aspects of {topic}",
                "snippet": f"Exploring deep technical implementation, architecture, and use cases of {topic}.",
                "url": f"https://example.com/research/{topic.lower().replace(' ', '-')}-2"
            }
        ]

        # ذخیره مقالات در پایگاه داده
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                title TEXT,
                snippet TEXT,
                url TEXT
            )
        ''')
        for art in articles:
            cursor.execute("INSERT INTO articles (job_id, title, snippet, url) VALUES (?, ?, ?, ?)",
                           (self.last_job_id, art['title'], art['snippet'], art['url']))
        conn.commit()
        conn.close()

        return articles
