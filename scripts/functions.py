from web3 import Web3
from scripts.util import *


# deploy Whitelist contract and return contract object
def deploy_whitelist(w3, account):
    tx_hash, contract_interface = deploy_contract(w3, account, '../contracts/WhiteList.sol', 'WhiteList')
    contract_address = wait_contract_address(w3, tx_hash)
    contract = get_contract(w3, contract_address, contract_interface['abi'])
    return contract


# return True if address in whitelist, else return False
def is_in_list(account, contract, address):
    return call_function(account, contract, 'isInWhiteList', address)


# add list of addresses to whitelist
def add_to_list(w3, account, contract, addresses):
    return transact_function(w3, account, contract, 'add', addresses)


# remove list of addresses from whitelist
def remove_from_list(w3, account, contract, addresses):
    return transact_function(w3, account, contract, 'remove', addresses)


# add address to controllers
def add_controller(w3, account, contract, address):
    return transact_function(w3, account, contract, 'addController', address)


# remove address from controllers
def remove_controller(w3, account, contract, address):
    return transact_function(w3, account, contract, 'removeController', address)


if __name__ == '__main__':
    ipc_path = '../testchain/geth.ipc'
    w3 = Web3(Web3.IPCProvider(ipc_path))

    key_path = '../testchain/keystore/UTC--2017-05-20T02-37-30.360937280Z--a00af22d07c87d96eeeb0ed583f8f6ac7812827e'
    key_passphrase = ''
    account = account_from_key(w3, key_path, key_passphrase)

    whitelist = deploy_whitelist(w3, account)

    tx_hash = add_to_list(w3, account, whitelist, [account.address])
    print(wait_event(w3, whitelist, tx_hash, 'AccountListed')[0]['args'])

    tx_hash = add_controller(w3, account, whitelist, w3.eth.accounts[5])
    print(wait_event(w3, whitelist, tx_hash, 'ControllerAdded')[0]['args'])
