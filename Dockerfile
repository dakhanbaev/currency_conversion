FROM python:3.11.7 as builder

RUN pip install poetry==1.4.2

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg


ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR .

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install

FROM python:3.11.7 as runtime

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src src
COPY tests tests
COPY alembic alembic
COPY alembic.ini .
COPY entrypoint.sh .
COPY log_conf.yaml .

RUN chmod +x entrypoint.sh

EXPOSE 8000
