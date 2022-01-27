# -*- coding: utf-8 -*-
from mako.template import Template
import codecs
import os

def run_create_config():
    # Alle Umgebungsvariablen in einen Dictionary abfüllen
    env_vars = [
        'POSTGRES_DATABASE',
        'POSTGRES_HOST',
        'POSTGRES_PASSWORD',
        'POSTGRES_PORT',
        'POSTGRES_USER',
        'PRINT_SERVICE_HOST',
        'PRINT_SERVICE_PORT',
        'PRINT_SERVICE_PATH',
        'POSTGRES_LOGGER_DATABASE',
        'POSTGRES_LOGGER_SCHEMA',
        'POSTGRES_LOGGER_TABLE',
        'INI_LEVEL'
        ]
    vars = {}
    level = ''
    for env_var in env_vars:
        vars[env_var] = os.environ[env_var]

    # pyramid_oereb_standard.yml schreiben
    template = Template(filename='oereb_server.mako')
    rendered_config = template.render(**vars)

    with codecs.open('oereb_server.yml', "w", "utf-8") as config_file:
        config_file.write(rendered_config)

    # ini-File schreiben (production oder development)
    level = vars['INI_LEVEL']

    template2 = Template(filename=level + '.mako')
    rendered_config2 = template2.render(**vars)

    with codecs.open(level + '.ini', "w", "utf-8") as ini_file:
        ini_file.write(rendered_config2)

if __name__ == "__main__":
    run_create_config()