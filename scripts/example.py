from web3 import Web3
from scripts.functions import *

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
