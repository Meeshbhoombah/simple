.PHONY: private

private: install-private run-private

install-private:

	brew tap ethereum/ethereum
	brew install ethereum
	
run-private:

	geth --dev

