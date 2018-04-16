.PHONY: network

init: network

network:

	docker build -t substrate/chain network/chain/.
	docker-compose scale node=3

