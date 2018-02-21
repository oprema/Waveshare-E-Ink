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
img.save("images/qrcode-btc.png")

qr.add_data('0x0F24D31a3a632F4205CBe8025cc13e86ff80a48e')
qr.make(fit=True)

img = qr.make_image().convert('RGBA')
img.save("images/qrcode-eth.png")

qr.add_data('KYDFCQTDJCTLBIJWNT9UIXCN9SXHHSVCT9WDCIZWERJMCPDNZLWVIKOMYSGUVJLRE9CACQPOMZROSARBWYWPPXHHRX')
qr.make(fit=True)

img = qr.make_image().convert('RGBA')
img.save("images/qrcode-iota.png")


