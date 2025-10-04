from flask import Flask, Response, request
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route("/qr")
def generate_qr():
    # ?qr= প্যারামিটার থেকে ডাটা নেওয়া
    data = request.args.get("qr", "https://example.com")

    # QR বানানো
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # মাঝখানে NBR লেখা (যদি না লাগে, এই অংশ কমেন্ট করে দিতে পারেন)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", 40)
    except:
        font = ImageFont.load_default()
    text = "NBR"
    w, h = draw.textsize(text, font=font)
    pos = ((img.size[0] - w) // 2, (img.size[1] - h) // 2)
    draw.rectangle([pos[0]-10, pos[1]-5, pos[0]+w+10, pos[1]+h+5], fill="red")
    draw.text(pos, text, font=font, fill="white")

    # PNG রিটার্ন করা
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Response(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
