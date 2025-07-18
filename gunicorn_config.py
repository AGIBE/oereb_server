import os
from logging.config import fileConfig


def post_fork(server, worker):
    fileConfig(os.environ["INI_LEVEL"] + ".ini")


# Port
bind = ":6543"
# Anzahl Workers
workers = os.environ["GUNICORN_WORKERS"]
# Anzahl Threads
threads = os.environ["GUNICORN_THREADS"]
# Temp-Dir umleiten (s. https://pythonspeed.com/articles/gunicorn-in-docker/)
worker_tmp_dir = "/dev/shm"
# Header, die der Reverse Proxy setzt (via Bedag konfigurieren lassen)
# Wenn sie gesetzt sind, erkennt die Applikation, dass sie unter https
# läuft. Wenn sie eine URL zurückgibt (z.B. für Logos), wird dies korrekter-
# weise eine HTTPS-Url sein.
secure_scheme_headers = {"X-FORWARDED-PORT": "443", "X-FORWARDED-PROTO": "https"}
# IP-Adresse, von dem die obigen Header kommen. Die IP des Reverse Proxy ist mir
# nicht bekannt, daher lasse ich hier den Asterisk drin. Im RZ der Bedag ist das
# wohl nicht zu heikel.
forwarded_allow_ips = "*"
# Logging: damit wird auch ein klassisches Access-Log geschrieben
accesslog = "-"
errorlog = "-"
# Der ÖREB-Server hat irgendwo ein Memory Leak, d.h. der Memory-Verbrauch wird
# wird über die Zeit immer grösser. Das führt dazu, dass die Applikation ans
# des zugewiesenen RAMS kommt und terminiert wird. Sie wird dann zwar automatisch
# wieder gestartet, generiert aber eine Fehlermeldung im Monitoring und wohl auch
# bei den Anwendern. Deshalb wird mit max_requests bewirkt, dass jeder Worker nach
# max_requests kontrolliert neugestartet wird. Mit dem Jitter-Parameter wird bewirkt,
# dass nicht alle Worker gleichzeitig neustarten.
max_requests = os.environ["GUNICORN_MAX_REQUESTS"]
max_requests_jitter = 50
