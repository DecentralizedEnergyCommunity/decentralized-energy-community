FROM python:3.11-slim

COPY . /app

WORKDIR /app/backend

RUN pip install poetry --no-root
RUN ["fastapi", "dev", "backend/src/app/httpserver.py"]
