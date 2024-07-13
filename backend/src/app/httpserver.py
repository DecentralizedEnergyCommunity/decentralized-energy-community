import asyncio
import json
from dataclasses import asdict
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import repository
from app import settlement
from models.community import Community
from models.meter import ean541448820060527996
from models.meterdata import MeterData
from models.timeperiod import TimePeriod, genesis

app = FastAPI()

repo = repository.Repository.create()


@app.post("/api/create-ean")
async def store_ean(mapping: repository.EanMapping) -> None:
    await repo.add_ean_hash(mapping)
    return None


@app.get("/calculate_balance")
async def calculate_balances(ean: str, start: datetime, end: datetime):
    time_period = TimePeriod(start, end)
    settlement_result = await settlement.settle(time_period, Community.create())
    results = {ean: {"amount_paid": result.amount_paid, "amount_earned": result.amount_earned} for result in
               settlement_result.results if ean in result.eans}
    json_response = json.dumps(results, default=str, sort_keys=True)
    return JSONResponse(content=json.loads(json_response), media_type="application/json")


@app.get("/load_meter_data")
async def load_meter_data(ean: str, start: datetime, end: datetime):
    # just serve a stub for now, EAN might not be known in frontend
    meter_data = MeterData.from_file(ean, TimePeriod(start, end))

    json_response = meter_data.df_kwh.to_json(force_ascii=True)
    return JSONResponse(content=json.loads(json_response), media_type="application/json")


if __name__ == "__main__":
    start = genesis
    end = datetime.now(timezone.utc)
    time_period = TimePeriod(start, end)
    settlement_result = asyncio.run(settlement.settle(time_period, Community.create()))
    results = [asdict(result) for result in settlement_result.results if ean541448820060527996 in result.eans]
    ean = ean541448820060527996
    json_response = json.dumps(results, default=str, sort_keys=True)


