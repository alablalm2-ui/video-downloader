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
            margin-top: 25px;
        }
        .stats {
            color: #ccff00;
            font-size: 14px;
            margin-bottom: 30px;
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
        }
        /* نافذة القائمة الجانبية المنبثقة */
        .sidebar {
            height: 100%;
            width: 0;
            position: fixed;
            z-index: 1;
            top: 0;
            right: 0;
            background-color: #111;
            overflow-x: hidden;
            transition: 0.3s;
            padding-top: 60px;
            text-align: right;
        }
        .sidebar a {
            padding: 10px 25px;
            text-decoration: none;
            font-size: 18px;
            color: #fff;
            display: block;
            transition: 0.3s;
        }
        .sidebar a:hover {
            color: #ccff00;
        }
        .sidebar .close-btn {
            position: absolute;
            top: 15px;
            left: 20px;
            font-size: 25px;
        }
    </style>
</head>
<body>

    <div class="header">
        <div class="menu-icon" onclick="openNav()">☰</div>
        <div class="logo">DOWNLOAD<br><span>VIDEOS</span></div>
    </div>

    <!-- القائمة الجانبية الخيارات -->
    <div id="mySidebar" class="sidebar">
        <a href="javascript:void(0)" class="close-btn" onclick="closeNav()">&times;</a>
        <a href="#">الرئيسية</a>
        <a href="#">التحميلات الشائعة</a>
        <a href="#">من نحن</a>
        <a href="#">تواصل معنا</a>
    </div>

    <h1>تحميل الفيديوهات</h1>
    <div class="stats">videos downloaded 4,233,226+ <br> users • 153 countries 1,472,165+</div>

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
            document.getElementById("mySidebar").style.width = "250px";
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
