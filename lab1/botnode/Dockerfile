FROM ethereum/client-go:v1.6.6

RUN mkdir /geth_node/
WORKDIR /geth_node/

COPY ./scripts/_genesis.json /geth_node/

ENV PATH="/:${PATH}"
RUN geth init --datadir /geth_node/datadir /geth_node/_genesis.json 2> /geth_node/init.log
ADD ./scripts/keystore /geth_node/datadir/keystore/
ADD ./scripts/start_console.sh /geth_node/start_console.sh
RUN chmod u+x /geth_node/start_console.sh 

EXPOSE 30303
EXPOSE 8545

ENTRYPOINT sh
