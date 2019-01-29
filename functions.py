from web3 import Web3
import solc


# TODO: move util functions to separate file

# decrypt keystore file and return account
def account_from_key(w3, key_path, passphrase):
    with open(key_path) as key_file:
        key_json = key_file.read()
    private_key = w3.eth.account.decrypt(key_json, passphrase)
    account = w3.eth.account.privateKeyToAccount(private_key)
    return account


# compile contract using solc and return contract interface
def compile_contract(path, name):
    compiled_contacts = solc.compile_files([path])
    contract_interface = compiled_contacts['{}:{}'.format(path, name)]
    return contract_interface


# compile contract, deploy it from account specified, then return transaction hash
def deploy_contract(w3, account, path, name):
    contract_interface = compile_contract(path, name)
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    transaction = contract.constructor().buildTransaction({
        'nonce': w3.eth.getTransactionCount(account.address),
        'from': account.address
    })
    signed_transaction = w3.eth.account.signTransaction(transaction, account.privateKey)
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return tx_hash.hex()


# returns address of fresh created contract using hash returned from deploy_contract
# returns None if transaction was not included to block
def created_contract_address(w3, tx_hash):
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    if not tx_receipt:
        return None
    return tx_receipt['contractAddress']


# returns contract object using its address and ABI
def get_contract(w3, address, abi):
    return w3.eth.contract(address=address, abi=abi)


def transact_function(w3, account, contract, function_name, args):
    transaction = contract.functions[function_name](args).buildTransaction({
        'nonce': w3.eth.getTransactionCount(account.address),
        'from': account.address
    })
    signed_transaction = w3.eth.account.signTransaction(transaction, account.privateKey)
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return tx_hash.hex()


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
