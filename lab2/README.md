CVE-2020-26265 Demonstration
================================

## Dependency

We are in a Ubuntu 18.04 server with a Docker service. Assume you are in `<root_to_project>/lab2`

```bash
sudo apt-get update && sudo apt-get install python3-dev python3-pip -y
```

Install the Python libraries.

```bash
python3 -m pip install -r ./requirements.txt
```

## Exploit

1. The Environment consists two nodes:

- `Node A`: geth v1.9.7

  ```bash
  $ docker pull ethereum/client-go:v1.9.7
  $ docker run -it --entrypoint /bin/sh -p 8545:8545 -p 30303:30303 -v $PWD/asset/genesis.json:/genesis.json --name nodeA ethereum/client-go:v1.9.7
  ```

- `Node B`: geth v1.9.20

  ```bash
  $ docker pull ethereum/client-go:v1.9.20
  $ docker run -it --entrypoint /bin/sh -p 8546:8546 -p 30304:30304 -v $PWD/asset/genesis.json:/genesis.json --name nodeA ethereum/client-go:v1.9.20`
  ```

2. Then enter each contrainer to initiate the blockchain. Here is an example for `Node A`

   ```bash
   $ docker exec -it nodeA /bin/sh
   $ geth --datadir .ethereum account new
   $ geth --datadir .ethereum init /genesis.json
   $ geth --datadir .ethereum --networkid 1337 --port 30303 --rpc --rpcaddr "0.0.0.0" --rpcport 8545 --rpccorsdomain "*" \
   		--rpcapi="db,eth,net,web3,personal,web3,miner" --allow-insecure-unlock --miner.threads 4 --maxpeers=3
   ```

3. Enter `Node A` to  add `Node B`

   get the enode from `Node A`. Note that we need to replace IP of enode to the IPv4 of Node A.

   ```bash
   $ docker exec -it nodeA geth attach .ethereum/geth.ipc
   > admin.nodeInfo.enode
   ```

   Go to `Node B`. Add enode of `Node A` to `Node B`

   ```bash
   $ docker exec -it nodeB geth attach .ethereum/geth.ipc
   > admin.addPeer("NodeA’s enode url")
   > admin.peers # check here
   ```

4. Start mining

   ```bash
   > miner.start()
   ```

5. Exploit

   ```bash
   $ python ./example.py
   $ python3 ./ack.py
   ```

   The block hash in the same block hash should be different.