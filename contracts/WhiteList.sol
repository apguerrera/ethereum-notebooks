pragma solidity ^0.4.25;

// ----------------------------------------------------------------------------
// BokkyPooBah's White List
//
//
// Enjoy.
//
// (c) BokkyPooBah / Bok Consulting Pty Ltd. The MIT Licence.
// ----------------------------------------------------------------------------

import "./Controlled.sol";
import "./WhiteListInterface.sol";


// ----------------------------------------------------------------------------
// White List - on list or not
// ----------------------------------------------------------------------------
contract WhiteList is WhiteListInterface, Controlled {
    mapping(address => bool) public whiteList;

    event AccountListed(address indexed account, bool status);

    constructor() public {
        initControlled(msg.sender);
    }

    function isInWhiteList(address account) public view returns (bool) {
        return whiteList[account];
    }

    function add(address[] accounts) public onlyController {
        require(accounts.length != 0);
        for (uint i = 0; i < accounts.length; i++) {
            require(accounts[i] != address(0));
            if (!whiteList[accounts[i]]) {
                whiteList[accounts[i]] = true;
                emit AccountListed(accounts[i], true);
            }
        }
    }
    function remove(address[] accounts) public onlyController {
        require(accounts.length != 0);
        for (uint i = 0; i < accounts.length; i++) {
            require(accounts[i] != address(0));
            if (whiteList[accounts[i]]) {
                delete whiteList[accounts[i]];
                emit AccountListed(accounts[i], false);
            }
        }
    }
}
