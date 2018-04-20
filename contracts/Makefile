#
# contracts/Makefile
#

.PHONY: vyper-install erc-token

init: env vyper-install simple-contracts

env:

	virtualenv venv
	. venv/bin/activate
	pip install -r requirements.txt

test:

	pytest

test-silent:

	pytest -q

# It is recommended that you install Vyper in a 
# virtual environment
vyper-install:
ifeq ($(shell uname),Darwin)

	brew install gmp
	git clone https://github.com/ethereum/vyper.git
	cd vyper
	make
	cd ../
	rm -rf vyper

else

	sudo apt-get install build-essential libssl-dev libffi-dev
	git clone https://github.com/ethereum/vyper.git
	cd vyper
	make
	cd ../
	rm -rf vyper

endif

simple-contracts: erc-token

erc-token:

	vyper ERC20.v.py

