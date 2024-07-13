from __future__ import annotations

from fastapi import FastAPI

from app import repository

app = FastAPI()

repo = repository.Repository.create()

@app.post("/api/create-ean")
async def store_ean(mapping: repository.EanMapping) -> None:
    await repo.add_ean_hash(mapping)
    return None
