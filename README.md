# ethereum-notebooks

## Interacting with Ethereum using web3.py and Jupyter Notebooks
Step by step guide for setting up a Jupyter notebook, connecting to an Ethereum node and deploying a Smart Contract. 

### Installing Dependencies
#### Jupyter Notebooks

```
pip3 install --upgrade pip
pip3 install jupyter
```

[jupyter.readthedocs.io](https://medium.com/r/?url=https%3A%2F%2Fjupyter.readthedocs.io%2Fen%2Flatest%2Finstall.html)

##### Installing Web3.py

```
pip install web3
```

[web3py.readthedocs.io](https://medium.com/r/?url=https%3A%2F%2Fweb3py.readthedocs.io%2Fen%2Fstable%2Fquickstart.html)

[web3.py Clean Install](https://web3py.readthedocs.io/en/stable/troubleshooting.html#setup-environment)

#### Installing Solc

```
npm install -g solc
```

[Solc - Solidity Compiler](https://medium.com/r/?url=https%3A%2F%2Fsolidity.readthedocs.io%2Fen%2Fv0.4.24%2Finstalling-solidity.html)

### Running Geth

```
./00_runGeth.sh
```

Or alternatively run the following

```
geth --dev --dev.period 2 --datadir ./testchain --rpc --rpccorsdomain '*' --rpcport 8646 --rpcapi "eth,net,web3,debug" --port 32323 --maxpeers 0 console
```

### Running Jupyter Notebooks

```
./01_runNotebook.sh
```
