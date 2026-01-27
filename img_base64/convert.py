import base64

def image_file_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())

    print(data.decode('utf-8'))

if __name__ == '__main__':
    image_file_to_base64("物理攻撃UP.jpg")
