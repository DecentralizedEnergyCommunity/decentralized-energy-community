from __future__ import annotations

import asyncio
import sqlite3
import dataclasses
from typing import Optional

import models.meter


@dataclasses.dataclass
class EanMapping:
    ean: models.meter.EAN
    eanHash: str
    suplier: str


@dataclasses.dataclass
class Repository:
    conn: sqlite3.Connection
    lock: asyncio.Lock

    @staticmethod
    def create(dbfile: str = "ean-mappings.db") -> Repository:
        con = sqlite3.connect(dbfile, check_same_thread=False)
        # initialize the table
        con.execute("CREATE TABLE IF NOT EXISTS ean_mapping(hash TEXT PRIMARY KEY, ean TEXT, suplier TEXT)")
        return Repository(con, asyncio.Lock())

    async def add_ean_hash(self, eanMapping: EanMapping) -> None:
        sql = """ INSERT INTO ean_mapping(hash,ean, suplier)
                  VALUES(?,?,?) """

        async with self.lock:
            cur = self.conn.cursor()
            cur.execute(sql, (eanMapping.eanHash, eanMapping.ean, eanMapping.suplier))
            self.conn.commit()

        return

    async def get_ean(self, eanHash: str) -> Optional[models.meter.EAN]:
        async with self.lock:
            cur = self.conn.cursor()
            cur.execute(f"SELECT ean FROM ean_mapping WHERE hash = ?", (eanHash,))
            element = cur.fetchone()

        if element is None:
            return None

        return models.meter.EAN(element)
