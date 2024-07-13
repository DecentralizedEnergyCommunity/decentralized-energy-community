from datetime import timedelta

import pytest

from app.settlement import settle
from models.community import Community
from models.meter import Meter, MeterType, EAN
from models.participant import Participant, ParticipantId
import asyncio

from models.timeperiod import TimePeriod, genesis


@pytest.fixture
def community() -> Community:
    return Community.stub()


def test_settlement_period_1(community: Community):
    hour = TimePeriod.from_id(0)
    settlement_result = asyncio.run(settle(hour, community))
    assert settlement_result.community_id == 0
    for participation_result in settlement_result.results:
        assert participation_result.amount_paid == 0
        assert participation_result.amount_earned == 0


def test_settlement_period_2(community: Community):
    time_period = TimePeriod(genesis, genesis + timedelta(days=7))
    settlement_result = asyncio.run(settle(time_period, community))
    assert settlement_result.community_id == 0
    total_paid = 0
    total_earned = 0
    for participation_result in settlement_result.results:
        total_paid += participation_result.amount_paid
        total_earned += participation_result.amount_earned

    assert abs(total_paid - total_earned) < 0.0000001
