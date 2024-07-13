import dataclasses

from models.participant import Participant

CommunityId = int


@dataclasses.dataclass
class Community:
    id: CommunityId
    participants: list[Participant]
