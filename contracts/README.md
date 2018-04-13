# Contracts
**simple/contracts/**

These are the various versions of Simple implemented:
- [x] ERC20.v.py - an implementation of the ERC-20 standard
- [ ] bitcoin.v.py - a Bitcoin-like token

## Prerequisites
Running and testing the Simple smart contracts requires:
```
Homebrew
python 3.6
pip
virtualenv
```
It is recommended to create an isolated virtual envrionments (using `virtualenv` or something 
similar) for Simple. After creating the virtual environment, install the required packages
with `pip`.
```bash
$ pip install -r requirements.txt
```

Simple uses Vyper as its primary language for smart contracts. Vyper is **pre-beta** and has
not been release yet. As such Vyper must be built and installed manually. You can do this easily
with the `Makefile`:
```bash
$ make vyper-install
```

## Testing
The various Simple smart contracts can be tested with the `Makefile`.
```bash
$ make test
...
```

