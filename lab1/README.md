Blockchain eclipse demonstration
================================

### ***Imporant notice:*** This is a PoC attack. It was performed in a controlled environment.

This project uses Geth (Ethereum Client) and runs on Docker.
It is composed of three parts:

    * Backend: monitoring network with eth-netstats dashboard.
    * Bootnode: first node to run on the network.
    * Node: nodes connecting to bootnode.

Each part has it's own Dockerfile and scripts. The scripts are as follows:

    * generate_genesis.py: used to generate genesis block.
    * start_console.sh: used inside a container to start Geth console.
    * genesis.json: genesis block template (without funds).

For steps on how to run, watch [video](https://www.youtube.com/watch?v=i9WVCJIaq3w)