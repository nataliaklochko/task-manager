FROM python:3.13-slim

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root

COPY /src ./src

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.app.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
