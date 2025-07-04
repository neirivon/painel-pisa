import qrcode

# Configurar e gerar QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data("neirivon@ufu.br")
qr.make(fit=True)

# Salvar imagem
img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_code_meu_email_ufu.png")
