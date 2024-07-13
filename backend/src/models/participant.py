from dataclasses import dataclass

from models.meter import Meter

ParticipantId = int


@dataclass(frozen=True)
class Participant:
    id: ParticipantId
    active: bool
    meters: list[Meter]


@dataclass(frozen=True)
class ParticipantResult:
    participantId: ParticipantId
    value: int
