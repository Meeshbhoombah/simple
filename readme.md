# Simple
A node of the simple blockchain 🤑 implemented in Python 🐍 and Vyper.

**Features:**
- [x] ERC-20 token implemented in Vyper
- [x] 100% test coverage on contracts
- [ ] Flask server for sending tokens via SMS
- [x] Private Ethereum Network
- [x] Running on Docker

## Getting Started
These instructions will get you a copy of the project up and running on your local machine 
for development and testing purposes. Instructions for have not yet been completed. This
document is in the early stages of its creation, please excuse its sparcity.

### Installing
1. Docker
2. Makefile

#### Manual Installation
Fork and/or clone the repository. It is recommended to build Python packages in a 
virutal environment to avoid conflicts.

1. Create a virtual environment with `virtualenv` using Homebrew's version of python, 
   `python3`
2. Install vyper
3. Install requirements without Vyper.

Install the dependencies with `pip`.
```
$ pip install -r requirements.txt
```
4. Run tests
5. Create a private Network.

The Simple contracts are for education purposes only (although the ERC20 contract is a 
valid ERC20 token). As such, they are not deployed on the `mainnet`. For running the SMS client
a private network can be deployed.

```bash
$ make private
```

`make private` installs `geth` (the Golang implementation of the Ethereum client) each time it
runs. After initally using `make private` in the future use `make run-private`


