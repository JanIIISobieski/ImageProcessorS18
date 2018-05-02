import base64


def encode_image_string(filename):
    with open(filename, "rb") as image_file:
        image_string = base64.b64encode(image_file.read())
        return image_string


def save_image_string(base64image, filename):
    with open(filename, "wb") as image_out:
        image_out.write(base64.b64decode(base64image))
