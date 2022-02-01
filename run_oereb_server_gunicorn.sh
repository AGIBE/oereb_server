#!/bin/bash
python oereb_server/scripts/create_config.py
gunicorn --paste production.ini#main --config gunicorn_config.py