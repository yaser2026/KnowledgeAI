import os
import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, request, jsonify, send_from_directory

app = Flask(__name__)
CONFIG_FILE = "config.json"
DB_PATH = "knowledge.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("output", exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"GEMINI_API_KEY": ""}

def save_config(config_data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)

def ensure_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

ensure_table()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-color: #f8f9fa;
            --sidebar-bg: #f0f4f9;
            --text-color: #1f1f1f;
            --text-secondary: #444746;
            --border-color: #e0e0e0;
            --input-bg: #f0f4f9;
            --card-bg: #ffffff;
            --hover-bg: #e2e7ec;
            --accent-color: #0b57d0;
        }

        [data-theme="dark"] {
            --bg-color: #131314;
            --sidebar-bg: #1e1f20;
            --text-color: #e3e3e3;
            --text-secondary: #c4c7c5;
            --border-color: #333537;
            --input-bg: #1e1f20;
            --card-bg: #1e1f20;
            --hover-bg: #333537;
            --accent-color: #a8c7fa;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Vazirmatn', sans-serif;
            transition: background-color 0.3s, color 0.3s;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        sidebar {
            width: 280px;
            background-color: var(--sidebar-bg);
            border-left: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 12px;
            z-index: 10;
        }

        .sidebar-top {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .menu-btn {
            background: none;
            border: none;
            color: var(--text-color);
            font-size: 18px;
            cursor: pointer;
            padding: 8px;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .menu-btn:hover { background-color: var(--hover-bg); }

        .new-chat-btn {
            display: flex;
            align-items: center;
            gap: 10px;
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 10px 16px;
            border-radius: 24px;
            cursor: pointer;
            font-size: 14px;
            color: var(--text-color);
            font-weight: 500;
            width: fit-content;
        }
        .new-chat-btn:hover { background-color: var(--hover-bg); }

        .history-section {
            margin-top: 20px;
            overflow-y: auto;
            max-height: calc(100vh - 200px);
        }

        .history-title {
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 8px;
            padding-right: 8px;
        }

        .history-item {
            padding: 10px 12px;
            border-radius: 16px;
            cursor: pointer;
            font-size: 13px;
            color: var(--text-color);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .history-item:hover { background-color: var(--hover-bg); }

        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100vh;
            position: relative;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: 500;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background-color: var(--accent-color);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            cursor: pointer;
        }

        .chat-area {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
        }

        .welcome-msg {
            font-size: 32px;
            font-weight: 500;
            background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 40px;
        }

        .message {
            display: flex;
            gap: 15px;
            max-width: 100%;
            line-height: 1.8;
            font-size: 15px;
        }

        .message.user {
            flex-direction: row-reverse;
        }

        .message .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .message.user .avatar { background-color: #5f6368; color: white; }
        .message.ai .avatar { background: linear-gradient(135deg, #4285f4, #9b72cb); color: white; }

        .message .content {
            background-color: var(--card-bg);
            padding: 12px 18px;
            border-radius: 18px;
            border: 1px solid var(--border-color);
            max-width: 80%;
            word-break: break-word;
        }

        .input-container-wrapper {
            padding: 20px;
            display: flex;
            justify-content: center;
            background: transparent;
        }

        .input-box {
            max-width: 800px;
            width: 100%;
            background-color: var(--input-bg);
            border: 1px solid var(--border-color);
            border-radius: 32px;
            display: flex;
            align-items: center;
            padding: 8px 16px;
            gap: 10px;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        }

        .input-box input {
            flex: 1;
            background: none;
            border: none;
            outline: none;
            color: var(--text-color);
            font-size: 15px;
            padding: 8px;
        }

        .input-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .action-icon {
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 18px;
            cursor: pointer;
            padding: 8px;
            border-radius: 50%;
        }
        .action-icon:hover { color: var(--text-color); background-color: var(--hover-bg); }

        .send-btn {
            background-color: var(--text-color);
            color: var(--bg-color);
            border: none;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .send-btn:hover { opacity: 0.9; }

        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
            z-index: 100;
        }
        .modal-content {
            background: var(--card-bg);
            padding: 24px;
            border-radius: 16px;
            width: 400px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            border: 1px solid var(--border-color);
        }
        .modal-content input {
            padding: 10px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background: var(--input-bg);
            color: var(--text-color);
        }
        .modal-buttons {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }
        .btn { padding: 8px 16px; border-radius: 8px; border: none; cursor: pointer; }
        .btn-primary { background: var(--accent-color); color: white; }
    </style>
</head>
<body data-theme="light">

    <sidebar>
        <div class="sidebar-top">
            <button class="menu-btn"><i class="fa-solid fa-bars"></i></button>
            <button class="new-chat-btn" onclick="newChat()"><i class="fa-solid fa-plus"></i> چت جدید</button>
            
            <div class="history-section">
                <div class="history-title">تاریخچه</div>
                <div id="history-list"></div>
            </div>
        </div>
        <div class="sidebar-bottom">
            <button class="menu-btn" onclick="openSettings()"><i class="fa-solid fa-gear"></i> تنظیمات API</button>
        </div>
    </sidebar>

    <div class="main-container">
        <header>
            <div class="header-right">
                <span>Gemini</span>
            </div>
            <div class="header-left">
                <button class="action-icon" onclick="toggleTheme()"><i class="fa-solid fa-moon" id="theme-icon"></i></button>
                <div class="user-avatar" onclick="openSettings()">U</div>
            </div>
        </header>

        <div class="chat-area" id="chat-area">
            <div class="welcome-msg" id="welcome-text">سلام، چطور می‌توانم کمک کنم؟</div>
        </div>

        <div class="input-container-wrapper">
            <div class="input-box">
                <input type="file" id="file-input" style="display:none" onchange="handleFileUpload()">
                <button class="action-icon" onclick="document.getElementById('file-input').click()" title="آپلود فایل"><i class="fa-solid fa-paperclip"></i></button>
                <input type="text" id="user-input" placeholder="پرسش از جمینای..." onkeypress="if(event.key === 'Enter') sendMessage()">
                <div class="input-actions">
                    <button class="action-icon" onclick="startMic()" title="میکروفون"><i class="fa-solid fa-microphone" id="mic-icon"></i></button>
                    <button class="send-btn" onclick="sendMessage()"><i class="fa-solid fa-arrow-up"></i></button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal" id="settings-modal">
        <div class="modal-content">
            <h3>تنظیم کلید Gemini API</h3>
            <input type="text" id="api-key-input" placeholder="کلید API خود را وارد کنید...">
            <div class="modal-buttons">
                <button class="btn" onclick="closeSettings()">انصراف</button>
                <button class="btn btn-primary" onclick="saveApiKey()">ذخیره</button>
            </div>
        </div>
    </div>

    <script>
        function toggleTheme() {
            const body = document.body;
            const icon = document.getElementById('theme-icon');
            if (body.getAttribute('data-theme') === 'light') {
                body.setAttribute('data-theme', 'dark');
                icon.className = 'fa-solid fa-sun';
            } else {
                body.setAttribute('data-theme', 'light');
                icon.className = 'fa-solid fa-moon';
            }
        }

        function openSettings() {
            document.getElementById('settings-modal').style.display = 'flex';
            fetch('/get-key').then(res => res.json()).then(data => {
                document.getElementById('api-key-input').value = data.key;
            });
        }

        function closeSettings() {
            document.getElementById('settings-modal').style.display = 'none';
        }

        function saveApiKey() {
            const key = document.getElementById('api-key-input').value;
            fetch('/save-key', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({key: key})
            }).then(() => closeSettings());
        }

        function newChat() {
            document.getElementById('chat-area').innerHTML = '<div class="welcome-msg" id="welcome-text">سلام، چطور می‌توانم کمک کنم؟</div>';
        }

        function loadHistory() {
            fetch('/history').then(res => res.json()).then(data => {
                const list = document.getElementById('history-list');
                list.innerHTML = '';
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'history-item';
                    div.innerText = item.topic;
                    div.onclick = () => loadReport(item.id);
                    list.appendChild(div);
                });
            });
        }

        function loadReport(id) {
            fetch('/report/' + id).then(res => res.json()).then(data => {
                const chatArea = document.getElementById('chat-area');
                chatArea.innerHTML = '';
                appendMessage(data.topic, 'user');
                appendMessage(data.summary, 'ai');
            });
        }

        function appendMessage(text, sender) {
            const chatArea = document.getElementById('chat-area');
            const welcome = document.getElementById('welcome-text');
            if (welcome) welcome.remove();

            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.innerHTML = sender === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-wand-magic-sparkles"></i>';
            
            const content = document.createElement('div');
            content.className = 'content';
            content.innerHTML = text.replace(/\\n/g, '<br>');

            msgDiv.appendChild(avatar);
            msgDiv.appendChild(content);
            chatArea.appendChild(msgDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('user-input');
            const query = input.value.trim();
            if (!query) return;

            appendMessage(query, 'user');
            input.value = '';

            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: query})
            }).then(res => res.json()).then(data => {
                appendMessage(data.response, 'ai');
                loadHistory();
            });
        }

        function handleFileUpload() {
            const fileInput = document.getElementById('file-input');
            const file = fileInput.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            appendMessage(`آپلود فایل: ${file.name}`, 'user');

            fetch('/upload', {
                method: 'POST',
                body: formData
            }).then(res => res.json()).then(data => {
                appendMessage(data.message, 'ai');
            });
        }

        function startMic() {
            const micIcon = document.getElementById('mic-icon');
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                alert('مرورگر شما از جستجوی صوتی پشتیبانی نمی‌کند.');
                return;
            }
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = 'fa-IR';
            
            micIcon.style.color = '#ea4335';
            recognition.onresult = function(event) {
                document.getElementById('user-input').value = event.results[0][0].transcript;
                micIcon.style.color = '';
            };
            recognition.onerror = function() { micIcon.style.color = ''; };
            recognition.onend = function() { micIcon.style.color = ''; };
            recognition.start();
        }

        loadHistory();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/get-key")
def get_key():
    config = load_config()
    return jsonify({"key": config.get("GEMINI_API_KEY", "")})

@app.route("/save-key", methods=["POST"])
def save_key():
    data = request.json
    config = load_config()
    config["GEMINI_API_KEY"] = data.get("key", "")
    save_config(config)
    return jsonify({"status": "success"})

@app.route("/history")
def history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, topic FROM chats ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "topic": r[1]} for r in rows])

@app.route("/report/<int:report_id>")
def get_report(report_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT topic, summary FROM chats WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"topic": row[0], "summary": row[1]})
    return jsonify({"error": "Not found"}), 404

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    topic = data.get("query", "")
    
    search_data = ""
    try:
        url = f"https://html.duckduckgo.com/html/?q={topic}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.post(url, headers=headers, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            snippets = [a.get_text(strip=True) for a in soup.find_all('a', class_='result__snippet', limit=5)]
            search_data = "\n".join([f"- {s}" for s in snippets])
    except:
        search_data = "خطا در جستجو"

    config = load_config()
    api_key = config.get("GEMINI_API_KEY", "")
    
    if not api_key:
        ai_response = f"[حالت آفلاین] کلید API تنظیم نشده است. نتایج جستجو:\n{search_data}"
    else:
        try:
            ai_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            prompt = f"موضوع: {topic}\nاطلاعات وب:\n{search_data}\nیک پاسخ جامع به زبان فارسی بنویس."
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            ai_res = requests.post(ai_url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
            if ai_res.status_code == 200:
                ai_response = ai_res.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                ai_response = f"خطا در هوش مصنوعی: {ai_res.text}"
        except Exception as e:
            ai_response = f"خطا: {str(e)}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (topic, summary) VALUES (?, ?)", (topic, ai_response))
    conn.commit()
    conn.close()

    return jsonify({"response": ai_response})

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"message": "فایلی ارسال نشد"})
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"message": f"فایل {file.filename} با موفقیت بارگذاری و ذخیره شد."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
