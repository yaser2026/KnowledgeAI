import os
import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

CONFIG_FILE = "config.json"

class KnowledgeAIApp:
    def __init__(self, db_path="knowledge.db"):
        self.db_path = db_path
        self.config = self._load_config()
        self._setup_font()
        self._ensure_table()

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"GEMINI_API_KEY": ""}

    def _save_config(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def set_api_key(self):
        print("\n--- تنظیم کلید API جمینای ---")
        current_key = self.config.get("GEMINI_API_KEY", "")
        if current_key:
            print(f"کلید فعلی: {current_key[:6]}...{current_key[-4:]}")
        
        new_key = input("لطفاً کلید API جدید خود را وارد کنید (یا اینتر بزنید تا تغییر نکند): ").strip()
        if new_key:
            self.config["GEMINI_API_KEY"] = new_key
            self._save_config()
            print("کلید API با موفقیت ذخیره شد.")
        else:
            print("تغییری ایجاد نشد.")

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

    def free_web_search(self, query):
        print("در حال جستجوی رایگان در وب...")
        try:
            url = f"https://html.duckduckgo.com/html/?q={query}"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"}
            response = requests.post(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                for a in soup.find_all('a', class_='result__snippet', limit=5):
                    results.append(a.get_text(strip=True))
                
                if results:
                    return "\n".join([f"- {res}" for res in results])
            
            return "محتوا یا نتیجه‌ای یافت نشد."
        except Exception as e:
            return f"خطا در جستجو: {str(e)}"

    def generate_ai_summary(self, topic, search_data):
        api_key = self.config.get("GEMINI_API_KEY", "")
        if not api_key:
            return f"موضوع: {topic}\n\n[حالت آفلاین] کلید Gemini API تنظیم نشده است. ابتدا از طریق منو کلید API خود را وارد کنید.\n\nنتایج جستجوی خام:\n{search_data}"
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            prompt = f"موضوع تحقیق: {topic}\n\nاطلاعات استخراج شده از وب:\n{search_data}\n\nلطفاً یک گزارش جامع، ساختاریافته و علمی به زبان فارسی بر اساس اطلاعات بالا بنویس."
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                res_json = response.json()
                return res_json['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"خطا در پاسخ هوش مصنوعی: {response.text}"
        except Exception as e:
            return f"خطا در ارتباط با هوش مصنوعی: {str(e)}"

    def save_to_db(self, topic, summary):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO knowledge (topic, summary) VALUES (?, ?)", (topic, summary))
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return record_id

    def generate_pdf(self, knowledge_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT topic, summary FROM knowledge WHERE id = ?", (knowledge_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            print("گزارشی با این شناسه یافت نشد.")
            return

        topic, summary = row
        os.makedirs("output", exist_ok=True)
        filename = f"output/Knowledge_Report_{knowledge_id}.pdf"

        doc = SimpleDocTemplate(filename, pagesize=letter)
        style = ParagraphStyle(name='PersianStyle', fontName=self.font_name, fontSize=12, leading=18, alignment=2)
        title_style = ParagraphStyle(name='PersianTitleStyle', fontName=self.font_name, fontSize=16, leading=22, alignment=2)

        story = [Paragraph(str(topic), title_style), Spacer(1, 15)]
        if summary:
            story.append(Paragraph(str(summary).replace('\n', '<br/>'), style))

        doc.build(story)
        print(f"فایل PDF گزارش با موفقیت ایجاد شد: {filename}")

    def list_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, topic FROM knowledge ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("\nهیچ گزارشی در تاریخچه وجود ندارد.")
            return

        print("\n--- تاریخچه گزارش‌های ذخیره‌شده ---")
        for r_id, topic in rows:
            print(f"[{r_id}] موضوع: {topic}")
        print("-" * 35)

        choice = input("شناسه (ID) گزارش مورد نظر را برای مشاهده متن یا بازسازی PDF وارد کنید (یا اینتر بزنید تا برگردید): ").strip()
        if choice.isdigit():
            self.view_report_detail(int(choice))

    def view_report_detail(self, knowledge_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT topic, summary FROM knowledge WHERE id = ?", (knowledge_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            print("گزارشی با این شناسه یافت نشد.")
            return

        topic, summary = row
        print(f"\n--- گزارش شماره {knowledge_id} ---")
        print(f"موضوع: {topic}\n")
        print(summary)
        print("-" * 40)

        make_pdf = input("آیا می‌خواهید فایل PDF این گزارش دوباره ساخته شود؟ (y/n): ").strip().lower()
        if make_pdf == 'y':
            self.generate_pdf(knowledge_id)

    def run_research(self):
        user_topic = input("\nموضوع تحقیق یا جستجوی خود را وارد کنید: ").strip()
        if not user_topic:
            print("موضوع نمی‌تواند خالی باشد.")
            return
        
        search_results = self.free_web_search(user_topic)
        print("در حال پردازش و تولید محتوا با هوش مصنوعی...")
        ai_report = self.generate_ai_summary(user_topic, search_results)
        
        rec_id = self.save_to_db(user_topic, ai_report)
        print(f"گزارش با موفقیت در دیتابیس ذخیره شد (شناسه: {rec_id})")
        
        make_pdf = input("آیا می‌خواهید فایل PDF این گزارش ساخته شود؟ (y/n): ").strip().lower()
        if make_pdf == 'y':
            self.generate_pdf(rec_id)

def main():
    app = KnowledgeAIApp()
    while True:
        print("\n=== منوی اصلی سیستم هوش مصنوعی KnowledgeAI ===")
        print("1. جستجوی جدید و تولید گزارش")
        print("2. مشاهده تاریخچه و مدیریت گزارش‌ها")
        print("3. تنظیم کلید API جمینای")
        print("4. خروج")
        
        choice = input("انتخاب شما (1-4): ").strip()
        
        if choice == "1":
            app.run_research()
        elif choice == "2":
            app.list_history()
        elif choice == "3":
            app.set_api_key()
        elif choice == "4":
            print("خروج از برنامه. موفق باشید!")
            break
        else:
            print("انتخاب نامعتبر. لطفاً عددی بین 1 تا 4 وارد کنید.")

if __name__ == "__main__":
    main()
