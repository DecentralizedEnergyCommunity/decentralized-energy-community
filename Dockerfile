FROM python:3.11-slim

COPY . /app
WORKDIR /app

RUN apt -y update && apt -y install curl
RUN curl https://mise.run | sh
RUN /root/.local/bin/mise install -y
ENV PATH="$PATH:/root/.local/share/mise/shims"
RUN just setup

RUN ["fastapi", "dev", "backend/src/app/httpserver.py"]
