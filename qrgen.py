import qrcode

qr = qrcode.QRCode(
  version=1,
  error_correction=qrcode.constants.ERROR_CORRECT_L,
  box_size=3,
  border=2,
)

# Bitcoin donation address. Any BTC fraction is welcome!
qr.add_data('18U7Ci1wSuMXDJbgkKJwVLK9cs52ZtzL16')
qr.make(fit=True)

img = qr.make_image().convert('RGBA')
img.save("qrcode.png")
