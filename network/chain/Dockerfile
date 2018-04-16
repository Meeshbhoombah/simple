FROM ubuntu:latest

MAINTAINER Rohan Mishra @Meeshbhoombah

WORKDIR /opt/eth

COPY ./genesis.json .

RUN apt-get update && \
    apt-get -y install software-properties-common && \
    add-apt-repository -y ppa:ethereum/ethereum && \
    apt-get update && \
    apt-get -y install vim ethereum

RUN geth --datadir ./chain init /opt/eth/genesis.json
RUN mkdir -p ~/.ethash && geth --datadir ./chain makedag 0 ~/.ethash

