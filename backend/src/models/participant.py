from dataclasses import dataclass

from models.meter import Meter

ParticipantId=int

@dataclass
class Participant:
    active: bool
    meters: list[Meter]


@dataclass
class ParticipantResult:
    participantId: ParticipantId
    value: int
