You need to install "docker" into your computer first if it is not installed.

## Step 1: build docker images
1. enter into the `bootnode` path, e.g., `cd ./bootnode/`
2. run `sudo docker build -t bootnode .` to build the `bootnode` image
3. enter into the `node` path, e.g., `cd ./node/`
4. run `sudo docker build -t node .` to build the `node` image
5. enter into the `botnode` path, e.g., `cd ./botnode/`
6. run `sudo docker build -t botnode .` to build the `botnode` image
7. run `sudo docker image ps` to check the images, the terminal will output contents like the following information
   ```sh
   REPOSITORY           TAG       IMAGE ID       CREATED          SIZE
   botnode              latest    b5e93a73f3e5   6 seconds ago        384MB
   node                 latest    5d77127535f8   42 seconds ago       384MB
   bootnode             latest    de4ca6d53244   About a minute ago   384MB
   ethereum/client-go   v1.6.6    18a3fff827f9   5 years ago          384MB
   ```

## step 2: start containers
We will start seven containers in lab1. Four of them are honest nodes (1 bootnode which first launches the blockchain network and 1 victim node), and the other three of them are bot nodes of attackers.
1. launch the bootnode by `sudo docker run --name boot -it bootnode /bin/bash`, and tap `Ctrl + P + Q` to exit the container with keeping it alive
2. launch three (honest) nodes and do not forget to exit them with keeping them alive
   ```sh
   sudo docker run --name node1 -it node /bin/bash
   sudo docker run --name node2 -it node /bin/bash
   sudo docker run --name node3 -it node /bin/bash
   ```
3. launch the other three bot nodes and do not forget to exit them with keeping them alive
   ```sh
   sudo docker run --name bot1 -it botnode /bin/bash
   sudo docker run --name bot2 -it botnode /bin/bash
   sudo docker run --name bot3 -it botnode /bin/bash
   ```
4. check the running containers by `sudo docker ps`, and the terminal will output contents like the following information
   ```sh
   CONTAINER ID   IMAGE      COMMAND                  CREATED          STATUS          PORTS                            NAMES
   aa7ae8dc41e7   botnode    "/bin/sh -c sh /bin/…"   3 minutes ago    Up 3 minutes    8545/tcp, 30303/tcp, 30303/udp   bot3
   dc29bec29caf   botnode    "/bin/sh -c sh /bin/…"   4 minutes ago    Up 4 minutes    8545/tcp, 30303/tcp, 30303/udp   bot2
   b694e0f858eb   botnode    "/bin/sh -c sh /bin/…"   5 minutes ago    Up 5 minutes    8545/tcp, 30303/tcp, 30303/udp   bot1
   8946118bc9e9   node       "/bin/sh -c sh /bin/…"   7 minutes ago    Up 7 minutes    8545/tcp, 30303/tcp, 30303/udp   node3
   6d6de5f0b93d   node       "/bin/sh -c sh /bin/…"   8 minutes ago    Up 8 minutes    8545/tcp, 30303/tcp, 30303/udp   node2
   99c0f536eda2   node       "/bin/sh -c sh /bin/…"   9 minutes ago    Up 9 minutes    8545/tcp, 30303/tcp, 30303/udp   node1
   de62c6d9b6fa   bootnode   "/bin/sh -c sh /bin/…"   11 minutes ago   Up 11 minutes   8545/tcp, 30303/tcp, 30303/udp   boot
   ```