FROM ubuntu:latest
MAINTAINER Rohan Mishra @Meeshbhoombah

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev git && \
    cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    pip3 install --upgrade pip

WORKDIR /sms

COPY requirements.txt /sms
COPY run.py /sms
COPY ./app /sms
COPY run.sh /sms
RUN chmod +x run.sh

RUN pip install -r requirements.txt
ENTRYPOINT ['python']
CMD ['run.py']
 
EXPOSE 5000

