# -*- coding: utf-8 -*-
from pyramid.paster import get_app, setup_logging
from waitress import serve
from oereb_server.scripts import create_config
import os


def main():
    create_config.run_create_config()

    level = os.environ["INI_LEVEL"]

    ini_path = level + ".ini"
    setup_logging(ini_path)
    application = get_app(ini_path, "main")

    serve(application, listen="*:6543", url_scheme="https", threads=16)


if __name__ == "__main__":
    main()
