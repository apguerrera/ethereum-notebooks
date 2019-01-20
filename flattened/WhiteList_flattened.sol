pragma solidity ^0.4.25;

// ----------------------------------------------------------------------------
// BokkyPooBah's White List
//
//
// Enjoy.
//
// (c) BokkyPooBah / Bok Consulting Pty Ltd. The MIT Licence.
// ----------------------------------------------------------------------------



// ----------------------------------------------------------------------------
// Owned contract
// ----------------------------------------------------------------------------
contract Owned {

address public mOwner;      // AG should be private
bool public initialised;    // AG should be private

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  /**
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */

  function initOwned(address _owner) internal {
      require(!initialised);
      mOwner = _owner;
      initialised = true;
      emit OwnershipTransferred(address(0), mOwner);

  }

  /**
   * @return the address of the owner.
   */
  function owner() public view returns (address) {
      return mOwner;
  }

  /**
   * @dev Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
      require(isOwner());
      _;
  }

  /**
   * @return true if `msg.sender` is the owner of the contract.
   */
  function isOwner() public view returns (bool) {
      return msg.sender == mOwner;
  }

  /**
   * @dev Allows the current owner to relinquish control of the contract.
   * @notice Renouncing to ownership will leave the contract without an owner.
   * It will not be possible to call the functions with the `onlyOwner`
   * modifier anymore.
   */
  function renounceOwnership() public onlyOwner {
      emit OwnershipTransferred(mOwner, address(0));
      mOwner = address(0);
  }

  /**
   * @dev Allows the current owner to transfer control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function transferOwnership(address newOwner) public onlyOwner {
      _transferOwnership(newOwner);
  }

  /**
   * @dev Transfers control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function _transferOwnership(address newOwner) internal {
      require(newOwner != address(0));
      emit OwnershipTransferred(mOwner, newOwner);
      mOwner = newOwner;
  }
}

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

// ----------------------------------------------------------------------------
// White List interface
// ----------------------------------------------------------------------------

contract WhiteListInterface {
    function isInWhiteList(address account) public view returns (bool);
}


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
