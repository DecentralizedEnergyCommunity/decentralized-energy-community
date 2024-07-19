from __future__ import annotations

import io
import typing
import urllib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests
import pandas as pd

import fluvius

from models.meter import EAN
from models.timeperiod import TimePeriod, genesis
from utils.config import Config


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
        return pd.to_datetime(self.consumption.index[0])

    @property
    def end(self) -> datetime:
        return pd.to_datetime(self.consumption.index[-1])

    @property
    def df_kwh(self) -> pd.DataFrame:
        return pd.concat([self.consumption.rename("consumption"), self.production.rename("production")], axis=1) / 1000

    @staticmethod
    def _load_csv(ean: EAN, filename: str, time_period: TimePeriod) -> typing.Tuple[pd.Series, pd.Series]:
        folder = Config.data_dir()
        df = pd.read_csv(Path(folder / filename), delimiter=",", dtype={"Van Datum": str, "Van Datum": str, "Tot Datum": str, "Tot Tijdstip": str, "Volume": str, "Register": str})
        index = pd.DatetimeIndex(
            pd.to_datetime(df["Van Datum"] + "T" + df["Van Tijdstip"], format="%d-%m-%YT%H:%M:%S")
        ).tz_localize(timezone.utc)
        # FIXME localize here
        volume = (df["Volume"].astype(float) * 1000).fillna(0).astype(int)

        df = pd.DataFrame.from_dict({"timestamp": index, ean: volume, "type": df["Register"]}).set_index("timestamp")

        time_slice = df.loc[time_period.start : time_period.end_exclusive]

        production = time_slice.loc[time_slice["type"].str.startswith("Injectie")].drop(columns=["type"])[ean]
        consumption = time_slice.loc[time_slice["type"].str.startswith("Afname")].drop(columns=["type"])[ean]
        return consumption, production

    @staticmethod
    def from_file(ean: EAN, time_period: TimePeriod) -> MeterData:
        if ean in files:
            consumption, production = MeterData._load_csv(ean, files[ean], time_period)
        else:
            raise Exception(f"No data for {ean}!")
        return MeterData(ean, consumption, production)

    @staticmethod
    def from_api(ean: EAN, time_period: TimePeriod, granularity: Granularity) -> MeterData:
        """
        Using a static token works but it needs to be refreshed as it expires after a while.
        So we load smartmeter data into csv and read it from there for now
        """
        #token = fluvius.api.refresh_token()

        headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Authorization": Config.load()['fluvius']['token'],
        }

        start_str = urllib.parse.quote(time_period.start.strftime("%Y-%m-%dT%H:%M:%S%z"))
        end_str = urllib.parse.quote(time_period.end.strftime("%Y-%m-%dT%H:%M:%S%z"))
        endpoint = f"https://mijn.fluvius.be/verbruik/api/consumption-histories/{ean}/report?historyFrom={start_str}&historyUntil={end_str}&granularity={granularity}&asServiceProvider=false"
        response = requests.get(endpoint, headers=headers)

        with open('response_data.csv', 'w') as file:
            file.write(response.text)
            file.close()

        consumption, production = MeterData._load_csv(ean, 'response_data.csv', time_period)
        return MeterData(ean, consumption, production)


config = Config.load()["eans"]

files = {
    config["ean1"]: "Verbruikshistoriek_elektriciteit_20220110_20240708_kwartiertotalen.csv",
    config["ean2"]: "Verbruikshistoriek_elektriciteit_20240517_20240712_kwartiertotalen.csv",
    config["ean3"]: "Verbruikshistoriek_elektriciteit_20240707_20240709_kwartiertotalen.csv",
    config["ean4"]: 'Verbruikshistoriek_elektriciteit_20240709_20240713_kwartiertotalen.csv'
}

if __name__ == "__main__":
    for ean in files.keys():
        a = MeterData.from_file(ean, TimePeriod(genesis, genesis + timedelta(weeks=1)))
        print(a)
