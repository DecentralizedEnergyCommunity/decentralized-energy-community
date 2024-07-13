from datetime import date

import pandas as pd

from models.community import Community
from models.meterdata import MeterData
from models.settlement import SettlementResult, TimePeriodId, ParticipantSettlement
from models.timeperiod import TimePeriod


async def settle(period: TimePeriodId, community: Community) -> SettlementResult:
    time_period = TimePeriod.from_id(period)

    pool_consumed_energy_series: list[pd.Series] = []
    pool_produced_energy_series: list[pd.Series] = []

    for participant in community.participants:
        # filter non active users
        if not participant.active:
            continue

        for meter in participant.meters:
            meterdata= MeterData.from_file(meter.ean, time_period)
            pool_consumed_energy_series.append(meterdata.production)
            pool_produced_energy_series.append(meterdata.consumption)

    pool_consumed_energy = pd.concat(pool_consumed_energy_series, axis=1)
    # the energy consumed by the pool
    total_consumed_energy = pool_consumed_energy.sum(axis=1)
    # every column is a participant
    equal_share = 100 / len(pool_consumed_energy.columns)
    consumer_participation = (pool_consumed_energy / total_consumed_energy.sum()).fillna(equal_share)

    # the energy produced by the pool
    pool_produced_energy = pd.concat(pool_produced_energy_series, axis=1)
    total_produced_energy = pool_produced_energy.sum(axis=1)
    # every column is a participant
    producer_participation = (pool_produced_energy / total_produced_energy.sum()).fillna(equal_share)

    # the traded energy is the minimum of the two totals
    traded_energy = pd.concat([total_produced_energy, total_consumed_energy], axis=1).min(axis=1)

    # the average price of each quarter
    quarterly_price = get_monthly_price(time_period.start.date())
    traded_euros = quarterly_price * traded_energy

    settled_euros_consumer = traded_euros.sum() * producer_participation
    settled_euros_producer = traded_euros.sum() * consumer_participation

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
            ParticipantSettlement(participant_id=participant.id, amount_paid=amount_paid, amount_earned=amount_earned)
        )

    return SettlementResult(period, community.id, results)


def get_monthly_price(month: date) -> float:
    """
    We use spread between average price for injection and consumption for july, according to vreg (belgian energy regulator)
    """
    return (0.34 - 0.04) / 2


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

