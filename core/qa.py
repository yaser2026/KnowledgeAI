import sqlite3

class KnowledgeQA:
    def __init__(self, db_path="knowledge.db"):
        self.db_path = db_path

    def ask(self, knowledge_id, query):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT topic, summary FROM knowledge WHERE id = ?", (knowledge_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return "موضوعی با این شناسه یافت نشد."

        topic, summary = row
        query_words = [w for w in query.lower().split() if len(w) > 2]
        
        if not query_words:
            return f"پاسخ کلی در گزارش '{topic}':\n{summary}"

        # جستجوی ساده امتیازدهی بر اساس تطابق کلمات کلیدی
        match_score = sum(1 for word in query_words if word in summary.lower() or word in topic.lower())

        if match_score > 0 or any(w in topic.lower() for w in query_words):
            return f"پاسخ یافت شده در رابطه با گزارش '{topic}':\n{summary}\n\n(میزان تطابق کلمات کلیدی: {match_score} مورد)"
        else:
            return f"در گزارش '{topic}' اشاره مستقیم و بازیابی‌شده‌ای برای این عبارت خاص پیدا نشد. موضوع اصلی این گزارش پیرامون '{topic}' است."
