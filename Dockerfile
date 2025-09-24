FROM python:3.12-slim
RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml ./

RUN uv pip install . --system

COPY src ./src
COPY .env /app/src/.env

ENV PYTHONPATH=/app/src


EXPOSE 8080
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]

