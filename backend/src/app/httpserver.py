import json
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import repository
from app import settlement
from models.community import Community
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
    settlement_result = await settlement.settle(time_period, Community.stub())
    dumps = json.dumps(settlement_result, default=str, sort_keys=True)
    return JSONResponse(content=dumps, media_type="application/json")


@app.get("/load_meter_data")
async def load_meter_data(ean: str, start: datetime, end: datetime):
    # just serve a stub for now, EAN might not be known in frontend
    meter_data = MeterData.from_file(ean, TimePeriod(start, end))

    json_response = meter_data.df_kwh.to_json(force_ascii=True)
    return JSONResponse(content=json.loads(json_response), media_type="application/json")


if __name__ == "__main__":
    start = genesis
    end = datetime.now(timezone.utc)
    meter_data: MeterData = MeterData.from_file(ean, TimePeriod(start, end))
    ja =(meter_data.df_kwh / 1000).to_json()
    df_json = json.loads(ja)


