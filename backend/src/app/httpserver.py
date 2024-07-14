import asyncio
import json
from dataclasses import asdict
from datetime import datetime, timezone, timedelta

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import repository
from app import settlement
from models.community import Community
from models.meterdata import MeterData
from models.timeperiod import TimePeriod, genesis
from utils.config import Config

app = FastAPI()

repo = repository.Repository.create()


@app.post("/api/create-ean")
async def store_ean(mapping: repository.EanMapping) -> None:
    await repo.add_ean_hash(mapping)
    return None


@app.get("/calculate_balance")
async def calculate_balances(ean: str, start: datetime, end: datetime):
    try:
        time_period = TimePeriod(start, end)
        settlement_result = await settlement.settle(time_period, Community.create())
        results = {ean: {"amount_paid": result.amount_paid, "amount_earned": result.amount_earned} for result in
                   settlement_result.results if ean in result.eans}
        json_response = json.dumps(results, default=str, sort_keys=True)
        return JSONResponse(content=json.loads(json_response), media_type="application/json")
    except Exception:
        return JSONResponse(content={}, media_type="application/json", status_code=404)


@app.get("/load_meter_data")
async def load_meter_data(ean: str, start: datetime, end: datetime):
    # just serve a stub for now, EAN might not be known in frontend
    meter_data = MeterData.from_file(ean, TimePeriod(start, end))

    json_data = json.loads(meter_data.df_kwh.resample('1d').sum().to_json(force_ascii=True))

    consumption = []
    for key, value in json_data["consumption"].items():
        date = datetime.utcfromtimestamp(int(key) / 1000).strftime('%Y-%m-%d')
        consumption.append({"date": date, "value": value})

    production = []
    for key, value in json_data["production"].items():
        date = datetime.utcfromtimestamp(int(key) / 1000).strftime('%Y-%m-%d')
        production.append({"date": date, "value": value})

    output = {"consumption": consumption, "production": production}

    return JSONResponse(content=output, media_type="application/json")


if __name__ == "__main__":
    start = genesis
    end = datetime.now(timezone.utc) - timedelta(days=7)
    config = Config.load()
    ean1 = config["eans"]["ean1"]
    meter_data = MeterData.from_file(ean1, TimePeriod(start, end))

    a = json.loads(meter_data.df_kwh.resample('1d').sum().to_json(force_ascii=True))

    consumption = []
    for key, value in a["consumption"].items():
        date = datetime.utcfromtimestamp(int(key) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        consumption.append({"date": date, "value": value})

    production = []
    for key, value in a["production"].items():
        date = datetime.utcfromtimestamp(int(key) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        production.append({"date": date, "value": value})

    output = {"consumption": consumption, "production": production}
    json.dumps(output)

    time_period = TimePeriod(start, end)
    settlement_result = asyncio.run(settlement.settle(time_period, Community.create()))


