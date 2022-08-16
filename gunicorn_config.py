import os
from logging.config import fileConfig

def post_fork(server, worker):
    fileConfig(os.environ['INI_LEVEL'] + ".ini")

# Port
bind = ":6543"
# Anzahl Workers
workers = os.environ['GUNICORN_WORKERS']
# Anzahl Threads
threads = os.environ['GUNICORN_THREADS']
# Temp-Dir umleiten (s. https://pythonspeed.com/articles/gunicorn-in-docker/)
worker_tmp_dir = "/dev/shm"
# Header, die der Reverse Proxy setzt (via Bedag konfigurieren lassen)
# Wenn sie gesetzt sind, erkennt die Applikation, dass sie unter https
# läuft. Wenn sie eine URL zurückgibt (z.B. für Logos), wird dies korrekter-
# weise eine HTTPS-Url sein.
secure_scheme_headers = {'X-FORWARDED-PORT': '443', 'X-FORWARDED-PROTO': 'https'}
# IP-Adresse, von dem die obigen Header kommen. Die IP des Reverse Proxy ist mir
# nicht bekannt, daher lasse ich hier den Asterisk drin. Im RZ der Bedag ist das
# wohl nicht zu heikel.
forwarded_allow_ips = "*"
# Logging: damit wird auch ein klassisches Access-Log geschrieben
accesslog = "-"
errorlog = "-"