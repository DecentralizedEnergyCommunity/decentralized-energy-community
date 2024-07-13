from __future__ import annotations
import sqlite3
import dataclasses
from typing import Optional

import models.meter


@dataclasses.dataclass
class EanMapping:
    ean: models.meter.EAN
    eanHash: str


@dataclasses.dataclass
class Repository:
    conn: sqlite3.Connection

    @staticmethod
    def create(dbfile: str = "ean-mappings.db") -> Repository:
        con = sqlite3.connect(dbfile)
        # initialize the table
        con.execute("CREATE TABLE IF NOT EXISTS ean_mapping(hash BLOB PRIMARY KEY, ean BLOB)")
        return

    def add_ean_hash(self, eanMapping: EanMapping) -> None:
        sql = """ INSERT INTO ean_mapping(hash,ean)
                  VALUES(?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, (eanMapping.hash, eanMapping.ean))
        self.conn.commit()
        return

    def get_ean(self, eanHash: str) -> Optional[models.meter.EAN]:
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM ean_mapping WHERE hash='?'", (eanHash,))
        element = cur.fetchone()
        if element is None:
            return None

        return models.meter.EAN(element)
