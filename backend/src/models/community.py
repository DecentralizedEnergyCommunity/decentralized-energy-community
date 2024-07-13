from __future__ import annotations
import dataclasses

from models.meter import MeterType, Meter, EAN, ean541448820044186577, ean541448820060527996, ean541449500000446547
from models.participant import Participant, ParticipantId

CommunityId = int


@dataclasses.dataclass
class Community:
    id: CommunityId
    participants: list[Participant]

    @staticmethod
    def create() -> Community:
        participant1 = Participant(
            id=ParticipantId(1),
            active=True,
            meters=[Meter(MeterType.PRODUCER, ean541448820044186577)],
        )

        participant2 = Participant(
            id=ParticipantId(2),
            active=True,
            meters=[Meter(MeterType.CONSUMER, ean541448820060527996)],
        )

        participant3 = Participant(
            id=ParticipantId(3),
            active=False,
            meters=[Meter(MeterType.PRODUCER, ean541449500000446547)]
        )

        return Community(id=0, participants=[participant1, participant2, participant3])

