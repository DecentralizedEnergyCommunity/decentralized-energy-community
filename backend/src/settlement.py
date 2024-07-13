import datetime

import pandas as pd

from models.community import Community
from models.meter import MeterType
from models.meterdata import MeterData
from models.participant import ParticipantResult
from models.settlement import SettlementResult
from models.timeperiod import TimePeriod


async def settle(period: int, community: Community) -> SettlementResult:
    results = []
    time_period = TimePeriod.from_id(period)
    for participant in community.participants:
        if participant.active:
            participant_results: list[ParticipantResult] = []
            meter_series: list[pd.Series] = []

            for meter in participant.meters:
                meterdata = MeterData.from_csv(meter.ean, time_period)

                if meter.is_consumer:
                    meter_series.append(-1 * meterdata.readings["volume"])
                elif meter.is_producer:
                    meter_series.append(meterdata.readings["volume"])

            net_usage = pd.concat(meter_series).sum()

    return SettlementResult(community.id, results)


def get_communities() -> list[Community]:
    # get the community from the smart contract.
    return []


def update_contract(result: SettlementResult) -> None:
    # todo write this back to the contract
    return None


async def run() -> None:
    communities = get_communities()

    for c in communities:
        result = await settle(c)
        update_contract(result)


if __name__ == '__main__':
    run()

