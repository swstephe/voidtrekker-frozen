# -*- coding: utf8 -*-
from collections import defaultdict
import datetime
import io
import json
from pathlib import Path
import re
import subprocess as sub
from typing import Union

from flask import Response
import markdown
from PIL import Image
import yaml

from voidtrekker.config import ROOT_DIR, SITE_DIR

NODE_DIR = ROOT_DIR / 'voidtrekker' / 'src'
NoneType = type(None)
md = markdown.Markdown()

re_more = re.compile(r'<~-\s*more\s*-->', re.IGNORECASE | re.DOTALL)
re_para = re.compile(r'<p>(.*?)</p>', re.IGNORECASE | re.DOTALL)
re_clean = re.compile(r'(\S|<[^>]*)+$', re.DOTALL)


def json_default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def dump_json(data):
    return json.dumps(
        data,
        sort_keys=True,
        indent=2,
        default=json_default
    )


def excerpt(html, max_chars=250):
    m = re_para.search(html)
    if m:
        return re_clean.sub('', m.group(1)[:max_chars])


def static(path):
    with open(SITE_DIR / path) as f:
        return f.read()


def load_markdown(path: Union[str, Path]):
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        return
    with path.open('r') as f:
        return md.convert(f.read())


def load_yaml(path: Union[str, Path]) -> Union[list, dict, NoneType]:
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        return {}
    with path.open('r') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def node(script, *args):
    """
    Given a script, run it through NodeJS

    :param script: the path to the script (in voidtrekker/src)
    :return: the output from running the script
    """
    return (
        sub
        .check_output(['node', script, *args], cwd=NODE_DIR)
        .decode('utf8')
    )


def coffee(path):
    return Response(
        node('coffee2js.js', str(SITE_DIR / path) + '.coffee'),
        content_type='application/javascript'
    )


def favicon(opt):
    favicon_path = SITE_DIR / 'favicon'
    src = favicon_path / 'favicon.png'
    img = Image.open(src)
    with io.BytesIO() as output:
        if opt == 'ico':
            img.save(
                output,
                format='ICO',
                sizes=[(x, x) for x in (16, 32, 48)]
            )
            content_type = 'image/ico'
        else:
            img.resize((opt, opt)).save(output, format='PNG')
            content_type = 'image/png'
        return Response(output.getvalue(), content_type=content_type)


def image(path, content_type):
    with (SITE_DIR / path).open('rb') as f:
        return Response(f.read(), content_type=content_type)


def pug(pug_path, site=None):
    pug_file = SITE_DIR / pug_path
    data = {'site': site}
    data_file = pug_file.with_suffix('.yaml')
    data.update(load_yaml(data_file))
    return Response(
        node('pug2html.js', str(pug_file), dump_json(data)),
        content_type='text/html'
    )


def site_data():
    data = {}
    site_data_file = SITE_DIR / 'site.yaml'
    data.update(load_yaml(site_data_file))
    blogs = defaultdict(dict)
    blog_path = SITE_DIR / 'blog'
    for path in blog_path.iterdir():
        if not path.is_file():
            continue
        if path.suffix == '.md':
            blogs[path.stem]['excerpt'] = excerpt(load_markdown(path))
        elif path.suffix == '.yaml':
            blogs[path.stem].update(load_yaml(path))
            blogs[path.stem]['filename'] = str(path.stem)
    blogs = [{'name': k} | v for k, v in blogs.items()]
    data['blogs'] = sorted(blogs, key=lambda v: v['date'], reverse=True)
    data['categories'] = defaultdict(list)
    data['tags'] = defaultdict(list)
    for blog in data['blogs']:
        for category in blog.get('categories', []):
            data['categories'][category].append(blog['filename'])
        for tag in blog.get('tags', []):
            data['tags'][tag].append(blog['filename'])
    return data


def stylus(path):
    stylus_file = str(SITE_DIR / path) + '.styl'
    return Response(
        node('stylus2css.js', stylus_file),
        content_type='text/css'
    )


def typography():
    typography_file = SITE_DIR / 'typography.yaml'
    config = {}
    config.update(load_yaml(typography_file))
    return Response(
        node('typography.js', json.dumps(config)),
        content_type='text/css'
    )


if __name__ == '__main__':
    # print(coffee('script.coffee'))
    # print(pug('index.pug'))
    # print(stylus('style.styl'))
    _data = site_data()
    print(_data['categories'])
    print(_data['tags'])