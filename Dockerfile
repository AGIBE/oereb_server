FROM python:3.9.18-slim-bookworm

RUN mkdir /usr/src/oereb_server

WORKDIR /usr/src/oereb_server

RUN groupadd oereb && useradd -g oereb oerebrunner

COPY --chown=oerebrunner:oereb *.mako *.py *.sh *.txt ./

RUN chmod +x run_oereb_server_gunicorn.sh

COPY --chown=oerebrunner:oereb ./src/oereb_server/. ./src/oereb_server/.

RUN apt-get update && apt-get -y upgrade && \
	DEV_PACKAGES="build-essential libgeos-dev libpq-dev" && \
	DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends \
	libgeos-c1v5 gosu tini libpq5 ${DEV_PACKAGES} && \
	pip install --disable-pip-version-check --no-cache-dir --requirement requirements.txt && \
	pip install -e . && \
	apt remove --purge --autoremove --yes ${DEV_PACKAGES} binutils && \
	apt-get clean && \
	rm --force --recursive /var/lib/apt/lists/* && \
	chown -R oerebrunner:oereb /usr/src/oereb_server

ENTRYPOINT [ "gosu", "oerebrunner", "tini", "--" ]

CMD ["/usr/src/oereb_server/run_oereb_server_gunicorn.sh"]
# CMD ["python3", "./run_oereb_server_waitress_local.py"]

