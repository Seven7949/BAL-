// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Vulnerable {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        if (balances[msg.sender] >= amount) {
            (bool sent, ) = msg.sender.call{value: amount}("");
            require(sent, "Failed");
            balances[msg.sender] -= amount; // state write after external call -> vulnerable
        }
    }
}

