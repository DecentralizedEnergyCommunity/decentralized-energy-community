
lint-mypy:
    #/bin/bash
    cd backend
    poetry run mypy

lint-backend:
    @just lint-mypy


[private]
setup-backend:
    #!/bin/bash
    # install the dependencies of the backend
    touch backend/.venv
    cd backend && poetry install

[private]
setup-froned:
    yarn install

# install all the tools and be ready to go!
setup:
    mise install -y
    @just setup-backend
    @just setup-frontend
    pre-commit install


test-frontend:
    yarn test

format-frontend:
    yarn format

format-backend:
    cd backend && poetry run black
