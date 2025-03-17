from flask import Flask, request, render_template, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64
from livereload import Server  # Live Reload 추가!

app = Flask(__name__)

# Pretendard SemiBold 폰트 경로
FONT_PATH = "static/fonts/Pretendard-SemiBold.otf"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_card', methods=['POST'])
def generate_card():
    name = request.form['name']
    date = request.form['date']
    stamp = request.form.get('stamp', '')

    # 🔥 슬라이더 값 받아오기 (기본값: 초기 위치)
    name_x = int(request.form.get('nameX', 280))
    name_y = int(request.form.get('nameY', 180))
    date_x = int(request.form.get('dateX', 280))
    date_y = int(request.form.get('dateY', 240))

    # 회원증 이미지 불러오기
    card = Image.open("static/images/card.png")
    draw = ImageDraw.Draw(card)

    # 폰트 로드
    try:
        font = ImageFont.truetype(FONT_PATH, 40)
    except IOError:
        return "Font file not found!", 500

    # 🔹 이름 & 날짜 위치 조정 (슬라이더 값 적용)
    draw.text((name_x, name_y), name, font=font, fill="black")
    draw.text((date_x, date_y), date, font=font, fill="black")

    # 도장 추가
    if stamp:
        stamp_path = f"static/images/{stamp}.png"
        if os.path.exists(stamp_path):
            stamp_img = Image.open(stamp_path).convert("RGBA")
            card.paste(stamp_img, (550, 300), stamp_img)

    # 🔥 회원증 크기 자동 조정 (너무 크지 않게 max-width: 350px)
    max_width = 350
    ratio = max_width / card.width
    new_size = (max_width, int(card.height * ratio))
    card = card.resize(new_size, Image.LANCZOS)

    # Base64 변환하여 미리보기 반환
    img_io = io.BytesIO()
    card.save(img_io, 'PNG')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return jsonify({'image': f"data:image/png;base64,{encoded_img}"})

# 🔥 Live Reload 설정 (코드 수정 시 자동 새로고침)
if __name__ == "__main__":
    server = Server(app)
    server.serve(port=5000)
