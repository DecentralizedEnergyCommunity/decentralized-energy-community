import decimal
from datetime import date

import pandas as pd

from models.community import Community
from models.meterdata import MeterData
from models.settlement import SettlementResult, ParticipantSettlement
from models.timeperiod import TimePeriod, genesis


async def settle(time_period: TimePeriod, community: Community) -> SettlementResult:
    pool_consumed_energy_series: list[pd.Series] = []
    pool_produced_energy_series: list[pd.Series] = []

    for participant in community.participants:
        # filter non active users
        if not participant.active:
            continue

        for meter in participant.meters:
            meterdata = MeterData.from_file(meter.ean, time_period)
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
    quarterly_price = get_monthly_price_eur_kwh(time_period.start.date()) / 1000
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

        amount_paid = settled_euros_consumer[eans].sum(axis=1).sum()
        amount_earned = settled_euros_producer[eans].sum(axis=1).sum()
        results.append(
            ParticipantSettlement(participant_id=participant.id, amount_paid=amount_paid, amount_earned=amount_earned)
        )

    return SettlementResult(time_period, community.id, results)


def get_monthly_price_eur_kwh(month: date) -> decimal.Decimal:
    """
    We use spread between average price for injection and consumption for july, according to Vreg website (belgian energy regulator).
    This data can be fetched from their API instead
    """
    return (0.34 - 0.04) / 2


def update_contract(result: SettlementResult) -> None:
    # todo write this back to the contract
    return None


async def run() -> None:
    communities = [Community.stub()]

    for c in communities:
        settlement_result = await settle(TimePeriod.quarter_hour(genesis), c)
        update_contract(settlement_result)


if __name__ == "__main__":
    run()
