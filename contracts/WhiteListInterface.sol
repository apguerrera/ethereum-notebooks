pragma solidity ^0.5.3;

// ----------------------------------------------------------------------------
// White List interface
// ----------------------------------------------------------------------------

contract WhiteListInterface {
    function isInWhiteList(address account) public view returns (bool);
}
