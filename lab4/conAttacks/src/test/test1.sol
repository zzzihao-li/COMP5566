pragma solidity 0.8.10;

import "ds-test/test.sol";

contract User {
  function callOnlyOwner(Blacksmith b) public {
    b.onlyOwner();
  }
}

contract Blacksmith {
  address public owner;

  constructor(address _owner){
    owner = _owner;
  }

  function onlyOwner() public{
    require(msg.sender == owner, "Not the owner");
  }
}

contract BlacksmithTest is DSTest {
    Blacksmith blacksmith;
    User user;

    function setUp() public {
      blacksmith = new Blacksmith(address(this));
      user = new User();    
    }

    function testOwner() public {
        assertEq(blacksmith.owner(),address(this));
    }

    function testFailOwner() public {
       user.callOnlyOwner(blacksmith);
    }

    function testWrongOwner() public {
        user.callOnlyOwner(blacksmith); // This test will fail
    }
}