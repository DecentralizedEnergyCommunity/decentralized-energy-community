from web3 import Web3
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

import json

contract_abi = json.loads('[<your_contract_ABI_here>]')
contract_address = '0xYourContractAddress'

contract = web3.eth.contract(address=contract_address, abi=contract_abi)


contract.