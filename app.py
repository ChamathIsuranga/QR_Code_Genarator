from flask import Flask, render_template, request,send_file
import qrcode
import io
import re


app = Flask(__name__)


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  
        r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|'
        r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return re.match(regex, url)

@app.route("/", methods=["GET", "Post"])

def index():
    qr_image = None
    if request.method =="POST":
        url = request.form["url"].strip()
        if not is_valid_url(url):
            return render_template("index.html", error="Invalid URL !!!, Please Enter Valid URL start with http:// or https://")
        
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")


        buf = io.BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)

        return send_file(buf, mimetype="image/png", as_attachment=False, download_name="qrcode.png")
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)