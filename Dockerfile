FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.8.3

WORKDIR /app

RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root

COPY . .

ENTRYPOINT ["python", "dpulse.py"]
