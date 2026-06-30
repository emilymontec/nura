FROM python:3.11-slim

WORKDIR /shared/nura-shared

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

COPY . .
