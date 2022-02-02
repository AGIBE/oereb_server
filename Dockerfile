FROM python:3.7.12-slim-bullseye

RUN mkdir /usr/src/oereb_server
WORKDIR /usr/src/oereb_server
RUN groupadd oereb && useradd -g oereb oerebrunner

COPY --chown=oerebrunner:oereb *.mako *.py *.sh *.txt ./
RUN chmod +x run_oereb_server_gunicorn.sh
COPY --chown=oerebrunner:oereb ./oereb_server/. ./oereb_server/.

RUN apt update && \
    DEV_PACKAGES="build-essential libgeos-dev" && \
    DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends \
        libgeos-c1v5 gosu tini ${DEV_PACKAGES} && \
    pip install --disable-pip-version-check --no-cache-dir --requirement requirements.txt && \
    pip install -e . && \
    apt remove --purge --autoremove --yes ${DEV_PACKAGES} binutils && \
    apt-get clean && \
    rm --force --recursive /var/lib/apt/lists/*

RUN chown -R oerebrunner:oereb /usr/src/oereb_server

# WORKDIR /usr/src
# RUN git clone https://github.com/openoereb/pyramid_oereb.git
# WORKDIR /usr/src/pyramid_oereb
# RUN python setup.py develop
# RUN chown -R oerebrunner:oereb /usr/src/pyramid_oereb

ENTRYPOINT [ "gosu", "oerebrunner", "tini", "--" ]
CMD ["/usr/src/oereb_server/run_oereb_server_gunicorn.sh"]