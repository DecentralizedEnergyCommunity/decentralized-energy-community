from dataclasses import dataclass

from models import participant
from models.community import CommunityId

TimePeriodId = int


@dataclass(frozen=True)
class ParticipantSettlement:
    participantId: participant.ParticipantId
    amount_paid: int
    amount_earned: int


@dataclass
class SettlementResult:
    id: TimePeriodId
    communityId: CommunityId
    results: list[ParticipantSettlement]
