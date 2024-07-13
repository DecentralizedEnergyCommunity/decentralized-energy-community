
lint-mypy:
    #/bin/bash
    cd backend && poetry run mypy .

watch-lint-mypy:
    #/bin/bash
    cd backend && watchexec -r -c -e .py -- just lint-mypy

lint-backend:
    @just lint-mypy


[private]
setup-backend:
    #!/bin/bash
    # install the dependencies of the backend
    mkdir backend/.venv
    cd backend && poetry install

[private]
setup-frontend:
    yarn install

# install all the tools and be ready to go!
setup:
    mise install -y
    @just setup-backend
    @just setup-frontend

test-frontend:
    yarn test

format-frontend:
    yarn format

format-backend:
    cd backend && poetry run black

watch-hardhead-build:
    #!/bin/bash
    cd packages/hardhat
    watchexec -r -e js,ts,json -c -- yarn compile

