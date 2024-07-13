from __future__ import annotations

from fastapi import FastAPI

from app import repository

app = FastAPI()

repo = repository.Repository.create()

@app.post("api/create-ean")
def store_ean(mapping: repository.EanMapping) -> None:
    repo.add_ean_hash(mapping)
    return None
