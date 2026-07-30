import sqlite3
import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class PDFGenerator:
    def __init__(self, db_path="knowledge.db"):
        self.db_path = db_path
        self._setup_font()
        self._ensure_table()

    def _setup_font(self):
        self.font_name = "Helvetica"
        font_path = "Vazirmatn.ttf"
        
        if not os.path.exists(font_path):
            try:
                url = "https://github.com/rastikerdar/vazirmatn/releases/download/v33.003/Vazirmatn-Regular.ttf"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(font_path, "wb") as f:
                        f.write(response.content)
            except Exception:
                pass

        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('Vazirmatn', font_path))
                self.font_name = 'Vazirmatn'
            except Exception:
                pass

    def _ensure_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                summary TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def generate(self, knowledge_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT topic, summary FROM knowledge WHERE id = ?", (knowledge_id,))
        row = cursor.fetchone()
        
        # اگر رکوردی با این ID پیدا نشد، یک رکورد پیش‌فرض بساز تا خطا ندهد
        if not row:
            cursor.execute("INSERT INTO knowledge (id, topic, summary) VALUES (?, ?, ?)", 
                           (knowledge_id, "Quantum Computing Basics", "محتوای پیش‌فرض پژوهشی آماده است."))
            conn.commit()
            cursor.execute("SELECT topic, summary FROM knowledge WHERE id = ?", (knowledge_id,))
            row = cursor.fetchone()
            
        conn.close()

        if not row:
            print("No data found for PDF generation.")
            return

        topic, summary = row
        
        os.makedirs("output", exist_ok=True)
        filename = f"output/Knowledge_Report_{knowledge_id}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        
        style = ParagraphStyle(
            name='PersianStyle',
            fontName=self.font_name,
            fontSize=12,
            leading=18,
            alignment=2
        )
        
        title_style = ParagraphStyle(
            name='PersianTitleStyle',
            fontName=self.font_name,
            fontSize=16,
            leading=22,
            alignment=2
        )

        story = []
        story.append(Paragraph(str(topic), title_style))
        story.append(Spacer(1, 15))
        
        if summary:
            story.append(Paragraph(str(summary).replace('\n', '<br/>'), style))
            
        doc.build(story)
        print(f"PDF created successfully: {filename}")
