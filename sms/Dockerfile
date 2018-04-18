FROM ubuntu:latest
MAINTAINER Rohan Mishra @Meeshbhoombah

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    pip3 install --upgrade pip

WORKDIR /app

COPY . /requirements.txt
COPY . /run.py
COPY . /app
COPY . .env
COPY . /bin/run.sh

RUN pip install -r requirements.txt
RUN . .env
RUN ./run.sh

EXPOSE 5000

