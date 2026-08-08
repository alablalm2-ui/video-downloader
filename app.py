from flask import Flask, render_template_string, request
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

html_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download Videos - منصة التحميل الذكية</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; 
            background-color: #000000; 
            color: #ffffff; 
            display: flex; 
            flex-direction: column;
            align-items: center; 
            min-height: 100vh; 
            padding: 20px;
        }
        header {
            width: 100%;
            max-width: 900px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        .logo {
            font-weight: 800;
            font-size: 22px;
            line-height: 1.1;
            color: #ffffff;
            text-transform: uppercase;
        }
        .logo span {
            color: #ccff00;
        }
        .menu-icon {
            font-size: 26px;
            cursor: pointer;
            color: #ffffff;
            background: none;
            border: none;
        }
        
        /* القائمة الجانبية المنبثقة */
        .menu-overlay {
            position: fixed;
            top: 0;
            right: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.96);
            z-index: 1000;
            display: none;
            flex-direction: column;
            padding: 20px;
            overflow-y: auto;
        }
        .menu-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            max-width: 800px;
            margin: 0 auto 30px auto;
        }
        .close-btn {
            font-size: 32px;
            color: #ffffff;
            background: none;
            border: none;
            cursor: pointer;
        }
        .menu-content {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }
        .menu-item {
            padding: 18px 0;
            border-bottom: 1px solid #222222;
            font-size: 18px;
            color: #ffffff;
            cursor: pointer;
            text-align: right;
            transition: 0.2s;
        }
        .menu-item:hover { color: #ccff00; }
        
        .languages-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 30px;
        }
        .lang-btn {
            background-color: #111111;
            border: 1px solid #333333;
            color: #ffffff;
            padding: 14px;
            border-radius: 8px;
            font-size: 15px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: 0.2s;
        }
        .lang-btn.active {
            background-color: #ccff00;
            color: #000000;
            border-color: #ccff00;
            font-weight: 700;
        }

        /* المحتوى الرئيسي */
        .main-container {
            width: 100%;
            max-width: 650px;
            text-align: center;
            margin-top: 20px;
        }
        h1 { 
            font-size: 38px; 
            font-weight: 700; 
            margin-bottom: 12px; 
            color: #ffffff;
        }
        .stats-main {
            font-size: 20px;
            font-weight: 700;
            color: #ccff00;
            margin-bottom: 6px;
        }
        .stats-sub {
            font-size: 14px;
            color: #777777;
            margin-bottom: 35px;
        }
        
        /* صندوق الإدخال الاحترافي */
        .input-box-wrapper {
            position: relative;
            background: #ffffff;
            border-radius: 12px;
            display: flex;
            align-items: center;
            padding: 6px;
            margin-bottom: 15px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.6);
        }
        input[type="text"] { 
            flex: 1;
            background: transparent; 
            border: none; 
            padding: 14px 16px; 
            color: #111111; 
            font-size: 16px; 
            outline: none; 
            text-align: right;
        }
        input[type="text"]::placeholder { color: #888888; }
        
        .paste-btn {
            background: #ccff00;
            color: #000000;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: 0.2s;
        }
        .paste-btn:hover { background: #b3e600; }

        .download-btn { 
            width: 100%; 
            background: #ccff00; 
            color: #000000; 
            border: none; 
            padding: 16px; 
            border-radius: 12px; 
            font-size: 18px; 
            font-weight: 800; 
            cursor: pointer; 
            transition: 0.2s; 
            box-shadow: 0 4px 20px rgba(204,255,0,0.25);
        }
        .download-btn:hover { 
            background: #b3e600; 
            transform: translateY(-1px); 
        }

        /* شريط التحميل التفاعلي */
        .progress-container {
            width: 100%;
            background-color: #222222;
            border-radius: 8px;
            margin-top: 20px;
            overflow: hidden;
            display: none;
        }
        .progress-bar {
            width: 0%;
            height: 8px;
            background-color: #ccff00;
            transition: width 0.4s ease;
        }
        .loading { margin-top: 15px; color: #ccff00; font-size: 15px; display: none; font-weight: 600; }
        
        .success { color: #000000; background: #ccff00; padding: 14px; border-radius: 10px; margin-top: 20px; font-weight: 700; word-break: break-all; }
        .error { color: #ff4d4d; background: rgba(255, 77, 77, 0.1); padding: 14px; border-radius: 10px; margin-top: 20px; border: 1px solid rgba(255, 77, 77, 0.3); font-size: 14px; text-align: left; direction: ltr; word-break: break-all; }
    </style>
</head>
<body>

    <!-- هيدر احترافي متناسق -->
    <header>
        <div class="logo">
            DOWNLOAD<br><span>VIDEOS</span>
        </div>
        <button class="menu-icon" onclick="toggleMenu()">☰</button>
    </header>

    <!-- القائمة الجانبية -->
    <div id="sideMenu" class="menu-overlay">
        <div class="menu-header">
            <div class="logo">
                DOWNLOAD<br><span>VIDEOS</span>
            </div>
            <button class="close-btn" onclick="toggleMenu()">✕</button>
        </div>
        <div class="menu-content">
            <div class="menu-item">تحميل الستوري</div>
            <div class="menu-item">تحميل السلايدشو</div>
            <div class="menu-item">تحميل TikTok Notes</div>
            <div class="menu-item">Douyin محمل</div>
            <div class="menu-item">تحميل TikTok MP3</div>
            <div class="menu-item">TikTok كيفية تحميل</div>

            <div class="languages-grid">
                <button class="lang-btn">🇬🇧 English</button>
                <button class="lang-btn active">🇸🇦 العربية</button>
                <button class="lang-btn">🇫🇷 Français</button>
                <button class="lang-btn">🇩🇪 Deutsch</button>
            </div>
        </div>
    </div>

    <div class="main-container">
        <h1>تحميل الفيديوهات</h1>
        <div class="stats-main">+4,233,226 videos downloaded</div>
        <div class="stats-sub">+1,472,165 users &nbsp;•&nbsp; 153 countries</div>

        <form method="POST" id="downloadForm" onsubmit="startDownload(event)">
            <div class="input-box-wrapper">
                <button type="button" class="paste-btn" onclick="pasteText()">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>
                    لصق
                </button>
                <input type="text" name="url" id="url-input" placeholder="ألصق الرابط هنا..." autocomplete="off" required oninput="hideSuccess()">
            </div>
            
            <button type="submit" id="sub-btn" class="download-btn">تحميل</button>
        </form>

        <div class="progress-container" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>
        <div id="loading-text" class="loading">جاري معالجة وسحب الفيديو بأعلى جودة...</div>

        {% if success %}
            <div class="success" id="success-box">
                <p>{{ success }}</p>
            </div>
        {% endif %}

        {% if error %}
            <div class="error">
                <p>{{ error }}</p>
            </div>
        {% endif %}
    </div>

    <script>
        function toggleMenu() {
            const menu = document.getElementById('sideMenu');
            menu.style.display = (menu.style.display === 'flex') ? 'none' : 'flex';
        }

        async function pasteText() {
            try {
                const text = await navigator.clipboard.readText();
                document.getElementById('url-input').value = text;
                hideSuccess();
            } catch (err) {
                alert('فشل اللصق تلقائياً، يمكنك الضغط بـ Ctrl + V يدوياً.');
            }
        }

        function startDownload(event) {
            // إظهار شريط التقدم وحالة التحميل التفاعلية
            document.getElementById('loading-text').style.display = 'block';
            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('sub-btn').innerText = 'جاري التحميل...';
            
            let progressBar = document.getElementById('progressBar');
            let width = 10;
            let interval = setInterval(() => {
                if (width >= 90) {
                    clearInterval(interval);
                } else {
                    width += 15;
                    progressBar.style.width = width + '%';
                }
            }, 200);
        }

        function hideSuccess() {
            const successBox = document.getElementById('success-box');
            if (successBox) { successBox.style.display = 'none'; }
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    success = None
    error = None
    if request.method == 'POST':
        video_url = request.form.get('url')
        if video_url:
            try:
                ydl_opts = {
                    'format': 'mp4/best',
                    'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                    'socket_timeout': 60,
                    'retries': 10,
                    'geo_bypass': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    title = info.get('title', 'فيديو')
                    
                success = f"تم تحميل وحفظ الفيديو بنجاح: {title}"
                    
            except Exception as e:
                error = f"Error: {str(e)}"
            
    return render_template_string(html_template, success=success, error=error)

if __name__ == '__main__':
    app.run(debug=True)