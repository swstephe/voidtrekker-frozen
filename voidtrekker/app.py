# -*- coding: utf8 -*-
from flask import Flask

from voidtrekker import content
app = Flask(__name__)


@app.route('/')
def home_html():
    return content.pug('index.pug', site=content.site_data())


@app.route('/favicon.ico')
def favicon_ico():
    return content.favicon('ico')


@app.route('/favicon/favicon-<int:size>.png')
def favicon_png(size):
    return content.favicon(size)


@app.route('/<path:path>.jpg')
def jpg_image(path):
    return content.image(path + '.jpg', content_type='image/jpg')


@app.route('/<path:path>.png')
def png_image(path):
    return content.image(path + '.png', content_type='image/png')


@app.route('/<path:path>.html')
def html_file(path):
    return content.pug(path + '.pug', site=content.site_data())


@app.route('/<path:path>.js')
def script_js(path):
    print('path', path)
    return content.coffee(path)


@app.route('/<path:path>.css')
def style_css(path):
    return content.stylus(path)


@app.route('/typography.css')
def typography_css():
    return content.typography()


if __name__ == '__main__':
    app.run(debug=True, extra_files=content.SITE_DIR)
