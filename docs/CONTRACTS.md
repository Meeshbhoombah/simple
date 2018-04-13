# Contracts
**/contracts/**

**TODO**
- [ ] Prerequisites
- [ ] Private Network Instructions Link

These are the various planned implementations of Simple:
- [x] ERC20.v.py - an implementation of the ERC-20 standard
- [ ] bitcoin.v.py - a Bitcoin-like token

The follow instructions are for recreating the Simple smart contract development environment. 
Instructions for running the contracts on a private Ethereum network can be found [here]().

It is not recommended to deploy the Simple smart contracts on the public Ethereum network as 
this is meant to be an educational implementation.

## Prerequisites
The Simple smart contracts are written in Vyper, an experimental language for the Ethereum
blockchain. Vyper is **pre-beta** and has not been release yet. As such Vyper must be built and 
installed manually. 

### MacOS
Download Homebrew.

Install pip.

Use pip to install virtualenv.

## Installation
It is recommended to create an isolated virtual environment (using `virtualenv` or something 
similar) for Simple. After creating the virtual environment, install the required packages
with `pip`.
```bash
$ pip install -r requirements.txt
```

Simple uses Vyper as its primary language for smart contracts. You can do this easily
with the `Makefile`:
```bash
$ make vyper-install
```

## Testing
The various Simple smart contracts can be tested with the `Makefile`.
```bash
$ make test
```

The test suite provides **100% converage of all Simple smart contracts**.

## Usage 
Use the Vyper compiler to compile smart contracts.
```bash
$ vyper ERC20.v.py
```

