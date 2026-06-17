# -*- coding: utf-8 -*-
from pyramid.paster import get_app, setup_logging
from waitress import serve
from oereb_server.scripts import create_config

def main():
    create_config.run_create_config()

    ini_path = "oereb_server.ini"
    setup_logging(ini_path)
    application = get_app(ini_path, "main")

    serve(application, listen="*:6543", url_scheme="http", threads=4)


if __name__ == "__main__":
    main()
