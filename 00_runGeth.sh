#!/bin/sh

# ----------------------------------------------------------------------------------------------
# Testing the smart contract
#
# Enjoy. (c) BokkyPooBah / Bok Consulting Pty Ltd 2017. The MIT Licence.
# Enjoy. (c) Adrian Guerrera / Deepyr Pty Ltd 2019. The MIT Licence.
# ----------------------------------------------------------------------------------------------


rm -f ./testchain/geth/chaindata/*

# geth --datadir ./testchain init genesis.json

# geth --datadir ./testchain --unlock 0 --password ./testpassword --rpc --rpccorsdomain '*' --rpcport 8646 --rpcapi "eth,net,web3,debug" --port 32323 --mine --minerthreads 1 --maxpeers 0 --targetgaslimit 994712388 console
geth --dev --dev.period 2 --datadir ./testchain --rpc --rpccorsdomain '*' --rpcport 8646 --rpcapi "eth,net,web3,debug" --port 32323 --maxpeers 0 --targetgaslimit 994712388 console
