# !/usr/bin/python3
# -*- coding: UTF-8 -*-
from web3 import Web3

def runRPC(port):
    w3 = Web3(Web3.HTTPProvider("http://localhost:" + str(port), request_kwargs={'timeout': 60}))
    assert w3.isConnected() == True, "[ERROR] Testnet is not activated."
    return w3

def main():
    nodeA = runRPC(8545)
    BlockA = nodeA.eth.get_block("latest") 

    nodeB = runRPC(8546)
    BlockB = nodeB.eth.get_block("latest") 
    
    print("Node\tNumber\tHash")
    print(f"A\t{BlockA['number']}\t{BlockA['hash'].hex()}")
    print(f"B\t{BlockB['number']}\t{BlockB['hash'].hex()}")


main()