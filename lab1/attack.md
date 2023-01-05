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
   
   After `admin.nodeInfo`, we get the node id and port of the bootnode, e.g., **e68f458cfc42bebc5b9212a3b5b15faf8335506ea3043505efaf9fd550aa44074e6c9f0777c5d33928d04cdfa671f8aeba98eda9f4f0203d725844fd4495dfc4** and **30303**.

   Hence, the enode url of the bootnode is **enode://e68f458cfc42bebc5b9212a3b5b15faf8335506ea3043505efaf9fd550aa44074e6c9f0777c5d33928d04cdfa671f8aeba98eda9f4f0203d725844fd4495dfc4@172.17.0.2:30303**
   
   Finally, you can exit the bootnode with keeping it alive.

2. We then launch the 3 honest nodes with connecting to the bootnode. (I have set the maxpeers parameter as 3 for honest nodes in the `./start_console.sh`)
   ```sh
   sudo docker attach node1
   ip addr
   ./start_console.sh enode://e68f458cfc42bebc5b9212a3b5b15faf8335506ea3043505efaf9fd550aa44074e6c9f0777c5d33928d04cdfa671f8aeba98eda9f4f0203d725844fd4495dfc4@172.17.0.2:30303
   admin.nodeInfo
   ```
   After `sudo docker attach node1`, we enter into the running node1 container.
   
   After `./start_console.sh enode://e68f458cfc42bebc5b9212a3b5b15faf8335506ea3043505efaf9fd550aa44074e6c9f0777c5d33928d04cdfa671f8aeba98eda9f4f0203d725844fd4495dfc4@172.17.0.2:30303`, we launch the geth 
   client in node1 with connecting to the bootnode.

   Besides, we pick the node1 as the victim node and compute its enode url as **enode://caa269ed6e766a12c656cd8f86ba9b1d57113ce890b7be7c61ffc9e6f529b73ba815c077852f9fdad218d1ab1112b198cf8c76eb6a674dfa82b2db033fe65bf4@172.17.0.3:30303**

   You can exit node1 with keeping it alive.

   Then, repeat the same steps to launch the geth clients in node2 and node3.

   In node3, after launching the geth client, you can check whether all three nodes are connected to the network by checking the peers of node3.
   ```sh
   admin.peers
   ```
   Then the terminal will output contents like the following, which means node3 has three peers, and ip addresses of the three peers are "172.17.0.4, 172.17.0.3, 172.17.0.2" 
   ```sh
   [{
        caps: ["eth/63"],
        id: "238e4b1a5f6eb0311831397a8a2dd3f83c740e0283dee4f69c546e49c90c35258971d419315ceea2f2f111a08af8326fbf1b9fe0435e5af12b819dfc484db440",
        name: "Geth/v1.6.6-stable/linux-amd64/go1.7.3",
        network: {
        localAddress: "172.17.0.5:50310",
        remoteAddress: "172.17.0.4:30303"
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
        id: "caa269ed6e766a12c656cd8f86ba9b1d57113ce890b7be7c61ffc9e6f529b73ba815c077852f9fdad218d1ab1112b198cf8c76eb6a674dfa82b2db033fe65bf4",
        name: "Geth/v1.6.6-stable/linux-amd64/go1.7.3",
        network: {
        localAddress: "172.17.0.5:43364",
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
        id: "e68f458cfc42bebc5b9212a3b5b15faf8335506ea3043505efaf9fd550aa44074e6c9f0777c5d33928d04cdfa671f8aeba98eda9f4f0203d725844fd4495dfc4",
        name: "Geth/v1.6.6-stable/linux-amd64/go1.7.3",
        network: {
        localAddress: "172.17.0.5:30303",
        remoteAddress: "172.17.0.2:37386"
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
   ./start_console.sh enode://e68f458cfc42bebc5b9212a3b5b15faf8335506ea3043505efaf9fd550aa44074e6c9f0777c5d33928d04cdfa671f8aeba98eda9f4f0203d725844fd4495dfc4@172.17.0.2:30303
   admin.nodeInfo
   admin.addPeer("enode://caa269ed6e766a12c656cd8f86ba9b1d57113ce890b7be7c61ffc9e6f529b73ba815c077852f9fdad218d1ab1112b198cf8c76eb6a674dfa82b2db033fe65bf4@172.17.0.3:30303")
   ```

   After `admin.addPeer("enode://caa269ed6e766a12c656cd8f86ba9b1d57113ce890b7be7c61ffc9e6f529b73ba815c077852f9fdad218d1ab1112b198cf8c76eb6a674dfa82b2db033fe65bf4@172.17.0.3:30303")`, we add the node1 to be bot1's peer.

   You can check the peers of bot1, it shows that bot1 doesnot have the peer of node1. This is because the peers of node1 reach to the limit (3).

   You can exit bot1 with keeping it alive.

   Then, repeat the same steps to launch the geth clients in bot2 and bot3.

4. We get back to node1, and reboot it.
   ```sh
   sudo docker attach node1
   admin.peers
   ```
   We can first check the peers of node1. It shows that node1 has three peers, i.e., bootnode, node2, and node3.

   Then we reboot geth client in node1.
   ```sh
   exit
   ./start_console.sh enode://e68f458cfc42bebc5b9212a3b5b15faf8335506ea3043505efaf9fd550aa44074e6c9f0777c5d33928d04cdfa671f8aeba98eda9f4f0203d725844fd4495dfc4@172.17.0.2:30303
   ```

   Now we check the peers of node1 by `admin.peers`, and we can find that the peers of node1 are the bootnode, bot2, and bot3. It shows that the peers of node1 are eclipsed by the bot nodes.


## Notes
While connecting to the Ethereum mainnet, we do not need to set the bootnode, and the geth client will automatically search peers. In the lab1, we demostrate eclipse attack in a controlled environment by using our bootnode.