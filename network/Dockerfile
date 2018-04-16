FROM substrate/chain

MAINTAINER Rohan Mishra @Meeshbhoombah

WORKDIR /opt/eth

COPY ./bin/node.sh .
COPY ./chain/password.txt .

RUN chmod a+x ./node.sh

CMD ./node.sh

