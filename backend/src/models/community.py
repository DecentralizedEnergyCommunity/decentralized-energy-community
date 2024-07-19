from __future__ import annotations
import dataclasses

from models.meter import MeterType, Meter, EAN
from models.participant import Participant, ParticipantId
from utils.config import Config

CommunityId = int


@dataclasses.dataclass
class Community:
    id: CommunityId
    participants: list[Participant]

    @staticmethod
    def create() -> Community:

        config = Config.load()
        eans = config["eans"]

        participant1 = Participant(
            id=ParticipantId(1),
            active=True,
            meters=[Meter(MeterType.PRODUCER, eans["ean1"])],
        )

        participant2 = Participant(
            id=ParticipantId(2),
            active=True,
            meters=[Meter(MeterType.CONSUMER, eans["ean2"])],
        )

        participant3 = Participant(
            id=ParticipantId(3),
            active=False,
            meters=[Meter(MeterType.PRODUCER, eans["ean3"])]
        )

        return Community(id=0, participants=[participant1, participant2, participant3])

