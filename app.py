from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# قالب HTML الخاص بالموقع وتصميمك الاحترافي
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
        h1 {
            color: #fff;
            font-size: 28px;
            margin-top: 30px;
        }
        .stats {
            color: #ccff00;
            font-size: 16px;
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
        input[type="text"] {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border-radius: 10px;
            border: none;
            outline: none;
            box-sizing: border-box;
        }
        button {
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
        .success-box {
            background-color: #ccff00;
            color: #000;
            padding: 15px;
            border-radius: 10px;
            margin-top: 25px;
            font-weight: bold;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
</head>
<body>

    <h1>تحميل الفيديوهات</h1>
    <div class="stats">videos downloaded 4,233,226+ <br> users • 153 countries 1,472,165+</div>

    <form method="POST">
        <input type="text" name="url" placeholder="ألصق الرابط هنا..." required>
        <button type="submit">تحميل</button>
    </form>

    {% if downloaded %}
    <div class="success-box">
        تم تحميل وحفظ الفيديو بنجاح! سيتم تنزيله على جهازك الان 🐐🔥 #cr7 #capcut
    </div>
    {% endif %}

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    downloaded = False
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            output_filename = 'downloaded_video.mp4'
            
            # إزالة الملف القديم إذا كان موجوداً لتجنب التداخل
            if os.path.exists(output_filename):
                os.remove(output_filename)
                
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_filename,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # إرسال الملف مباشرة لجهاز المستخدم
                if os.path.exists(output_filename):
                    return send_file(output_filename, as_attachment=True)
            except Exception as e:
                print(f"Error: {e}")
                
    return render_template_string(HTML_TEMPLATE, downloaded=downloaded)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
