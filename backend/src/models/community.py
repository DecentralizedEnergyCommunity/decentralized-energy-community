from __future__ import annotations
import dataclasses

from models.meter import MeterType, Meter, EAN
from models.participant import Participant, ParticipantId

CommunityId = int


@dataclasses.dataclass
class Community:
    id: CommunityId
    participants: list[Participant]

    @staticmethod
    def stub() -> Community:
        participant1 = Participant(
            id=ParticipantId(1),
            active=True,
            meters=[Meter(MeterType.PRODUCER, ean)],
        )

        participant2 = Participant(
            id=ParticipantId(2),
            active=True,
            meters=[Meter(MeterType.CONSUMER, ean)],
        )

        participant3 = Participant(
            id=ParticipantId(3),
            active=False,
            meters=[Meter(MeterType.PRODUCER, ean)]
        )

        return Community(id=0, participants=[participant1, participant2, participant3])

