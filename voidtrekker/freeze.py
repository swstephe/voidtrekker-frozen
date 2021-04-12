# -*- coding: utf8 -*-
from flask_frozen import Freezer
from voidtrekker.app import app

freezer = Freezer(app)


def main():
    freezer.freeze()


if __name__ == '__main__':
    main()
