import os
import random
from multiprocessing import Pool
import time
import imgkit
import jinja2
import qrcode

config = imgkit.config(wkhtmltoimage='C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe')
templates_dir = "templates"
rendered_filename = "rendered.html"
script_path = os.path.dirname(os.path.abspath(__file__))
template_file_path = os.path.join(script_path, templates_dir)
render_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_file_path))


def qr_generate(msg):
    img = qrcode.make(msg)
    id = random.randint(100_000_000, 999_000_000)
    img_url = "qr_{}.jpg".format(id)
    img.save(img_url)
    return img_url



def render(msg):
    jpg_url = qr_generate(msg)
    render_vars = {
        "qr_code": jpg_url
    }
    output_text = render_environment.get_template('index.html').render(render_vars)

    with open(rendered_filename, "w") as result_file:
        result_file.write(output_text)


def gen(url):
    imgkit.from_file(rendered_filename, url, config=config,options={'width':420,'height':600})


def png_generate(msg):
    render(msg)
    pdf_url = "png_{}.png".format(random.randint(100_000_000, 999_000_000))
    gen(pdf_url)
    return pdf_url


def remove_img(img_name, path=None):
    if path:
        os.remove(path + '/' + img_name)
    else:
        os.remove(img_name)

if __name__ == '__main__':
    begin = time.time()
    img_url=png_generate(";ldcnsfaskelfhqpieuhwihqwiuhqipeufhqw[jkpfoq[ejc")
    remove_img(img_url)
    print(time.time()-begin)