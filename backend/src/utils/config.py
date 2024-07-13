from __future__ import annotations

import os
import tomllib
from os import getcwd
from pathlib import Path


class Config:

    @staticmethod
    def data_dir():
        return Path(Path(__file__).parent.parent.parent / "data")

    @staticmethod
    def load(file: str = os.environ.get("CONFIG_FILE", getcwd() + "/application.toml")) -> Config:
        with open(file, "rb") as f:
            return tomllib.load(f)


if __name__ == "__main__":
    config = Config.load()
    print(config['fluvius'])
