pragma solidity ^0.4.25;

import "./Owned.sol";

// ----------------------------------------------------------------------------
// Maintain a list of controllers that are permissioned to execute certain
// functions
// ----------------------------------------------------------------------------
contract Controlled  is Owned {
    mapping(address => bool) public controllers;

    event ControllerAdded(address _controller);
    event ControllerRemoved(address _controller);

    modifier onlyController() {
        require(controllers[msg.sender] || mOwner == msg.sender);
        _;
    }

    function initControlled(address _owner) internal {
        initOwned(_owner);
        controllers[_owner] = true;
    }
    function addController(address _controller) public  onlyOwner  {
        require(!controllers[_controller]);
        controllers[_controller] = true;
        emit ControllerAdded(_controller);
    }
    function removeController(address _controller) public  onlyOwner {
        require(controllers[_controller]);
        delete controllers[_controller];
        emit ControllerRemoved(_controller);
    }
    function isControllable() external view returns (bool) {
        return controllers[msg.sender];
    }

}
