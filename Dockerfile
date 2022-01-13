FROM python:3.7.12-slim-bullseye

WORKDIR /usr/src
RUN mkdir oereb_server
WORKDIR /usr/src/oereb_server

COPY ./dev-requirements.txt .
COPY development.mako .
COPY run_oereb_server.py .
COPY production.mako .
COPY oereb_server.mako .
COPY requirements.txt .
COPY setup.py .
COPY ./oereb_server/. ./oereb_server/.
COPY ./tests/. ./tests/.

RUN apt update && \
    DEV_PACKAGES="build-essential libgeos-dev" && \
    DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends \
        libgeos-c1v5 gosu tini git ${DEV_PACKAGES} && \
    pip install --disable-pip-version-check --no-cache-dir --requirement requirements.txt && \
    apt remove --purge --autoremove --yes ${DEV_PACKAGES} binutils && \
    apt-get clean && \
    rm --force --recursive /var/lib/apt/lists/*

WORKDIR /usr/src
RUN git clone https://github.com/openoereb/pyramid_oereb.git
WORKDIR /usr/src/pyramid_oereb
RUN git checkout v3
RUN python setup.py develop

WORKDIR /usr/src/oereb_server
RUN python setup.py develop

RUN groupadd oereb && useradd -g oereb oerebrunner

RUN chown -R oerebrunner:oereb /usr/src/oereb_server
RUN chown -R oerebrunner:oereb /usr/src/pyramid_oereb

ENTRYPOINT [ "gosu", "oerebrunner", "tini", "--" ]

CMD ["python", "/usr/src/oereb_server/run_oereb_server.py"]