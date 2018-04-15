FROM ubuntu:latest

MAINTAINER Rohan Mishra @Meeshbhoombah

WORKDIR /opt/eth

COPY ./simple/genesis.json .

RUN RUN apt-get update && \
    apt-get -y install software-properties-common && \
    add-apt-repository -y ppa:ethereum/ethereum && \
    add-apt-repository -y ppa:ethereum/ethereum-dev && \
    apt-get update

RUN geth --datadir ./chain init ./simple/genesis.json
RUN mkdir -p ~/.ethash && geth --datadir ./chain makedag 0 ~/.ethash

