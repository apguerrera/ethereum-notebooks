from web3 import Web3
from scripts.util import *


if __name__ == '__main__':
    ipc_path = '../testchain/geth.ipc'
    w3 = Web3(Web3.IPCProvider(ipc_path))

    key_path = '../testchain/keystore/UTC--2017-05-20T02-37-30.360937280Z--a00af22d07c87d96eeeb0ed583f8f6ac7812827e'
    key_passphrase = ''
    account = account_from_key(w3, key_path, key_passphrase)

    contract_path = '../contracts/WhiteList.sol'
    contract_name = 'WhiteList'
    contract_interface = compile_contract(contract_path, contract_name)

    tx_hash = deploy_contract(w3, account, contract_path, contract_name)

    # wait for transaction to be included to block
    w3.eth.waitForTransactionReceipt(tx_hash)

    contract_address = created_contract_address(w3, tx_hash)
    contract = get_contract(w3, contract_address, contract_interface['abi'])

    tx_hash = transact_function(w3, account, contract, 'add', [account.address])
    print(tx_hash)
