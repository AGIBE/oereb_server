"""Modul für die Erstellung der verschiedenen Config-Files"""

import os
from mako.template import Template


def run_create_config():
    """Erstellt auf Basis von Umgebungsvariablen das Config-File des ÖREB-Servers (oereb_server.yml)
    sowie das ini-File für die Webapplikation (oereb_server.ini)
    """

    # Alle Umgebungsvariablen in einen Dictionary abfüllen
    expected_environment_variables = [
        "POSTGRES_DATABASE",
        "POSTGRES_HOST",
        "POSTGRES_PASSWORD",
        "POSTGRES_PORT",
        "POSTGRES_USER",
        "PRINT_SERVICE_HOST",
        "PRINT_SERVICE_PORT",
        "PRINT_SERVICE_PATH",
        "POSTGRES_LOGGER_DATABASE",
        "POSTGRES_LOGGER_SCHEMA",
        "POSTGRES_LOGGER_TABLE",
        "INI_LEVEL",
        "LOG_LEVEL",
    ]
    found_environment_variables = {}
    level = ""
    for env_var in expected_environment_variables:
        found_environment_variables[env_var] = os.environ[env_var]

    # pyramid_oereb_standard.yml schreiben
    yml_template = Template(filename="oereb_server.mako")
    rendered_yml_config = yml_template.render(**found_environment_variables)

    with open("oereb_server.yml", "w", encoding="utf-8") as config_file:
        config_file.write(rendered_yml_config)

    # ini-File schreiben (production oder development)
    level = found_environment_variables["INI_LEVEL"]

    ini_template = Template(filename=f"{level}.mako")
    rendered_ini_config = ini_template.render(**found_environment_variables)

    with open("oereb_server.ini", "w", encoding="utf-8") as ini_file:
        ini_file.write(rendered_ini_config)


if __name__ == "__main__":
    run_create_config()
