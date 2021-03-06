# -*- coding: utf-8 -*-
from pyramid.paster import get_app, setup_logging
from waitress import serve
from mako.template import Template
import paste
from paste.translogger import TransLogger
import codecs
import os

def main():
    # Alle Umgebungsvariablen in einen Dictionary abfüllen
    env_vars = ['POSTGRES_SERVICE_DATABASE', 'POSTGRES_SERVICE_HOST', 'POSTGRES_SERVICE_PASS', 'POSTGRES_SERVICE_PORT', 'POSTGRES_SERVICE_USER', 'PRINT_SERVICE_HOST', 'PRINT_SERVICE_PORT', 'POSTGRES_LOGGER_DATABASE', 'POSTGRES_LOGGER_HOST', 'POSTGRES_LOGGER_PASS', 'POSTGRES_LOGGER_PORT', 'POSTGRES_LOGGER_SCHEMA','POSTGRES_LOGGER_TABLE','POSTGRES_LOGGER_USER']
    vars = {}
    for env_var in env_vars:
        vars[env_var] = os.environ[env_var]

    # pyramid_oereb_standard.yml schreiben
    template = Template(filename='pyramid_oereb_standard.mako')
    rendered_config = template.render(**vars)

    with codecs.open('pyramid_oereb_standard.yml', "w", "utf-8") as config_file:
        config_file.write(rendered_config)

    level = "development"

    template2 = Template(filename=level + '.mako')
    rendered_config2 = template2.render(**vars)

    with codecs.open(level + '.ini', "w", "utf-8") as ini_file:
        ini_file.write(rendered_config2)

    ini_path = level + '.ini'
    setup_logging(ini_path)
    application = get_app(ini_path, 'main')
    
    serve(paste.translogger.TransLogger(application, setup_console_handler=False), listen='*:6543')

if __name__ == "__main__":
    main()