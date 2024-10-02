FROM python:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root
COPY . /app

CMD ["python", "-m", "bot.main"]