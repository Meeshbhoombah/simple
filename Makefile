.PHONY:

init:

network-deploy:

	docker build -t network/Dockerfile.base .

	docker-compose up -d
	echo "##################################"
	echo "USE `docker-compose scale node=[# of nodes]`"
	echo "to create more nodes on the network"
	echo "##################################"

