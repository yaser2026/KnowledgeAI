import sqlite3
from deep_translator import GoogleTranslator

class ContentTranslator:
    def __init__(self, db_path="knowledge.db"):
        self.db_path = db_path
        self.translator = GoogleTranslator(source='auto', target='fa')

    def translate_knowledge(self, knowledge_id, target_lang="fa"):
        if target_lang != "fa":
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge';")
        if not cursor.fetchone():
            conn.close()
            return

        cursor.execute("SELECT topic, summary FROM knowledge WHERE id = ?", (knowledge_id,))
        row = cursor.fetchone()
        
        if row:
            topic, summary = row
            try:
                # ترجمه واقعی عنوان و خلاصه به فارسی به صورت رایگان
                translated_topic = self.translator.translate(topic)
                fa_topic = f"بررسی تخصصی: {translated_topic if translated_topic else topic}"
                
                if summary:
                    # ترجمه متن خلاصه
                    translated_summary = self.translator.translate(summary[:4500]) # محدودیت کاراکتر مترجم
                    fa_summary = translated_summary
                else:
                    fa_summary = "محتوای پژوهشی سنتز شده آماده است."
                
                cursor.execute("UPDATE knowledge SET topic = ?, summary = ? WHERE id = ?", (fa_topic, fa_summary, knowledge_id))
                conn.commit()
                print(f"[Translator] Knowledge ID {knowledge_id} successfully translated to Persian using GoogleTranslator.")
            except Exception as e:
                print(f"[Translator Error] Translation failed: {e}")
            
        conn.close()
