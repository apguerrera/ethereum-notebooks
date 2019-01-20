pragma solidity ^0.4.25;

// ----------------------------------------------------------------------------
// White List interface
// ----------------------------------------------------------------------------

contract WhiteListInterface {
    function isInWhiteList(address account) public view returns (bool);
}
