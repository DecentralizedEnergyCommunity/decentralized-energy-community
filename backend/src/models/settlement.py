from dataclasses import dataclass

from models import participant
from models.community import CommunityId

SettlementId = int


@dataclass(frozen=True)
class ParticipantSettlement:
    participantId: participant.ParticipantId
    amount_paid: int
    amount_earned: int


@dataclass
class SettlementResult:
    id: SettlementId
    communityId: CommunityId
    results: list[ParticipantSettlement]
