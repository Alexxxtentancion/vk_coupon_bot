import hashlib
import os
import random
import string

import imgkit
import jinja2
import qrcode

config = imgkit.config(wkhtmltoimage='C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe')
templates_dir = "templates"
rendered_filename = "rendered.html"
script_path = os.path.dirname(os.path.abspath(__file__))
template_file_path = os.path.join(script_path, templates_dir)
render_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_file_path))


def randomString(stringLength=10):
    letters = string.ascii_letters
    s = ''.join(random.choice(letters) for i in range(stringLength)).encode()
    hash_obj = hashlib.sha3_256(s)
    hex_dig = hash_obj.hexdigest()
    return hex_dig


def render(jpg_url):
    render_vars = {
        "qr_code": jpg_url
    }
    output_text = render_environment.get_template('index.html').render(render_vars)
    return output_text


def gen(url, _string):
    imgkit.from_string(_string, url, config=config, options={'width': 420, 'height': 600})


def remove_img(img_name, path=None):
    if path:
        os.remove(path + '/' + img_name)
    else:
        os.remove(img_name)


def generate_png():
    s = randomString()
    img = qrcode.make(s)
    id = random.randint(100_000_000, 999_000_000)
    img_url = "qr_{}.jpg".format(id)
    img.save(img_url)
    out = render(img_url)
    png_url = "png_{}.png".format(random.randint(100_000_000, 999_000_000))
    gen(png_url, out)
    remove_img(img_url)
    return png_url
