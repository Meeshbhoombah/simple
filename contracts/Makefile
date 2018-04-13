#
# contracts/Makefile
#

.PHONY: vyper-install erc-token

init: env vyper-install simple-contracts

env:

	virtualenv venv
	. venv/bin/activate

test:

	pytest

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

