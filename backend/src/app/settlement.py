import datetime

import pandas as pd

from models.community import Community
from models.meter import MeterType
from models.meterdata import MeterData
from models.settlement import SettlementResult
from models.timeperiod import TimePeriod


async def settle(period: SettlementId, community: Community) -> SettlementResult:
    time_period = TimePeriod.from_id(period)

    pool_consumed_energy_series: list[pd.Series] = []
    pool_produced_energy_series: list[pd.Series] = []

    for participant in community.participants:
        # filter non active users
        if not participant.active:
            continue

        for meter in participant.meters:
            meterdata= MeterData.from_csv(meter.ean, time_period)
            pool_consumed_energy_series.append(meterdata.production)
            pool_produced_energy_series.append(meterdata.consumption)

    pool_consumed_energy = pd.concat(pool_consumed_energy_series, axis=1)
    # the energy consumed by the pool
    total_consumed_energy = pool_consumed_energy.sum(axis=1)
    # every column is a participant
    consumer_participation = pool_consumed_energy / total_consumed_energy

    # the energy produced by the pool
    pool_produced_energy = pd.concat(pool_produced_energy_series, axis=1)
    total_produced_energy = pool_produced_energy.sum(axis=1)
    # every column is a participant
    producer_participation = pool_produced_energy / total_produced_energy

    # the traded energy is the minimum of the two totals
    traded_energy = pd.concat([total_produced_energy, total_consumed_energy], axis=1).min(axis=1)

    # the spot price of each quarter
    quarterly_price = get_quarterly_price()
    traded_euros = quarterly_price * traded_energy

    settled_euros_consumer = traded_euros * producer_participation
    settled_euros_producer = traded_euros * consumer_participation

    # group by participant
    results: list[ParticipantSettlement] = []
    for participant in community.participants:
        # filter non active users
        if not participant.active:
            continue
        # sum the meters
        eans = [meter.ean for meter in participant.meters]

        # todo make sure we use ints
        amount_paid = settled_euros_consumer[eans].sum(axis=1).sum()
        amount_earned = settled_euros_producer[eans].sum(axis=1).sum()
        results.append(
            ParticipantSettlement(participantId=participant.id, amount_paid=amount_paid, amount_earned=amount_earned)
        )

    return SettlementResult(period, community.id, results)


def get_quarterly_price() -> pd.Series:
    # this returns the quarterly price
    pass


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

