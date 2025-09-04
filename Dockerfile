FROM python:3.12.10-slim-bookworm as builder

COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /bin/uv

WORKDIR /usr/src/oereb_server

ENV UV_COMPILE_BYTECODE=1

RUN apt-get update && apt-get -y upgrade && \
	DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends \
	libgeos-c1v5 libpq5 build-essential libgeos-dev libpq-dev

ADD . /usr/src/oereb_server

RUN uv sync --frozen --no-dev --no-cache

FROM python:3.12.10-slim-bookworm

RUN apt-get update && apt-get -y upgrade && \
	DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends \
	libgeos-c1v5 libpq5 gosu tini && \
    apt-get clean && \
    rm --force --recursive /var/lib/apt/lists/*

RUN groupadd oereb && useradd -g oereb oerebrunner

WORKDIR /usr/src/oereb_server

COPY --from=builder --chown=oerebrunner:oereb /usr/src/oereb_server /usr/src/oereb_server

RUN chmod +x run_oereb_server_gunicorn.sh

ENV PATH="/usr/src/oereb_server/.venv/bin:$PATH"

ENTRYPOINT [ "gosu", "oerebrunner", "tini", "--" ]

CMD ["/usr/src/oereb_server/run_oereb_server_gunicorn.sh"]