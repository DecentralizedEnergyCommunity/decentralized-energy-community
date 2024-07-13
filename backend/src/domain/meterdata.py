from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd

from backend.src.domain.meter import EAN
from backend.src.domain.participant import Participant


class Granularity:
    QUARTER_H = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 3


@dataclass(frozen=True)
class MeterData:
    ean: str
    readings: pd.DataFrame

    @property
    def start(self) -> datetime:
        return pd.to_datetime(self.readings.index[0])

    @property
    def end(self) -> datetime:
        return pd.to_datetime(self.readings.index[-1])

    @staticmethod
    def load_csv(filename: str) -> pd.DataFrame:
        folder = Path(Path(__file__).parent.parent.parent / "data")
        df = pd.read_csv(Path(folder / filename), delimiter=';')
        return pd.DataFrame.from_dict({
            "timestamp": pd.to_datetime(df["Van Datum"] + 'T' + df["Van Tijdstip"], format='%d-%m-%YT%H:%M:%S'),
            "volume": df["Volume"],
            "status": df["Validatiestatus"]
        }).set_index("timestamp")

    @staticmethod
    def from_csv(ean: EAN, filename: str) -> MeterData:
        df = MeterData.load_csv(filename)
        return MeterData(ean, df)


@dataclass
class SharingKey:
    producer: Participant
    participant: Participant
    key: float


if __name__ == '__main__':
    meterdata1 = MeterData.from_csv('541448820044186577', 'Verbruikshistoriek_elektriciteit_541448820044186577_20220110_20240708_kwartiertotalen.csv')
    meterdata2 = MeterData.from_csv('541448820060527996',
                                    'Verbruikshistoriek_elektriciteit_541448820044186577_20220110_20240708_kwartiertotalen.csv')



