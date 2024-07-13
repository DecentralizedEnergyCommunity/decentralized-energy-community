from __future__ import annotations

import io
import urllib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests
import pandas as pd

import constants
import fluvius
from constants import BE_TZ

from models.meter import EAN
from models.participant import Participant
from models.timeperiod import TimePeriod, genesis


class Granularity:
    QUARTER_H = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 3


@dataclass(frozen=True)
class MeterData:
    ean: EAN
    consumption: pd.Series
    production: pd.Series

    @property
    def start(self) -> datetime:
        return pd.to_datetime(self.readings.index[0])

    @property
    def end(self) -> datetime:
        return pd.to_datetime(self.readings.index[-1])

    @staticmethod
    def load_csv(filename: str, time_period: TimePeriod) -> (pd.DataFrame, pd.DataFrame):
        folder = Path(Path(__file__).parent.parent.parent / "data")
        df = pd.read_csv(Path(folder / filename), delimiter=';')
        index = pd.DatetimeIndex(
            pd.to_datetime(df["Van Datum"] + 'T' + df["Van Tijdstip"], format='%d-%m-%YT%H:%M:%S')).tz_localize(timezone.utc)
        # FIXME localize here
        volume = (df["Volume"].str.replace(",", ".").astype(float) * 1000).fillna(0).astype(int)
        time_slice = pd.DataFrame.from_dict({"timestamp": index,
             ean: volume,
             "type": df["Register"]
         }).set_index("timestamp").loc[time_period.start:time_period.end]
        production = time_slice.loc[time_slice["type"].str.startswith("Injectie")].drop(columns=["type"])[ean]
        consumption = time_slice.loc[time_slice["type"].str.startswith("Afname")].drop(columns=["type"])[ean]
        return consumption, production

    @staticmethod
    def from_csv(ean: EAN, time_period: TimePeriod) -> MeterData:
        if ean in files:
            consumption, production = MeterData.load_csv(files[ean], time_period)
        else:
            raise Exception(f"No data for {ean}!")
        return MeterData(ean, consumption, production)

    @staticmethod
    def from_api(ean: EAN, time_period: TimePeriod, granularity: Granularity) -> MeterData:
        token = fluvius.api.refresh_token()

        headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Authorization": token,
        }

        start_str = urllib.parse.quote(time_period.start.strftime("%Y-%m-%dT%H:%M:%S%z"))
        end_str = urllib.parse.quote(time_period.end.strftime("%Y-%m-%dT%H:%M:%S%z"))
        endpoint = f"https://mijn.fluvius.be/verbruik/api/consumption-histories/{ean}/report?historyFrom={start_str}&historyUntil={end_str}&granularity={granularity}&asServiceProvider=false"
        response = requests.get(endpoint, headers=headers)
        print(response.text)

        consumption, production = (MeterData.load_csv(io.StringIO(response.text), index_col=0))
        return MeterData(ean, consumption, production)


files = {
    '541448820044186577': 'Verbruikshistoriek_elektriciteit_541448820044186577_20220110_20240708_kwartiertotalen.csv',
    '541448820060527996': 'Verbruikshistoriek_elektriciteit_541448820044186577_20220110_20240708_kwartiertotalen.csv',
    '541448820072026166': 'Verbruikshistoriek_elektriciteit_541448820072026166_20240707_20240709_kwartiertotalen.csv',
    '541448860010420847': 'Verbruikshistoriek_elektriciteit_541448860010420847_20240708_20240709_kwartiertotalen.csv',
    '541449500000446547': 'Verbruikshistoriek_elektriciteit_541449500000446547_20240624_20240709_dagtotalen.csv'
}


@dataclass(frozen=True)
class SharingKey:
    producer: Participant
    participant: Participant
    key: float


if __name__ == '__main__':
    for ean in files.keys():
        MeterData.from_csv(ean, TimePeriod(genesis, genesis + timedelta(weeks=1)))




