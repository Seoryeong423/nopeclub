from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_card', methods=['POST'])
def generate_card():
    name = request.form['name']
    date = request.form['date']
    stamp = request.form['stamp']

    # 회원증 이미지 불러오기
    card = Image.open("static/images/card.png")
    draw = ImageDraw.Draw(card)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)

    # 이름 & 날짜 추가
    draw.text((300, 200), name, font=font, fill="black")
    draw.text((300, 250), date, font=font, fill="black")

    # 도장 추가
    if stamp:
        stamp_img = Image.open(f"static/images/{stamp}.png").convert("RGBA")
        card.paste(stamp_img, (550, 300), stamp_img)

    # 이미지 저장 & 반환
    img_io = io.BytesIO()
    card.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="nopeclub_card.png")

if __name__ == "__main__":
    app.run(debug=True)