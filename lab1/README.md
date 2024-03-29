Blockchain eclipse demonstration
================================

### ***Imporant notice:*** This is a PoC attack. It was performed in a controlled environment.

This project uses Geth v1.6.6 (Ethereum Client) and runs on Docker.
It is composed of three parts:

    * Bootnode: first node to run on the network.
    * Node: nodes connecting to bootnode.
    * Botnode: bots to perform eclipse attacks

Each part has it's own Dockerfile and scripts. The scripts are as follows:

    * generate_genesis.py: used to generate genesis block.
    * start_console.sh: used inside a container to start Geth console.
    * genesis.json: genesis block template (without funds).

If you want to build the lab environment from scratch, please refer to the **preparation.md** file.
Besides, **attack.md** file show how to eclipse an Ethereum node.

## Tips
1. `sudo docker build -t xxx .` build an image with the name `xxx` (DO NOT forget the "." in the last)
2. `sudo docker run --name xxx -it` start a container with the name `xxx`
3. `Ctrl + P + Q` exit a container without stopping it
4. `sudo docker attach` enter a running container
5. `ip addr` check current IP address
6. `sudo docker exec xxx ip addr` execute *ip addr* in the container `xxx`
7. `sudo docker ps -a` display all containers
8. `sudo docker rm -f xxx` remove the container `xxx`
## Slides
Link：https://docs.google.com/presentation/d/1VQrZVW35tdy9uLH37WWC9n0sXGEp5g2cKVYh6TKsoN4/edit
