import json
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import settlement
from models.community import Community
from models.meterdata import MeterData
from models.timeperiod import TimePeriod, genesis

app = FastAPI()


@app.get("/calculate_balance")
async def calculate_balances(ean: str, start: datetime, end: datetime):
    time_period = TimePeriod(start, end)
    result = settlement.settle(time_period, Community.stub())


@app.get("/load_meter_data")
async def load_meter_data(ean: str, start: datetime, end: datetime):
    # just serve a stub for now, EAN might not be known in frontend
    meter_data = MeterData.from_file(ean, TimePeriod(start, end))

    json_content = meter_data.df_kwh.to_json(force_ascii=True)
    df_json = json.loads(json_content)
    return JSONResponse(content=df_json, media_type="application/json")


if __name__ == "__main__":
    start = genesis
    end = datetime.now(timezone.utc)
    meter_data: MeterData = MeterData.from_file(ean, TimePeriod(start, end))
    ja =(meter_data.df_kwh / 1000).to_json()
    df_json = json.loads(ja)


