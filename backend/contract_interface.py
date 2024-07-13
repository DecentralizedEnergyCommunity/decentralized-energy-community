import json
import os
from web3 import Web3


web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

print(web3.eth.get_block_number())
# path to the file DecentralizedEnergyCommunity.json
contract_file = os.environ["CONTRACT_FILE"]

with open(contract_file) as f:
    contract_data = json.load(f)


contract = web3.eth.contract(address=contract_data["address"], abi = contract_data["abi"])
print(contract)





