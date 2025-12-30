import qrcode

# Flask server manzili
url = "http://192.168.8.57:5000"

# QR kod yaratish
img = qrcode.make(url)
img.save("qr_sklad.png")
print("QR kod yaratildi: qr_sklad.png")
