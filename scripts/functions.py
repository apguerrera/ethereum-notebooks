import web3
import time

from web3 import Web3
from eth_account import Account
from web3.middleware import geth_poa_middleware

# ipc:./testchain/geth.ipc

w3 = Web3(Web3.IPCProvider("./testchain/geth.ipc"))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# variables
ethPriceUSD = 150.00   # USD
defaultGasPrice = w3.toWei(16, "gwei");
accounts = []
accountNames = {}

minerAccount = w3.eth.accounts[0]
contractOwnerAccount = w3.eth.accounts[1]
aliceAccount = w3.eth.accounts[2]
bobAccount = w3.eth.accounts[3]
carolAccount = w3.eth.accounts[4]
daveAccount = w3.eth.accounts[5]
account6 = w3.eth.accounts[6]
account7 = w3.eth.accounts[7]
account8 = w3.eth.accounts[8]
account9 = w3.eth.accounts[9]
account10 = w3.eth.accounts[10]
account11 = w3.eth.accounts[11]

baseBlock = w3.eth.blockNumber
tokenContractAddress = ""
tokenContractAbi = ""

def sign_transaction(txn):
    # Flesh out the transaction for local signing
    next_nonce = w3.eth.getTransactionCount(str(w3.eth.accounts[0]))
    signable_transaction = dict(
      txn,
      nonce=next_nonce,
      gasPrice=w3.toWei(4, 'gwei'),
    )
    # Sign transaction
    encrypted_key = open('testchain/keystore/UTC--2017-05-20T02-37-30.360937280Z--a00af22d07c87d96eeeb0ed583f8f6ac7812827e').read()
    private_key = w3.eth.account.decrypt(encrypted_key, '')
    signature_info = w3.eth.account.signTransaction(signable_transaction, private_key)
    # Broadcast transaction
    txn_hash = w3.eth.sendRawTransaction(signature_info.rawTransaction)
    # Wait for the transaction to be mined
    receipt = w3.eth.waitForTransactionReceipt(txn_hash)

    return receipt

def addAccount(account, accountName):
    accounts.append(account)
    accountNames[account] = accountName

def unlockAccounts(password):
    i = 0
    while ( i < len(accounts) and i < len(w3.eth.accounts)): # .length and
        w3.personal.unlockAccount(w3.eth.accounts[i], str(password), 100000)
        if (i > 0 and w3.eth.getBalance(w3.eth.accounts[i]) == 0):
            w3.eth.sendTransaction({'from': str(w3.eth.accounts[0]), 'to': str(w3.eth.accounts[i]), 'value': w3.toWei(1000000, "ether")})
            print(i)
        i=i+1

def addTokenContractAddressAndAbi(address, tokenAbi):
    tokenContractAddress = address
    tokenContractAbi = tokenAbi

def printBalances():
    if (tokenContractAddress == "" or tokenContractAbi == ""):
        token = ""
        decimals = 18
    else:
        token = w3.eth.contract(tokenContractAbi).at(tokenContractAddress)
        token.decimals()
    i = 1
    totalTokenBalance = 0
    print(" # Account                                      EtherBalanceChange                   Token Name")
    print("-- ------------------------------------------ -------------------- ----------------------- ---------------------")

    while (i < len(accounts)):
        etherBalanceBaseBlock = w3.eth.getBalance(accounts[i], baseBlock)
        etherBalanceBaseBlock = w3.eth.getBalance(accounts[i], baseBlock)
        etherBalance = w3.fromWei((w3.eth.getBalance(accounts[i]) - etherBalanceBaseBlock), "ether")
        if token == "":
            tokenBalance = 0
        else:
            tokenBalance = token.balanceOf(accounts[i]).shift(-decimals)
        totalTokenBalance = totalTokenBalance + tokenBalance
        print("" + pad2(i) + " " + accounts[i]  + " " + pad(etherBalance) + " " + padToken(tokenBalance, decimals) + " " + accountNames[accounts[i]])
        i = i + 1

    print("-- ------------------------------------------ -------------------- ----------------------- ---------------------")
    print("                                                                   " + padToken(totalTokenBalance, decimals) + " Total Token Balances")
    print("-- ------------------------------------------ -------------------- ----------------------- ---------------------")
    print("")

def pad2(s):
    o = str(s)
    while(len(o) < 2):
        o = " " + o
    return o

def pad(s):
    o = str(s)
    while(len(o) < 20):
        o = " " + o
    return o

def padToken(s, decimals):
    o = str(s)
    l = decimals + 5
    while(len(o) < l):
        o = " " + o
    return o

def waitOneBlock(oldCurrentBlock):
    while (w3.eth.blockNumber <= oldCurrentBlock):
        time.sleep(0.1)
    print("RESULT: Waited one block")
    print("RESULT: ")
    return w3.eth.blockNumber

def assertCondition(condition, message):
    if condition:
        print("RESULT: PASS " + message)
    else:
        print("RESULT: FAIL " + message)
    return condition

def assertIntEquals(result, expected, message):
    if int(result) == int(expected):
        print("RESULT: PASS " + message)
        return True
    else:
        print("RESULT: FAIL " + message)
        return False

def assertEtherBalance(account, expectedBalance):
    etherBalance = w3.fromWei(w3.eth.getBalance(account), "ether")
    if etherBalance == expectedBalance:
        print("RESULT: OK " + str(account) + " has expected balance " + str(expectedBalance))
    else:
        print("RESULT: FAILURE " + str(account) + " has balance " + str(etherBalance) + " <> expected " + str(expectedBalance))

def failIfTxStatusError(tx, msg):
    status = w3.eth.getTransactionReceipt(tx).status
    if status == 0:
        print("RESULT: FAIL " + str(msg))
        return 0
    else:
        print("RESULT: PASS " + str(msg))
        return 1

def passIfTxStatusError(tx, msg):
    status = w3.eth.getTransactionReceipt(tx).status
    if status == 1:
        print("RESULT: FAIL " + str(msg))
        return 0
    else:
        print("RESULT: PASS " + str(msg))
        return 1


def gasEqualsGasUsed(tx):
    gas = w3.eth.getTransaction(tx).gas
    gasUsed = w3.eth.getTransactionReceipt(tx).gasUsed
    return (gas == gasUsed)


def failIfGasEqualsGasUsed(tx, msg):
    gas = w3.eth.getTransaction(tx).gas
    gasUsed = w3.eth.getTransactionReceipt(tx).gasUsed
    if (gas == gasUsed):
        print("RESULT: FAIL " + str(msg))
        return 0
    else:
        print("RESULT: PASS " + str(msg))
        return 1


def passIfGasEqualsGasUsed(tx, msg):
  gas = w3.eth.getTransaction(tx).gas
  gasUsed = w3.eth.getTransactionReceipt(tx).gasUsed
  if gas == gasUsed:
    print("RESULT: PASS " + str(msg))
    return 1
  else:
    print("RESULT: FAIL " +str(msg))
    return 0

def failIfGasEqualsGasUsedOrContractAddressNull(contractAddress, tx, msg):
    if contractAddress == null:
        print("RESULT: FAIL " + str(msg))
        return 0
    else:
        gas = eth.getTransaction(tx).gas
        gasUsed = eth.getTransactionReceipt(tx).gasUsed
        if (gas == gasUsed):
            print("RESULT: FAIL " + str(msg))
            return 0
        else:
            print("RESULT: PASS " + str(msg))
            return 1


def treeAsList(tree):
    result = []
    treeAsListWalker(tree, tree.functions.root().call(), result)
    return result.sort()

def treeAsListWalker(tree, node, result):
    SENTINEL = 0
    nodeData = tree.functions.getNode(node).call()
    leftNode = nodeData[2]
    rightNode = nodeData[3]
    if (leftNode != SENTINEL):
        treeAsListWalker(tree, leftNode, result)
    if (nodeData[0] != SENTINEL):
        result.append(parseInt(nodeData[0]))
    if (rightNode != SENTINEL):
        treeAsListWalker(tree, rightNode, result)


addAccount(minerAccount, "Account #0 - Miner")
addAccount(contractOwnerAccount, "Account #1 - Owner")
addAccount(aliceAccount, "Account #2 - Alice")
addAccount(bobAccount, "Account #3 - Bob")
addAccount(carolAccount, "Account #4 - Carol")
addAccount(daveAccount, "Account #5 - Dave")
addAccount(account6, "Account #6")
addAccount(account7, "Account #7")
addAccount(account8, "Account #8")
addAccount(account9, "Account #9")
addAccount(account10, "Account #10")
addAccount(account11, "Account #11")

#printBalances()
