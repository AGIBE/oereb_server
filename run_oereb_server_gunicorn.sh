#!/bin/bash
python oereb_server/scripts/create_config.py
gunicorn -h