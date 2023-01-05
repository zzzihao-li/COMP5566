## Step 1: build docker images
1. enter into the `bootnode` path, e.g., `cd ./bootnode/`
2. run `sudo docker build -t bootnode .` to build the `bootnode` image
3. enter into the `node` path, e.g., `cd ./node/`
4. run `sudo docker build -t node .` to build the `node` image
5. run `sudo docker image ps` to check the images, the terminal will output contents like the following information
   ```sh
   REPOSITORY           TAG       IMAGE ID       CREATED          SIZE
   node                 latest    3fa445ef9361   6 seconds ago    384MB
   bootnode             latest    a5c759aa8ae6   48 seconds ago   384MB
   ethereum/client-go   v1.6.6    18a3fff827f9   5 years ago      384MB
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
   sudo docker run --name bot1 -it node /bin/bash
   sudo docker run --name bot2 -it node /bin/bash
   sudo docker run --name bot3 -it node /bin/bash
   ```
4. check the running containers by `sudo docker ps`, and the terminal will output contents like the following information
   ```sh
   0283a5ce56b1   node       "/bin/sh -c sh /bin/…"   12 seconds ago   Up 11 seconds   8545/tcp, 30303/tcp, 30303/udp   bot3
   76f6ea76800f   node       "/bin/sh -c sh /bin/…"   21 seconds ago   Up 20 seconds   8545/tcp, 30303/tcp, 30303/udp   bot2
   7a26db02df5e   node       "/bin/sh -c sh /bin/…"   29 seconds ago   Up 28 seconds   8545/tcp, 30303/tcp, 30303/udp   bot1
   1081a3dfe133   node       "/bin/sh -c sh /bin/…"   2 minutes ago    Up 2 minutes    8545/tcp, 30303/tcp, 30303/udp   node3
   1292d29fb763   node       "/bin/sh -c sh /bin/…"   2 minutes ago    Up 2 minutes    8545/tcp, 30303/tcp, 30303/udp   node2
   bf9027c06ece   node       "/bin/sh -c sh /bin/…"   3 minutes ago    Up 3 minutes    8545/tcp, 30303/tcp, 30303/udp   node1
   08a8ec2e2619   bootnode   "/bin/sh -c sh /bin/…"   18 minutes ago   Up 18 minutes   8545/tcp, 30303/tcp, 30303/udp   boot
   ```