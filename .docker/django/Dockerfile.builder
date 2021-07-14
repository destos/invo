# application code is stored in /app
# TODO: describe build steps
ARG POETRY_HOME="/opt/poetry"
ARG SETUP_PATH="/opt/setup"
ARG VENV_PATH="${SETUP_PATH}/.venv/"

FROM python:3.9-slim-buster as python-base

ENV \
  # python
  PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

# builder-base is used to build dependencies
FROM python-base as builder-base

ARG POETRY_HOME
ARG SETUP_PATH
ARG VENV_PATH
ENV \
 # pip
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.4 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=true \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_CACHE_DIR="/var/cache/pypoetry" \
  POETRY_HOME=${POETRY_HOME}

# TODO: have poetry actually use the setup path virtual env
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        git \
        build-essential \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $SETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./

FROM python-base as production

ARG VENV_PATH
# ENV DJANGO_CONFIGURATION="Prod"
# ENV DJANGO_SECRET_KEY="<super secret>"

COPY --from=builder-base $VENV_PATH $VENV_PATH

WORKDIR /app
COPY ./invo ./invo
COPY ./manage.py manage.py

COPY ./.docker/django/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

RUN python -m venv $VENV_PATH
ENV PATH="${VENV_PATH}bin:$PATH"
RUN echo $PATH

ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "invo.asgi:application"]
