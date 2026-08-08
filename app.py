from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة التحميل الذكية - Download Videos</title>
    <style>
        body {
            background-color: #000;
            color: #fff;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 10px;
            max-width: 500px;
            margin: 0 auto;
        }
        .menu-icon {
            font-size: 26px;
            cursor: pointer;
            color: #fff;
        }
        .logo {
            font-size: 18px;
            font-weight: bold;
            color: #fff;
            line-height: 1.1;
            text-align: left;
        }
        .logo span {
            color: #ccff00;
        }
        h1 {
            color: #fff;
            font-size: 28px;
            margin-top: 20px;
        }
        .stats {
            color: #ccff00;
            font-size: 14px;
            margin-bottom: 25px;
        }
        /* قسم المنصات المدعومة الجديد */
        .platforms {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            max-width: 500px;
            margin: 0 auto 20px auto;
        }
        .platform-badge {
            background: #111;
            border: 1px solid #333;
            color: #ccc;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .platform-badge span {
            color: #ccff00;
            font-weight: bold;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
            max-width: 500px;
            margin: 0 auto;
        }
        .input-container {
            position: relative;
            width: 100%;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px 15px 15px 80px;
            font-size: 16px;
            border-radius: 10px;
            border: none;
            outline: none;
            box-sizing: border-box;
            background: #fff;
            color: #000;
            text-align: right;
        }
        .paste-btn {
            position: absolute;
            left: 8px;
            right: auto;
            top: 50%;
            transform: translateY(-50%);
            background: #ccff00;
            border: none;
            padding: 8px 14px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            color: #000;
            font-size: 14px;
        }
        button[type="submit"] {
            width: 100%;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            background-color: #ccff00;
            color: #000;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.2s;
        }
        button[type="submit"]:hover {
            background-color: #b3e600;
        }
        /* القائمة الجانبية المنبثقة المحسنة */
        .sidebar {
            height: 100%;
            width: 0;
            position: fixed;
            z-index: 10;
            top: 0;
            right: 0;
            background-color: #111;
            overflow-x: hidden;
            transition: 0.3s;
            padding-top: 60px;
            text-align: right;
            box-shadow: -5px 0 15px rgba(0,0,0,0.8);
        }
        .sidebar a {
            padding: 12px 25px;
            text-decoration: none;
            font-size: 18px;
            color: #fff;
            display: block;
            transition: 0.3s;
            border-bottom: 1px solid #222;
        }
        .sidebar a:hover {
            color: #ccff00;
            background: #1a1a1a;
        }
        .sidebar .close-btn {
            position: absolute;
            top: 15px;
            left: 20px;
            font-size: 30px;
            border: none;
            background: none;
            color: #fff;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <div class="header">
        <div class="menu-icon" onclick="openNav()">☰</div>
        <div class="logo">DOWNLOAD<br><span>VIDEOS</span></div>
    </div>

    <!-- القائمة الجانبية المحدثة ب الخيارات الحقيقية -->
    <div id="mySidebar" class="sidebar">
        <button class="close-btn" onclick="closeNav()">&times;</button>
        <a href="#" onclick="closeNav()">🏠 الرئيسية</a>
        <a href="#" onclick="alert('الموقع يدعم التحميل من يوتيوب، تيك توك، انستغرام، فيسبوك وتويتر بجودة عالية مجاناً!')">📌 المنصات المدعومة</a>
        <a href="#" onclick="alert('منصة التحميل الذكية الإصدار 2.0 - صُممت لتلبي احتياجاتك بكل سرعة واحترافية.')">ℹ️ عن الموقع</a>
        <a href="#" onclick="alert('للدعم والاستفسار، تواصل عبر حساباتنا الرسمية.')">📞 تواصل معنا</a>
    </div>

    <h1>تحميل الفيديوهات</h1>
    <div class="stats">videos downloaded 4,233,226+ <br> users • 153 countries 1,472,165+</div>

    <!-- شريط المنصات المدعومة -->
    <div class="platforms">
        <div class="platform-badge">🔴 <span>YouTube</span></div>
        <div class="platform-badge">⚫ <span>TikTok</span></div>
        <div class="platform-badge">🟣 <span>Instagram</span></div>
        <div class="platform-badge">🔵 <span>Facebook</span></div>
        <div class="platform-badge">🩵 <span>Twitter/X</span></div>
    </div>

    <form method="POST">
        <div class="input-container">
            <input type="text" id="urlInput" name="url" placeholder="ألصق الرابط هنا..." required>
            <button type="button" class="paste-btn" onclick="pasteText()">لصق</button>
        </div>
        <button type="submit">تحميل</button>
    </form>

    <script>
        async function pasteText() {
            try {
                const text = await navigator.clipboard.readText();
                document.getElementById('urlInput').value = text;
            } catch (err) {
                alert('فشل اللصق تلقائياً، قم باللصق يدوياً.');
            }
        }

        function openNav() {
            document.getElementById("mySidebar").style.width = "260px";
        }

        function closeNav() {
            document.getElementById("mySidebar").style.width = "0";
        }
    </script>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            output_filename = 'downloaded_video.mp4'
            if os.path.exists(output_filename):
                os.remove(output_filename)
                
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_filename,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                if os.path.exists(output_filename):
                    return send_file(output_filename, as_attachment=True)
            except Exception as e:
                print(f"Error: {e}")
                
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
