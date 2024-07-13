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
class Participant:
    id: int
    active: bool
    meters: list[Meter]
@dataclasses.dataclass
class Community:
    participantId: int
    participants: list[Participant]

@dataclasses.dataclass
class SettlementResult:
    participantId: ParticipantId
    value: int

@dataclasses.dataclass
class SettlementResult:
    community: int
    result: list[ParticipantResult]

async def settle(community: Community) -> SettlementResult:
    # todo add the settlement magic here!!!
    return SettlementResult(1, [])

def getCommunities() -> list[Community]:
    # get the community from the smart contract.
    return []

def updateContract(result : SettlementResult) -> None:
    # todo write this back to the contract
    return None


async def run() -> None:
    communities = getCommunities()

    for c in communities:
        result = await settle(c)
        updateContract(result)



if __name__ == '__main__':
    run()
