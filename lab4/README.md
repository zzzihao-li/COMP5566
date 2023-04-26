In the 4th Lab tutorial, we will use [Foundry](https://book.getfoundry.sh/) to reproduce typical attacks towards Ethereum smart contracts.

## Environment requiremet
1. You need to prepare a computer with Linux OS or deploy a Linux VM image in your computer.
2. Follow the following instructions to install **Foundry** on your equipment.
   - `sudo docker pull ghcr.io/foundry-rs/foundry:latest` to install the docker configued Foundry
   - `sudo docker image ls` to check the downloaded images
   - `sudo docker run --name forge-demo -it ghcr.io/foundry-rs/foundry /bin/sh` to run a docker container

> Tips: From [instructions](https://book.getfoundry.sh/getting-started/installation), you can also install Foundry by other methods in it, but there could be some issues for installing in different environments. Hence, I suggest to install the docker image configured Foundry.

3. After entering into the container, clone code scripts of our repos for this lab into the container:
   - `git clone https://github.com/zzzihao-li/COMP5566.git`
  
  Now you can find scripts for playing four kinds of typical attacks in dict `./COMP5566/lab4/conAttacks/src/test/`

## Slides

Link: https://docs.google.com/presentation/d/1gG2D84sMEsXqCKoeBaJU1umhWVp07UeRXMQH4zpx_1E/edit?usp=sharing
