from web3 import Web3
import solc


# compile contract using solc and return contract interface
def compile_contract(contract_path, contract_name):
    compiled_contacts = solc.compile_files([contract_path])
    contract_interface = compiled_contacts['{}:{}'.format(contract_path, contract_name)]
    return contract_interface


# compile contract, deploy it from account specified in key_path keystore file, then return transaction hash
def deploy_contract(w3, key_path, passphrase, contract_path, contract_name):
    with open(key_path) as key_file:
        key_json = key_file.read()
    private_key = w3.eth.account.decrypt(key_json, passphrase)
    account = w3.eth.account.privateKeyToAccount(private_key)

    contract_interface = compile_contract(contract_path, contract_name)
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    transaction = contract.constructor().buildTransaction({
        'nonce': w3.eth.getTransactionCount(account.address),
        'from': account.address
    })
    signed_transaction = w3.eth.account.signTransaction(transaction, account.privateKey)
    tx = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return tx.hex()


if __name__ == '__main__':
    ipc_path = '../testchain/geth.ipc'
    key_path = '../testchain/keystore/UTC--2017-05-20T02-37-30.360937280Z--a00af22d07c87d96eeeb0ed583f8f6ac7812827e'
    passphrase = ''

    contract_path = '../contracts/WhiteList.sol'
    contract_name = 'WhiteList'

    w3 = Web3(Web3.IPCProvider(ipc_path))
    tx_hash = deploy_contract(w3, key_path, passphrase, contract_path, contract_name)
    print(tx_hash)
