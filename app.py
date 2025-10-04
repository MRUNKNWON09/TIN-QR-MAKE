from flask import Flask, Response, request
import qrcode
import io

app = Flask(__name__)

@app.route("/qr")
def generate_qr():
    try:
        # Query parameter থেকে ডাটা নেওয়া
        data = request.args.get("qr", "https://example.com")

        # QR জেনারেট করা
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # PNG আকারে রিটার্ন করা
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return Response(buf, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
