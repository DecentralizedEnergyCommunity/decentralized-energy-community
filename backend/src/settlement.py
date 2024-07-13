import datetime

from models.community import Community
from models.settlement import SettlementResult


async def settle(date: datetime.datetime, community: Community) -> SettlementResult:
    # todo add the settlement magic here!!!
    return SettlementResult(1, [])


def get_communities() -> list[Community]:
    # get the community from the smart contract.
    return []


def update_contract(result: SettlementResult) -> None:
    # todo write this back to the contract
    return None


async def run() -> None:
    communities = get_communities()

    for c in communities:
        result = await settle(c)
        update_contract(result)


if __name__ == '__main__':
    run()

