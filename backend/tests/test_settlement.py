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
    participant1 = Participant(
        id=ParticipantId(1),
        active=True,
        meters=[Meter(MeterType.PRODUCER, EAN("541448820044186577"))],
    )

    participant2 = Participant(
        id=ParticipantId(2),
        active=True,
        meters=[Meter(MeterType.CONSUMER, EAN("541448820060527996"))],
    )

    participant3 = Participant(
        id=ParticipantId(3),
        active=False,
        meters=[Meter(MeterType.PRODUCER, EAN("541449500000446547"))]
    )

    return Community(id=0, participants=[participant1, participant2, participant3])


def test_settlement_period_1(community: Community):
    hour = TimePeriod.from_id(0)
    settlement_result = asyncio.run(settle(hour, community))
    assert settlement_result.community_id == 0
    for participation_result in settlement_result.results:
        assert participation_result.amount_paid == 0
        assert participation_result.amount_earned == 0


def test_settlement_period_2(community: Community):
    time_period = TimePeriod(genesis, genesis+timedelta(days=7))
    settlement_result = asyncio.run(settle(time_period, community))
    assert settlement_result.community_id == 0
    total_paid = 0
    total_earned = 0
    for participation_result in settlement_result.results:
        total_paid += participation_result.amount_paid
        total_earned += participation_result.amount_earned

    assert abs(total_paid - total_earned) < 0.0000001


