FROM python:alpine

ENV TERM xterm

RUN apk update && apk add make gcc python3-dev musl-dev postgresql-dev tzdata libressl-dev libffi-dev

WORKDIR /opt/coin/
RUN python -m pip install -U pip && pip install poetry
COPY pyproject.toml /opt/coin/pyproject.toml
RUN poetry install

COPY src /opt/coin
