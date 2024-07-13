from __future__ import annotations

import io
import urllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd

import fluvius

from models.meter import EAN
from models.participant import Participant


class Granularity:
    QUARTER_H = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 3


@dataclass(frozen=True)
class MeterData:
    ean: EAN
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

    @staticmethod
    def fetch(ean: EAN, start: datetime, end: datetime, granularity: Granularity, requests=None) -> MeterData:
        token = fluvius.api.refresh_token()

        headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Authorization": token,
        }

        start_str = urllib.parse.quote(start.strftime("%Y-%m-%dT%H:%M:%S%z"))
        end_str = urllib.parse.quote(end.strftime("%Y-%m-%dT%H:%M:%S%z"))
        endpoint = f"https://mijn.fluvius.be/verbruik/api/consumption-histories/{ean}/report?historyFrom={start_str}&historyUntil={end_str}&granularity={granularity}&asServiceProvider=false"
        response = requests.get(endpoint, headers=headers)
        print(response.text)

        df = (MeterData.load_csv(io.StringIO(response.text), index_col=0))
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




