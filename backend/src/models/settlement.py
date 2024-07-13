from dataclasses import dataclass

from models.community import CommunityId
from models.participant import ParticipantResult


@dataclass
class SettlementResult:
    communityId: CommunityId
    results: list[ParticipantResult]
