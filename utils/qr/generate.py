import qrcode

def create_qr_using_qrcode(data, filename):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        border=1,
    )
    
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)


if __name__ == "__main__":
    data = "Hello World!"
    filename = "qr_code.png"
    create_qr_using_qrcode(data, filename)

