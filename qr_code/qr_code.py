import qrcode

# OTP URL
otp_url = "otpauth://totp/GitHub:mystblue?secret=WMQ6ABEKXEY3CKEL&issuer=GitHub"

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
img.save("otp_qr_code.png")
