FROM python:3.12-slim

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.1.2

RUN apt-get -y update; apt-get -y install curl build-essential pip
RUN pip install six
RUN pip install poetry

WORKDIR /src
COPY . ./

RUN poetry install