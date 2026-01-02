# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

# Install uv and sync dependencies from pyproject.toml/uv.lock
COPY ./app/pyproject.toml /app/pyproject.toml
COPY ./app/uv.lock /app/uv.lock
RUN pip install --no-cache-dir uv && uv sync --project /app

# Copy the application code last for better build caching
COPY ./app /app

EXPOSE 2000

ENV NAME=bartmannxyz

CMD ["uv", "run", "--project", "/app", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2000"]
