import dataclasses

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

Meter=str
ParticipantId=int
CommunityId=int

@dataclasses.dataclass
class Community:
    participantId: int

@dataclasses.dataclass
class Participants:
    id: int
    active: int
    meters: list[Meter]
@dataclasses.dataclass
class SettlmentRequest:
    community: Community
    participants: list[Participants]

@dataclasses.dataclass
class ParticipantResult:
    participantId: ParticipantId
    value: int

@dataclasses.dataclass
class SettlementResult:
    community: int
    result: list[ParticipantResult]

async def settle(request: SettlmentRequest) -> SettlementResult:
    # todo add the settlement magic here!!!
    return SettlementResult(1, [])
