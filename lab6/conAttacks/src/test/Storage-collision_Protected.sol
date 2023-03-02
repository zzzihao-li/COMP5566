// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "forge-std/Test.sol";
 
contract ContractTest is Test {
    Logic LogicContract;
    Proxy ProxyContract;

    function testStorageCollision() public {

        LogicContract = new Logic();
        ProxyContract = new Proxy(address(LogicContract));

        console.log("Current implementation contract address:",ProxyContract._implementation());
        ProxyContract.invoke(
            abi.encodeWithSignature("foo(address)",address(0x0)));
        console.log("Overwrited slot0 implementation contract address:",ProxyContract._implementation());
        console.log("Exploit completed");
    }
    receive() payable external{}
}

contract Proxy {
    address public implementation;  //slot0

    /**
     * @dev Storage slot with the address of the current implementation.
     * This is the keccak-256 hash of "org.zeppelinos.proxy.implementation", and is
     * validated in the constructor.
     */
    bytes32 private constant IMPLEMENTATION_SLOT = 0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3;

    function _implementation() public view returns (address impl) {
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly {
            impl := sload(slot)
        }
    }

    /**
     * @dev Sets the implementation address of the proxy.
     * @param newImplementation Address of the new implementation.
     */
    function _setImplementation(address newImplementation) private {

        bytes32 slot = IMPLEMENTATION_SLOT;

        assembly {
            sstore(slot, newImplementation)
        }
    }

    constructor (address _implementation) public {
        _setImplementation(_implementation);
    }

    function invoke(bytes memory _calldata) public {
        _implementation().delegatecall(_calldata);
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