#!/bin/bash
python oereb_server/scripts/create_config.py
gunicorn --paste "$INI_LEVEL".ini#main --config gunicorn_config.py