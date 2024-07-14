FROM python:3.11-slim

COPY . /app

WORKDIR /app/backend

RUN pip install poetry
RUN ["backend/.venv/bin/fastapi", "dev", "backend/src/app/httpserver.py"]
