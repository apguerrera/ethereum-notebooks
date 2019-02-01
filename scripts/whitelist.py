from scripts.util import deploy_contract, wait_contract_address, get_contract, call_function, transact_function


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
