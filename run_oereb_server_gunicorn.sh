#!/bin/bash
python src/oereb_server/scripts/create_config.py
gunicorn --paste oereb_server.ini#main --config gunicorn_config.py