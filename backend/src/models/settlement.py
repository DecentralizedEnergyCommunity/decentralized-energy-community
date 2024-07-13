from dataclasses import dataclass

from models.community import CommunityId
from models.participant import ParticipantId
from models.timeperiod import TimePeriod



@dataclass(frozen=True)
class ParticipantSettlement:
    participant_id: ParticipantId
    amount_paid: int
    amount_earned: int


@dataclass
class SettlementResult:
    id: TimePeriod
    community_id: CommunityId
    results: list[ParticipantSettlement]
