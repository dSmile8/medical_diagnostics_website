FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false  \
    && poetry install --no-root

COPY . .
