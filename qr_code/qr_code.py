import qrcode

# OTP URL
otp_url = "otpauth://totp/Amazon%20Web%20Services:kayama-pc%40613951263398?secret=GXVNEKS2MZO47FBZ3CSSWMYKBNUMMYABT6MT4JER3O324ITMKZZNAS5KYEY325YM&issuer=Amazon%20Web%20Services"

# QRコードの生成
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(otp_url)
qr.make(fit=True)

# QRコードの画像を保存
img = qr.make_image(fill='black', back_color='white')
img.save("aws_qr_code.png")
