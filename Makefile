.PHONY:

init:

network:

	cd network/chain/
	docker build -t substrate/chain .
	cd ../../

	docker-compose up -d
	echo "##################################"
	echo "USE `docker-compose scale node=[# of nodes]`"
	echo "to create more nodes on the network"
	echo "##################################"

